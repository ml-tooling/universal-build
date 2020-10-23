from typing import Dict, List, Match, Optional, Tuple, Union
import argparse
import subprocess
import os
import re
import sys

ALLOWED_BRANCH_TYPES = ["release", "production"]
MAIN_BRANCH_NAMES = ["master", "main"]

FLAG_MAKE = "make"
FLAG_TEST = "test"
FLAG_RELEASE = "release"
FLAG_VERSION = "version"
FLAG_SKIP_PATH = "skip_path"
FLAG_FORCE = "force"
FLAG_DOCKER_IMAGE_PREFIX = "docker_image_prefix"
FLAG_DOCKER = "docker"
FLAG_SANITIZED = "_sanitized"

EXIT_CODE_GENERAL = 1
EXIT_CODE_INVALID_VERSION = 2
EXIT_CODE_NO_VERSION_FOUND = 3
EXIT_CODE_VERSION_IS_REQUIRED = 4
EXIT_CODE_DEV_VERSION_REQUIRED = 5
EXIT_CODE_DEV_VERSION_NOT_MATCHES_BRANCH = 6
EXIT_CODE_INVALID_ARGUMENTS = 7


def log(message: str):
    print(message, flush=True)


def get_sanitized_arguments(
    arguments: List[str] = None, argument_parser: argparse.ArgumentParser = None
) -> Dict[str, Union[str, bool]]:
    """Return sanitized default arguments when they are valid.
    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Args:
        arguments (List[str], optional): List of arguments that are used instead of the arguments passed to the process. Defaults to None.
        argument_parser (arparse.ArgumentParser, optional): An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. Must be initialized with `add_help=False` flag like argparse.ArgumentParser(add_help=False)!

    Returns:
        Dict[str, Union[bool, str]]: The parsed default arguments thar are already checked for validity.
    """

    argument_parser = argument_parser or argparse.ArgumentParser(add_help=False)
    parser = _get_default_cli_arguments_parser(argument_parser)
    args, unknown = parser.parse_known_args(args=arguments)

    if args._sanitized:
        return vars(args)

    if not _is_valid_command_combination(args):
        exit_process(EXIT_CODE_INVALID_ARGUMENTS)

    # Handle login when using the buld container
    if args.release and args.docker:
        completed_process = run(
            f"docker login -u {os.getenv('DOCKER_USERNAME')} -p {os.getenv('DOCKER_ACCESS_TOKEN')}"
        )
        if completed_process.returncode > 0:
            log(
                "Could not login into Docker repository. The environment variables DOCKER_USERNAME and DOCKER_ACCESS_TOKEN have to be set. Think about using an access token instead of your actual password."
            )

    existing_versions = _get_version_tags()
    try:
        version = _get_version(
            args.version, args.force, existing_versions=existing_versions
        )
    except VersionInvalidFormatException as e:
        log(str(e))
        exit_process(EXIT_CODE_INVALID_VERSION)
    except VersionInvalidPatchNumber as e:
        log(str(e))
        exit_process(EXIT_CODE_INVALID_VERSION)
    except Exception as e:
        version = None

    if args.release and version is None:
        log("For a release a valid semantic version has to be set.")
        exit_process(EXIT_CODE_VERSION_IS_REQUIRED)
    elif args.release is False and version is None:
        latest_branch_version = _get_latest_branch_version()
        if not latest_branch_version:
            log(
                "No version found in branch. Please provide the semantic version you are working on or create a tag in your current git branch."
            )
            exit_process(EXIT_CODE_NO_VERSION_FOUND)
        elif latest_branch_version.suffix == "" and not args.force:
            log(
                f"No version was provided and the last found version in the git branch looks like a release version ({latest_branch_version.to_string()}). \
                Please provide a dev version or create a dev version git tag in the current branch or set the '--{FLAG_FORCE}' flag."
            )
            exit_process(EXIT_CODE_DEV_VERSION_REQUIRED)
        elif not _is_dev_tag_belonging_to_branch(
            latest_branch_version, _get_current_branch()[0]
        ):
            log(
                f"The found dev version {latest_branch_version.to_string()} does not belong to branch {_get_current_branch()[0]}. Please remove the tag or pass it manually via the --{FLAG_VERSION} flag."
            )
            exit_process(EXIT_CODE_DEV_VERSION_NOT_MATCHES_BRANCH)

        version = latest_branch_version
    elif args.release is False and version:
        version.suffix = _get_dev_suffix(_get_current_branch()[0])

    # Reset the existing dev tag to the current HEAD.
    force_git_creation = not args.release
    create_git_tag(version.to_string(), force=force_git_creation)
    args.version = version.to_string()
    args._sanitized = True
    return vars(args)


def concat_command_line_arguments(args: dict) -> str:
    command_line_arguments = ""

    for arg in args:
        arg_value = args[arg]  # getattr(args, arg)
        if arg_value:
            # For boolean types, the existence of the flag is enough
            if type(arg_value) == bool:
                command_line_arguments += f" --{arg}"
            else:
                command_line_arguments += f" --{arg}={arg_value}"
    return command_line_arguments


def build_docker_image(
    name: str, version: str, build_args: str = ""
) -> subprocess.CompletedProcess:
    versioned_image = name + ":" + version
    latest_image = name + ":latest"
    completed_process = run(
        "docker build -t "
        + versioned_image
        + " -t "
        + latest_image
        + " "
        + build_args
        + " ./"
    )

    if completed_process.returncode > 0:
        log(f"Failed to build Docker image {name}:{version}")

    return completed_process


def release_docker_image(
    name: str, version: str, docker_image_prefix: str = ""
) -> subprocess.CompletedProcess:
    """Push a Docker image to a repository.

    Args:
        name (str): The name of the image. Must not be prefixed!
        version (str): The tag used for the image.
        docker_image_prefix (str, optional): The prefix added to the name to indicate an organization on DockerHub or a completely different repository. Defaults to "".

    Returns:
        subprocess.CompletedProcess: Returns the CompletedProcess object of the `docker push ...` command.
    """

    if not docker_image_prefix:
        log(
            f"The flag --docker-image-prefix cannot be blank when pushing a Docker image."
        )
        exit_process(EXIT_CODE_GENERAL)

    versioned_image = name + ":" + version
    latest_image = name + ":latest"
    remote_versioned_image = docker_image_prefix + versioned_image
    run("docker tag " + versioned_image + " " + remote_versioned_image)
    completed_process = run("docker push " + remote_versioned_image)

    if completed_process.returncode > 0:
        log(f"Failed to release Docker image {name}:{version}")

    if "-dev" not in version:
        log("Release Docker image with latest tag as well.")
        remote_latest_image = docker_image_prefix + latest_image
        run("docker tag " + latest_image + " " + remote_latest_image)
        run("docker push " + remote_latest_image)

    return completed_process


def create_git_tag(version: str, push: bool = False, force: bool = False):
    """Create an annotated git tag in the current HEAD via `git tag` and the provided version.
    The version will be prefixed with 'v'.

    Args:
        version (str): The tag to be created. Will be prefixed with 'v'.
        push (bool, optional): If true, push the tag to remote. Defaults to False.
        force (bool, optional): If true, force the tag to be created. Defaults to False.
    """
    force_flag = "-f" if force else ""
    completed_process = run(
        f"git tag -a -m 'Automatically tagged during build process.' {force_flag} v{version}",
        disable_stderr_logging=True,
    )

    if completed_process.returncode > 0:
        log(f"Executing `git tag` for version v{version} might have a problem: {completed_process.stderr}")

    if push:
        run(f"git push origin v{version}")


def build(component_path: str, args: Dict[str, str]):
    """Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths.

    Args:
        component_path (str): The path of the component to be built. The path must contain a build.py file.
        args (Dict): The arguments to be passed to the component's build.py file. The default arguments that were used to call this
            script are passed down to the component.
    """

    if _is_path_skipped(component_path, args[FLAG_SKIP_PATH]) is True:
        return

    build_command = _create_build_cmd_from_args(component_path, args)
    completed_process = run(build_command)

    if completed_process.returncode > 0:
        error_message = completed_process.stderr or completed_process.stdout
        log(
            f"Failed to build module {component_path}. Code: {completed_process.returncode}. Reason: {error_message}"
        )
        exit_process(EXIT_CODE_GENERAL)


def run(
    command: str,
    disable_stdout_logging: bool = False,
    disable_stderr_logging: bool = False,
) -> subprocess.CompletedProcess:
    """Wrapper for subprocess.run() to print our

    Args:
        command (str): The shell command that is executed via subprocess.Popen.
        disable_stdout_logging (bool): Disable stdout logging when it is too much or handled by the caller.

    Returns:
        subprocess.CompletedProcess: State
    """
    log("Executing: " + command)

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout = ""
    stderr = ""
    with process.stdout:
        for line in iter(process.stdout.readline, ""):
            if not disable_stdout_logging:
                log(line.rstrip("\n"))
            stdout += line
    with process.stderr:
        for line in iter(process.stderr.readline, ""):
            if not disable_stderr_logging:
                log(line.rstrip("\n"))
            stderr += line

    exitcode = process.wait()

    # return completed_process
    return subprocess.CompletedProcess(
        args=command, returncode=exitcode, stdout=stdout, stderr=stderr
    )


def exit_process(code: int = 0):
    """
    Exit the process with exit code.
    `sys.exit` seems to be a bit unreliable, process just sleeps and does not exit.
    So we are using os._exit instead and doing some manual cleanup.
    """
    import gc
    import atexit

    gc.collect()
    atexit._run_exitfuncs()
    sys.stdout.flush()
    os._exit(code)


# Private functions


def _get_current_branch() -> Tuple[str, str]:
    """Get the current branch name and type (feature, production, release etc.) if existing.

    Returns:
        Tuple: (branchname, type)
    """
    full_branch_name = run("git branch --show-current").stdout.rstrip("\n")
    if full_branch_name == "":
        full_branch_name = "HEAD"
    path_parts = full_branch_name.split("/")

    if len(path_parts) == 1:
        return (path_parts[0], "")
    else:
        # if a branch name consists of multiple slashes, the parts are concatenated; otherwise it just consists of the normal branch name
        # Example: "feature/foo/bar" -> (feature, foo-bar); "feature/foo" -> (feature, foo)
        merged_branch_name = "-".join(path_parts[1:])
        return (path_parts[0], merged_branch_name)


def _is_path_skipped(path: str, skip_paths: List[str] = []) -> bool:
    """Check whether the path is itself defined as a skip_path or is a sub-path of a skipped path.

    Args:
        path (str): The path to be checked
        skip_path (list, optional): The pathes to be skipped. Sub-pathes of these skip-pathes will be skipped as well. Defaults to [].

    Returns:
        bool: Return true if the path should be skipped
    """
    skip_paths = skip_paths or []
    for skip_path in skip_paths:
        if os.path.commonpath([path, skip_path]) != "":
            return True

    return False


def _get_default_cli_arguments_parser(
    initial_parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(parents=[initial_parser])

    # NEW FLAGS
    parser.add_argument(
        f"--{FLAG_MAKE}", help="Make/compile/package all artefacts", action="store_true"
    )
    parser.add_argument(
        f"--{FLAG_TEST}", help="Run unit and integration tests", action="store_true"
    )
    parser.add_argument(
        f"--{FLAG_RELEASE}",
        help="Release all artefacts to respective remote registries (e.g. DockerHub)",
        action="store_true",
    )
    parser.add_argument(
        f"--{FLAG_VERSION}", help="Version of build (MAJOR.MINOR.PATCH-TAG)"
    )
    parser.add_argument(
        f"--{FLAG_FORCE}",
        help="Ignore all enforcements and warnings and run the action",
        action="store_true",
    )
    parser.add_argument(
        "--skip-path",
        help="Skips the build phases for all (sub)paths provided here",
        action="append",
    )
    parser.add_argument(
        "--docker-image-prefix",
        help="With this flag you can provide a prefix for a Docker image, e.g. 'mltooling/' or even a repository path. When leaving blank, the default Dockerhub Repository is used.",
    )
    parser.add_argument(
        f"--{FLAG_DOCKER}",
        help="Build it with help of the Builder Docker container instead of locally on your machine.",
        action="store_true",
    )
    parser.add_argument(
        f"--{FLAG_SANITIZED}",
        help="Indicates that a parent build.py script already checked the validity of the passed arguments so that subsequent scripts don't do it again.",
        action="store_true",
    )

    return parser


def _create_build_cmd_from_args(module_path: str, sanitized_args: dict):
    build_command = "python -u build.py " + concat_command_line_arguments(
        sanitized_args
    )

    working_dir = os.path.dirname(os.path.realpath(__file__))
    full_command = (
        "cd '" + module_path + "' && " + build_command + " && cd '" + working_dir + "'"
    )
    log("Building " + module_path + " with: " + full_command)
    return full_command


def _is_valid_command_combination(args: argparse.Namespace) -> bool:
    if (
        args.release
        and (not args.version or not args.test or not args.make)
        and not args.force
    ):
        log(
            f"Please provide a version for deployment (--{FLAG_VERSION}=MAJOR.MINOR.PATCH-TAG)"
        )
        log(f"Test must be executed before the deployment (--{FLAG_TEST})")
        log(f"Build must be executed before the deployment (--{FLAG_MAKE})")

        return False

    if args.release:
        current_branch, current_branch_type = _get_current_branch()
        if (
            current_branch.lower() not in MAIN_BRANCH_NAMES
            and current_branch_type.lower() not in ALLOWED_BRANCH_TYPES
            and not args.force
        ):
            log(
                f"Release is only allowed from branches: [{', '.join(MAIN_BRANCH_NAMES)}] or in branch types: [{', '.join(ALLOWED_BRANCH_TYPES)}]"
            )
            return False

    return True


def _get_version_tags() -> List["Version"]:
    unformatted_tags = _get_remote_git_tags()
    versions = []
    for tag in unformatted_tags:
        tag_parts = tag.split("/")
        tag = tag_parts[-1]
        # only consider tags that resemble versions
        version = Version.get_version_from_string(tag)
        if version is not None:
            versions.append(version)
    return versions


def _get_latest_branch_version(branch_name: str = "") -> Optional["Version"]:
    result = run(
        "git describe --tags --match 'v[0-9].*' --abbrev=0",
        disable_stdout_logging=True,
    )

    return Version.get_version_from_string(result.stdout.rstrip("\n"))


def _is_dev_tag_belonging_to_branch(version: "Version", branch_name: str = "") -> bool:
    # The found dev-version does not belong to the current branch
    print(version.to_string(), _get_dev_suffix(branch_name))
    if (
        branch_name
        and version
        and version.suffix
        and version.suffix != _get_dev_suffix(branch_name)
    ):
        return False

    return True


def _get_remote_git_tags() -> List[str]:
    result = run(
        "git ls-remote --tags --sort='-v:refname' --refs", disable_stdout_logging=True
    )
    return result.stdout.rstrip("\n").split("\n")


def _get_version(
    version: str, force: bool = False, existing_versions: List["Version"] = []
) -> "Version":
    """Get validated version. If force is set to True, the version is allowed to be equal or smaller than the existing patch version.

    Raises:
        VersionInvalidFormatException: Raised when the provided version's format is not valid
        VersionInvalidPatchNumber: Raised when existing or higher version in the patch branch exists
        Exception: Raised when no version is passed

    Args:
        version (str): The version to be checked for validity. It will be tried to be transformed into a build_utils.Version object.
        force (bool, optional): If set tu true, the version can be equal or smaller than existing patch version version numbers
        existing_versions (list, optional): The list of versions to be checked against

    Returns:
        Version: Validated version
    """
    provided_version = version

    if provided_version:
        version_obj = Version.get_version_from_string(provided_version)
        if version_obj is None:
            raise VersionInvalidFormatException(
                "The provided version {provided_version} is not in a valid format. Valid formats include 1.0.0, 1.0.0-dev or 1.0.0-dev.foo"
            )
        for existing_version in existing_versions:
            if (
                existing_version.major == version_obj.major
                and existing_version.minor == version_obj.minor
                and existing_version.patch >= version_obj.patch
                and existing_version.suffix == "" # Only consider release versions, not suffixed dev versions
                and not force
            ):
                raise VersionInvalidPatchNumber(
                    f"A version ({existing_version.to_string()}) with the same or higher patch version as provided ({version_obj.to_string()}) already exists."
                )
    else:
        raise Exception("No version is provided")

    return version_obj


def _get_current_branch_version(
    existing_versions: List["Version"] = [],
) -> Tuple["Version", List["Version"]]:
    """Returns a tuple of the best suiting version based on our logic and all available versions.

    Returns:
        [Tuple]:(best suited version | None, list of all existing versions sorted from highest to lowest based on git's sorting algorithm)
    """
    # TODO Check that latest dev tag is given although there should be only one dev version per branch
    branch_name, branch_type = _get_current_branch()
    for version in existing_versions:
        if version.suffix == _get_dev_suffix(branch_name):
            return (version, existing_versions)
    return (None, existing_versions)


def _get_dev_suffix(branch_name: Optional[str]):
    branch_name = branch_name or ""
    return "dev." + branch_name


class Version:
    major: int
    minor: int
    patch: int
    suffix: str

    def __init__(self, major, minor, patch, suffix):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.suffix = suffix

    def to_string(self):
        suffix = "" if not self.suffix else "-" + self.suffix
        return f"{self.major}.{self.minor}.{self.patch}{suffix}"

    @staticmethod
    def get_version_from_string(version: str) -> Optional["Version"]:
        version_match = Version.is_valid_version_format(version)
        if version_match is None:
            return None

        major = version_match.group(1)
        minor = version_match.group(2)
        patch = version_match.group(3)
        suffix = ""
        if version_match.lastindex == 4:
            suffix = version_match.group(4)

        return Version(major, minor, patch, suffix)

    @staticmethod
    def is_valid_version_format(version: str) -> Optional[Match[str]]:
        return re.match(
            r"^v?([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$",
            version,
        )


class VersionInvalidFormatException(BaseException):
    pass


class VersionInvalidPatchNumber(BaseException):
    pass
from typing import Dict, List, Match, Optional, Tuple, Union
import argparse
import subprocess
import os
import re
import sys

ALLOWED_BRANCH_TYPES = ["release", "production"]
MAIN_BRANCH_NAMES = ["master", "main"]
REMOTE_IMAGE_PREFIX = "mltooling/"


def log(message: str):
    print(message, flush=True)


def get_sanitized_arguments(
    arguments: List[str] = None,
) -> Dict[str, Union[str, bool]]:
    """Return sanitized default arguments when they are valid.
    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Returns:
        Dict[str, Union[bool, str]]: The parsed default arguments thar are already checked for validity.
    """

    parser = _get_default_cli_arguments_parser(argparse.ArgumentParser(add_help=False))
    args, unknown = parser.parse_known_args(args=arguments)

    if not _is_valid_command_combination(args):
        exit_process(1)

    try:
        version = _get_version(args.version, args.force)
    except Exception as e:
        log(str(e))
        version = None

    if args.release and version is None and not args.force:
        log("For a release a valid semantic version has to be set.")
        exit_process(2)
    elif args.release is False and version is None:
        dev_version, existing_versions = _get_current_branch_dev_version()
        if not dev_version and args.force and len(existing_versions) > 0:
            dev_version = existing_versions[0]

        if not dev_version:
            log(
                "No version found. Please provide the semantic version you are working on."
            )
            exit_process(3)
        version = dev_version
    elif args.release is False and version:
        version.suffix = _get_dev_suffix(_get_current_branch()[0])

    args.version = version.to_string()
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
    return run(
        "docker build -t "
        + versioned_image
        + " -t "
        + latest_image
        + " "
        + build_args
        + " ./"
    )


def release_docker_image(name: str, version: str) -> subprocess.CompletedProcess:
    versioned_image = name + ":" + version
    latest_image = name + ":latest"
    remote_versioned_image = REMOTE_IMAGE_PREFIX + versioned_image
    run("docker tag " + versioned_image + " " + remote_versioned_image)
    completed_process = run("docker push " + remote_versioned_image)

    if "-dev" not in version:
        remote_latest_image = REMOTE_IMAGE_PREFIX + latest_image
        run("docker tag " + latest_image + " " + remote_latest_image)
        run("docker push " + remote_latest_image)

    return completed_process


def create_git_tag(args: Dict[str, Union[bool, str]]):
    completed_process = run(
        f"git tag -a -m 'Automatically tagged during build process.' {args['version']}"
    )

    if completed_process.returncode == 128:
        log(f"Git tag {args['version']} already exists.")
    elif completed_process.returncode > 0:
        log(completed_process.stderr)

    if args["release"]:
        run(f"git push origin {args['version']}")


def build(component_path: str, args: Dict[str, str]):
    """Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths.

    Args:
        component_path (str): The path of the component to be built. The path must contain a build.py file.
        args (Dict): The arguments to be passed to the component's build.py file. The default arguments that were used to call this
            script are passed down to the component.
    """

    if _is_path_skipped(component_path, args["skip_path"]) is True:
        return

    build_command = _create_build_cmd_from_args(component_path, args)
    completed_process = run(build_command)

    for line in completed_process.stdout.split('\n'):
        print(line)

    if completed_process.returncode > 0:
        error_message = completed_process.stderr or completed_process.stdout
        log(f"Failed to build module {component_path}. Code: {completed_process.returncode}. Reason: {error_message}")
        exit_process(1)


def run(command: str) -> subprocess.CompletedProcess:
    """Wrapper for subprocess.run() to print our

    Returns:
        subprocess.CompletedProcess: State
    """
    log("Executing: " + command)
    return subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
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
        "--make", help="Make/compile/package all artefacts", action="store_true"
    )
    parser.add_argument(
        "--test", help="Run unit and integration tests", action="store_true"
    )
    parser.add_argument(
        "--release",
        help="Release all artefacts to respective remote registries (e.g. DockerHub)",
        action="store_true",
    )
    parser.add_argument("--version", help="Version of build (MAJOR.MINOR.PATCH-TAG)")
    parser.add_argument(
        "--force",
        help="Ignore all enforcements and warnings and run the action",
        action="store_true",
    )
    parser.add_argument(
        "--skip-path",
        help="Skips the build phases for all (sub)paths provided here",
        action="append",
    )
    parser.add_argument(
        "--docker",
        help="Build it with help of the Builder Docker container instead of locally on your machine.",
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
        log("Please provide a version for deployment (--version=MAJOR.MINOR.PATCH-TAG)")
        log("Test must be executed before the deployment (--test)")
        log("Build must be executed before the deployment (--make)")

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


def _get_remote_git_tags() -> List[str]:
    result = run("git ls-remote --tags --sort='-v:refname' --refs")
    return result.stdout.rstrip("\n").split("\n")


def _get_version(version: str, force: bool = False) -> "Version":
    """Get version. If force is set to True, the version is allowed to be equal or smaller than the existing patch version.
    Raises:
        Exception: Raises an exception when the provided version's format is not valid, an existing or higher version in the patch branch exists or no version is passed. The exception contains a respective message.
    Returns:
        Version: Validated version
    """
    provided_version = version
    existing_versions = _get_version_tags()
    if provided_version:
        version_obj = Version.get_version_from_string(provided_version)
        if version_obj is None:
            raise Exception(
                "The provided version {provided_version} is not in a valid format. Valid formats include 1.0.0, 1.0.0-dev or 1.0.0-dev.foo"
            )
        for existing_version in existing_versions:
            if (
                existing_version.major == version_obj.major
                and existing_version.minor == version_obj.minor
                and existing_version.patch >= version_obj.patch
                and not force
            ):
                raise Exception(
                    f"The provided patch version {version_obj.to_string()} is equal or smaller than the existing version {existing_version.to_string()}."
                )
    else:
        raise Exception("No version is provided")

    return version_obj


def _get_current_branch_dev_version() -> Tuple[Optional["Version"], List["Version"]]:
    """Returns a tuple of the best suiting version based on our logic and all available versions.

    Returns:
        [Tuple]:(best suited version | None, list of all existing versions sorted from highest to lowest based on git's sorting algorithm)
    """
    # TODO Check that latest dev tag is given although there should be only one dev version per branch
    existing_versions = _get_version_tags()
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

"""Universal build utilities."""

import argparse
import os
import re
import shutil
import subprocess
import sys
from typing import Dict, List, Match, Optional, Tuple, Union

from universal_build._utilities import DashInsensitiveDict

_ALLOWED_BRANCH_TYPES_FOR_RELEASE = ["release", "production"]
_MAIN_BRANCH_NAMES = ["master", "main"]

FLAG_MAKE = "make"
FLAG_TEST = "test"
FLAG_TEST_MARKER = "test_marker"
FLAG_RELEASE = "release"
FLAG_VERSION = "version"
FLAG_CHECK = "check"
FLAG_RUN = "run"
FLAG_FORCE = "force"

_FLAG_SKIP_PATH = "skip_path"
_FLAG_SANITIZED = "_sanitized"

TEST_MARKER_SLOW = "slow"

EXIT_CODE_GENERAL = 1
EXIT_CODE_INVALID_VERSION = 2
EXIT_CODE_NO_VERSION_FOUND = 3
EXIT_CODE_VERSION_IS_REQUIRED = 4
EXIT_CODE_DEV_VERSION_REQUIRED = 5
EXIT_CODE_DEV_VERSION_NOT_MATCHES_BRANCH = 6
EXIT_CODE_INVALID_ARGUMENTS = 7


class _Version:
    """Parsed semantic version."""

    major: int
    minor: int
    patch: int
    suffix: str

    def __init__(self, major: int, minor: int, patch: int, suffix: str):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.suffix = suffix

    def to_string(self) -> str:
        suffix = "" if not self.suffix else "-" + self.suffix
        return f"{self.major}.{self.minor}.{self.patch}{suffix}"

    @staticmethod
    def get_version_from_string(version: str) -> Optional["_Version"]:
        version_match = _Version.is_valid_version_format(version)
        if version_match is None:
            return None

        major = int(version_match.group(1))
        minor = int(version_match.group(2))
        patch = int(version_match.group(3))
        suffix = ""
        if version_match.lastindex == 4:
            suffix = version_match.group(4)

        return _Version(major, minor, patch, suffix)

    @staticmethod
    def is_valid_version_format(version: str) -> Optional[Match[str]]:
        return re.match(
            r"^v?([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$",
            version,
        )


def log(message: str) -> None:
    """Log message to stdout.

    Args:
        message (str): Message to log.
    """
    print(message, flush=True)


def command_exists(
    command: str, silent: bool = False, exit_on_error: bool = False
) -> bool:
    """Checks whether the `command` exists and is marked as executable.

    Args:
        command (str): Command to check.
        silent (bool): If `True`, no message will be logged in case the command does not exist. Default is `False`.
        exit_on_error (bool, optional): Exit process if the command does not exist. Defaults to `False`.

    Returns:
        bool: `True` if the commend exist and is executable.
    """

    # Alternative:
    # import distutils.spawn
    # return distutils.spawn.find_executable(name)

    from shutil import which

    exists: bool = which(command) is not None

    if not exists and not silent:
        log(
            f"The command {command} does not exist on the system or is not executable. Make sure to install {command}."
        )
        if exit_on_error:
            exit_process(1)

    return exists


def parse_arguments(
    input_args: List[str] = None, argument_parser: argparse.ArgumentParser = None
) -> dict:
    """Parses all arguments and returns a sanitized & augmented list of arguments.

    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Args:
        input_args (List[str], optional): List of arguments that are used instead of the arguments passed to the process. Defaults to None.
        argument_parser (arparse.ArgumentParser, optional): An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones.

    Returns:
        dict: The parsed default arguments thar are already checked for validity.
    """
    argument_parser = argument_parser or argparse.ArgumentParser()
    parser = _get_default_cli_arguments_parser(argument_parser)
    parsed_args, _ = parser.parse_known_args(args=input_args)

    if not input_args:
        input_args = sys.argv

    # convert args to dict
    args = vars(parsed_args)

    # Set defaults
    if len(input_args) <= 1:
        # Set default configuration if called without any arguments
        args[FLAG_CHECK] = True
        args[FLAG_MAKE] = True
        args[FLAG_TEST] = True

    if args.get(FLAG_TEST_MARKER) is None:
        # Set test marker to an empty list for better access
        args[FLAG_TEST_MARKER] = []

    if args.get(_FLAG_SKIP_PATH) is None:
        # Set skip path to an empty list for better access
        args[_FLAG_SKIP_PATH] = []

    # load from env variables
    args = _load_from_env_variables(args, input_args)

    if args.get(_FLAG_SANITIZED):
        log("Sanatized Arguments: " + str(args))
        return DashInsensitiveDict(args)

    if not _is_valid_command_combination(args):
        exit_process(EXIT_CODE_INVALID_ARGUMENTS)

    try:
        version: Optional[_Version] = _get_version(
            args.get(FLAG_VERSION),  # type: ignore
            args.get(FLAG_FORCE),  # type: ignore
            existing_versions=_get_version_tags(),
        )
    except _VersionInvalidFormatException as e:
        log(str(e))
        exit_process(EXIT_CODE_INVALID_VERSION)
    except Exception:
        version = None

    if args.get(FLAG_RELEASE) and version is None:
        log("For a release a valid semantic version has to be set.")
        exit_process(EXIT_CODE_VERSION_IS_REQUIRED)
    elif args.get(FLAG_RELEASE) is False and version is None:
        latest_branch_version = _get_latest_branch_version()

        if not latest_branch_version:
            version = _Version(0, 0, 0, _get_dev_suffix(_get_current_branch()[0]))
        else:
            version = latest_branch_version
            # higher minor version and add dev suffix
            version.minor += 1
            # Set patch to 0 since its a new minor version
            version.patch = 0
            # Apply dev prefix
            version.suffix = _get_dev_suffix(_get_current_branch()[0])
    elif args.get(FLAG_RELEASE) is False and args.get(FLAG_FORCE) is False and version:
        version.suffix = _get_dev_suffix(_get_current_branch()[0])

    assert version is not None
    args[FLAG_VERSION] = version.to_string()

    args[_FLAG_SANITIZED] = True

    log("Sanatized Arguments: " + str(args))
    return DashInsensitiveDict(args)


def _load_from_env_variables(sanatized_args: dict, program_args: List[str]) -> dict:
    for argument in sanatized_args:
        if not isinstance(sanatized_args[argument], str):
            # Only load env variables for string variables
            continue

        if argument.replace("_", "-") in " ".join(program_args):
            # Argument was provided via command line arguments
            continue

        if os.environ.get(argument.upper()):
            sanatized_args[argument] = os.environ.get(argument.upper())

        if os.environ.get("INPUT_" + argument.upper()):
            # Support for github action inputs
            sanatized_args[argument] = os.environ.get("INPUT_" + argument.upper())

    return sanatized_args


def _concat_command_line_arguments(args: Dict[str, Union[str, bool, List[str]]]) -> str:
    command_line_arguments = ""

    for arg in args:
        arg_value = args[arg]  # getattr(args, arg)
        # Underscores must be converted back to dashes, since the
        # argparser initially transforms all dashes to underscores
        cli_arg_name = str(arg).replace("_", "-")
        if arg_value:
            # For boolean types, the existence of the flag is enough
            if type(arg_value) == bool:
                command_line_arguments += f" --{cli_arg_name}"
            elif isinstance(arg_value, list):
                for single_arg_value in arg_value:
                    command_line_arguments += f" --{cli_arg_name}={single_arg_value}"
            else:
                command_line_arguments += f" --{cli_arg_name}={arg_value}"

        command_line_arguments = command_line_arguments.lstrip()
    return command_line_arguments


def create_git_tag(
    version: str, push: bool = False, force: bool = False, exit_on_error: bool = False
) -> subprocess.CompletedProcess:
    """Create an annotated git tag in the current HEAD via `git tag` and the provided version.

    The version will be prefixed with 'v'.
    If push is set, the tag is pushed to remote but only if the previous `git tag` command was successful.

    Args:
        version (str): The tag to be created. Will be prefixed with 'v'.
        push (bool, optional): If true, push the tag to remote. Defaults to False.
        force (bool, optional): If true, force the tag to be created. Defaults to False.
        exit_on_error (bool): Exit program if the tag creation fails.

    Returns:
        subprocess.CompletedProcess: Returns the CompletedProcess object of either the `git tag` or the `git push tag` command. If `push` is set to true, the CompletedProcess of `git tag` is returned if it failed, otherwise the CompletedProcess object from the `git push tag` command is returned.
    """
    force_flag = "-f" if force else ""
    completed_process = run(
        f"git tag -a -m 'Automatically tagged during build process.' {force_flag} v{version}",
        disable_stderr_logging=True,
        exit_on_error=exit_on_error,
    )

    if completed_process.returncode > 0:
        log(
            f"Executing `git tag` for version v{version} might have a problem: {completed_process.stderr}"
        )

    if completed_process.returncode == 0 and push:
        completed_process = run(
            f"git push origin v{version}", exit_on_error=exit_on_error
        )

    return completed_process


def build(component_path: str, args: Dict[str, Union[str, bool, List[str]]]) -> None:
    """Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths.

    Args:
        component_path (str): The path of the component to be built. The path must contain a build.py file.
        args (Dict): The arguments to be passed to the component's build.py file. The default arguments that were used to call this
            script are passed down to the component.
    """

    if _is_path_skipped(component_path, args):
        return

    build_command = _create_build_cmd_from_args(component_path, args)
    completed_process = run(build_command, exit_on_error=False)

    if completed_process.returncode > 0:
        log(
            f"Failed to build module {component_path}. Code: {completed_process.returncode}."
        )
        exit_process(EXIT_CODE_GENERAL)


def run(  # type: ignore
    command: str,
    disable_stdout_logging: bool = False,
    disable_stderr_logging: bool = False,
    exit_on_error: bool = True,
    timeout: Optional[int] = None,
) -> subprocess.CompletedProcess:
    """Run a specified command.

    Args:
        command (str): The shell command that is executed via subprocess.Popen.
        disable_stdout_logging (bool): Disable stdout logging when it is too much or handled by the caller.
        exit_on_error (bool): Exit program if the exit code of the command is not 0.
        timeout (Optional[int]): If the process does not terminate after timeout seconds, raise a TimeoutExpired exception.

    Returns:
        subprocess.CompletedProcess: State
    """
    # Add timeout to command
    if timeout:
        command = f"timeout {timeout} {command}"
    log(f"Executing: {command}")

    with subprocess.Popen(  # type: ignore
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        try:
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
            exitcode = process.wait(timeout=timeout)
            process.stdout.close()
            process.stderr.close()

            if exit_on_error and exitcode != 0:
                exit_process(exitcode)

            return subprocess.CompletedProcess(
                args=command, returncode=exitcode, stdout=stdout, stderr=stderr
            )
        except Exception as ex:
            log(f"Exception during command run: {ex}")
            process.terminate()
            exit_process(1)


def exit_process(code: int = 0) -> None:
    """Exit the process with exit code.

    `sys.exit` seems to be a bit unreliable, process just sleeps and does not exit.
    So we are using os._exit instead and doing some manual cleanup.
    """
    import atexit
    import gc

    gc.collect()
    atexit._run_exitfuncs()
    sys.stdout.flush()
    os._exit(code)


def replace_in_files(
    find: str,
    replace: str,
    file_paths: List[str],
    regex: bool = False,
    exit_on_error: bool = True,
) -> None:
    """Replaces a string or regex occurence in a collection of files.

    Args:
        find (str): A string to find and replace in the files.
        replace (str): The string to replace it with.
        file_paths (List[str]): Collection of file paths.
        regex (bool, optional): If `True`, apply the find string as a regex notation. Defaults to `False`.
        exit_on_error (bool, optional): If `True`, exit process as soon as error occures. Defaults to True.
    """
    for file_path in file_paths:
        if not os.path.exists(file_path):
            log("File path does not exist for string replacement: " + file_path)
            if exit_on_error:
                exit_process(1)
        try:
            with open(file_path, "r+") as f:
                data = f.read()
                f.seek(0)
                if regex:
                    f.write(re.sub(find, replace, data))
                else:
                    f.write(data.replace(find, replace))
                f.truncate()
        except Exception as ex:
            log(
                "Failed to replace string in file: "
                + file_path
                + ". Exception: "
                + str(ex)
            )
            if exit_on_error:
                exit_process(1)


def get_latest_version() -> Optional[str]:
    """Returns the latest version based on Git tags."""
    try:
        latest_version = _get_latest_branch_version()
        assert latest_version is not None
        return latest_version.to_string()
    except Exception:
        return None


def duplicate_folder(
    src_path: str, target_path: str, exit_on_error: bool = True
) -> None:
    """Duplicate a folder into another folder.

    Args:
        src_path (str): Source path to duplicate.
        target_path (str): Target path to move the source folder.
            The existing content in the folder will be deleted.
        exit_on_error (bool, optional): If `True`, exit process as soon as error occures. Defaults to True.
    """
    try:
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.copytree(src_path, target_path)
    except Exception as ex:
        log("Failed to duplicate folder: " + str(ex))
        if exit_on_error:
            exit_process(1)


# Private functions


def _get_current_branch() -> Tuple[str, str]:
    """Get the current branch name and type (feature, production, release etc.) if existing.

    Returns:
        Tuple: (branchname, type)
    """
    full_branch_name = run(
        "git branch --show-current", disable_stdout_logging=True, exit_on_error=False
    ).stdout.rstrip("\n")
    if full_branch_name == "":
        full_branch_name = "HEAD"
    path_parts = full_branch_name.split("/")

    if len(path_parts) == 1:
        return (path_parts[0], "")

    # if a branch name consists of multiple slashes, the parts are concatenated; otherwise it just consists of the normal branch name
    # Example: "feature/foo/bar" -> (feature, foo-bar); "feature/foo" -> (feature, foo)
    merged_branch_name = "-".join(path_parts[1:])
    return (path_parts[0], merged_branch_name)


def _is_path_skipped(path: str, args: dict) -> bool:
    """Check whether the path is itself defined as a skip_path or is a sub-path of a skipped path.

    Args:
        path (str): The path to be checked
        args (dict): The cli arguments that might contain paths to be skipped. Sub-pathes of these skip-pathes will be skipped as well.

    Returns:
        bool: Return true if the path should be skipped
    """
    if _FLAG_SKIP_PATH not in args:
        return False

    skip_paths: list = args[_FLAG_SKIP_PATH]
    skip_paths = skip_paths or []
    real_path = os.path.realpath(path)
    for skip_path in skip_paths:
        real_skip_path = os.path.realpath(skip_path)
        if real_path == real_skip_path or real_path.startswith(real_skip_path + os.sep):
            return True
    return False


def _get_default_cli_arguments_parser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:

    # NEW FLAGS
    parser.add_argument(
        f"--{FLAG_MAKE}", help="Make/compile/package all artifacts", action="store_true"
    )
    parser.add_argument(
        f"--{FLAG_TEST}", help="Run unit and integration tests", action="store_true"
    )
    parser.add_argument(
        f"--{FLAG_CHECK}",
        help="Run linting and style checks.",
        action="store_true",
    )
    parser.add_argument(
        f"--{FLAG_RELEASE}",
        help="Release all artifacts (e.g. to  registries like DockerHub or NPM)",
        action="store_true",
    )
    parser.add_argument(
        f"--{FLAG_RUN}",
        help="Run the component in development mode (e.g. dev server).",
        action="store_true",
    )
    parser.add_argument(
        f"--{FLAG_VERSION}", help="Version of the build (`MAJOR.MINOR.PATCH-TAG`)"
    )
    parser.add_argument(
        f"--{FLAG_FORCE}",
        help="Ignore all enforcements and warnings.",
        action="store_true",
    )
    parser.add_argument(
        "--" + _FLAG_SKIP_PATH.replace("_", "-"),
        help="Skips the build phases for all (sub)paths provided here",
        action="append",
    )
    parser.add_argument(
        "--" + FLAG_TEST_MARKER.replace("_", "-"),
        help="Provide custom markers for testing. The default marker for slow tests is `slow`.",
        action="append",
    )
    parser.add_argument(
        f"--{_FLAG_SANITIZED}",
        help="Indicates that a parent build.py script already checked the validity of the passed arguments so that subsequent scripts don't do it again.",
        action="store_true",
    )

    return parser


def _create_build_cmd_from_args(module_path: str, sanitized_args: dict) -> str:
    build_command = f"{sys.executable} -u build.py " + _concat_command_line_arguments(
        sanitized_args
    )

    working_dir = os.getcwd()
    full_command = (
        "cd '" + module_path + "' && " + build_command + " && cd '" + working_dir + "'"
    )
    log("Building " + module_path + " with: " + full_command)
    return full_command


def _is_valid_command_combination(args: dict) -> bool:
    if (
        args.get(FLAG_RELEASE)
        and not args.get(FLAG_VERSION)
        and not args.get(FLAG_FORCE)
    ):
        log(
            f"Please provide a version for deployment (--{FLAG_VERSION}=MAJOR.MINOR.PATCH-TAG)"
        )
        return False
    if args.get(FLAG_RELEASE) and not args.get(FLAG_TEST) and not args.get(FLAG_FORCE):
        log(f"The release steps requires test to be executed (--{FLAG_TEST})")
        return False
    if args.get(FLAG_RELEASE) and not args.get(FLAG_MAKE) and not args.get(FLAG_FORCE):
        log(f"The release steps requires make to be executed (--{FLAG_MAKE})")
        return False

    if args.get(FLAG_RELEASE):
        current_branch, current_branch_type = _get_current_branch()
        if (
            current_branch.lower() not in _MAIN_BRANCH_NAMES
            and current_branch_type.lower() not in _ALLOWED_BRANCH_TYPES_FOR_RELEASE
            and not args.get(FLAG_FORCE)
        ):
            log(
                f"Release is only allowed from branches: [{', '.join(_MAIN_BRANCH_NAMES)}] or in branch types: [{', '.join(_ALLOWED_BRANCH_TYPES_FOR_RELEASE)}]"
            )
            return False

    return True


def _get_version_tags() -> List["_Version"]:
    unformatted_tags = _get_remote_git_tags()
    versions = []
    for tag in unformatted_tags:
        tag_parts = tag.split("/")
        tag = tag_parts[-1]
        # only consider tags that resemble versions
        version = _Version.get_version_from_string(tag)
        if version is not None:
            versions.append(version)
    return versions


def _get_latest_branch_version() -> Optional[_Version]:
    result = run(
        "git describe --tags --match 'v[0-9].*' --abbrev=0",
        disable_stdout_logging=True,
        exit_on_error=False,
    )

    return _Version.get_version_from_string(result.stdout.rstrip("\n"))


def _get_remote_git_tags() -> List[str]:
    if not os.getenv("GITHUB_TOKEN"):
        # if no github token is set, don't try to get the tags from remote
        return []

    result = run(
        "git ls-remote --tags --sort='-v:refname' --refs",
        disable_stdout_logging=True,
        exit_on_error=False,
    )
    return result.stdout.rstrip("\n").split("\n")


def _get_version(
    version: str, force: bool = False, existing_versions: List[_Version] = []
) -> _Version:
    """Get validated version. If force is set to True, the version is allowed to be equal or smaller than the existing patch version.

    Raises:
        _VersionInvalidFormatException: Raised when the provided version's format is not valid
        Exception: Raised when no version is passed

    Args:
        version (str): The version to be checked for validity. It will be tried to be transformed into a build_utils.Version object.
        force (bool, optional): If set tu true, the version can be equal or smaller than existing patch version version numbers
        existing_versions (list, optional): The list of versions to be checked against

    Returns:
        Version: Validated version
    """
    provided_version = version

    if not provided_version:
        raise Exception("No version is provided")

    version_obj = _Version.get_version_from_string(provided_version)
    if version_obj is None:
        raise _VersionInvalidFormatException(
            "The provided version {provided_version} is not in a valid format. Valid formats include 1.0.0, 1.0.0-dev or 1.0.0-dev.foo"
        )
    for existing_version in existing_versions:
        if (
            existing_version.major == version_obj.major
            and existing_version.minor == version_obj.minor
            and existing_version.patch >= version_obj.patch
            and existing_version.suffix
            == ""  # Only consider release versions, not suffixed dev versions
            and not force
        ):
            raise _VersionInvalidFormatException(
                f"A version ({existing_version.to_string()}) with the same or higher patch version as provided ({version_obj.to_string()}) already exists."
            )
    return version_obj


def _get_current_branch_version(
    existing_versions: List[_Version] = [],
) -> Tuple[Optional[_Version], List[_Version]]:
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


def _get_dev_suffix(branch_name: Optional[str]) -> str:
    branch_name = branch_name or ""
    return "dev." + branch_name


class _VersionInvalidFormatException(Exception):
    """Raised when the provided version's format is not valid."""

    pass

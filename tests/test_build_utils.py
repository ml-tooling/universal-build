from typing import Tuple, Optional
from universal_build import build_utils
import pytest
import sys

valid_patch_version = "1.1.4"
valid_minor_version = "2.2.0"


def _mocked_get_remote_git_tags() -> list:
    return ["1.0.0", "1.1.3", "2.1.0", "1.2.0-dev.foo-branch", "1.0.0-dev"]


def exit_process(code: int = 0):
    sys.exit(code)


build_utils._get_remote_git_tags = _mocked_get_remote_git_tags
build_utils.exit_process = exit_process


def mock_branch(branch_name: str, branch_type: str = ""):
    def _mocked_get_current_branch() -> Tuple[str, str]:
        return (branch_name, branch_type)

    build_utils._get_current_branch = _mocked_get_current_branch


class TestGetVersionClass:
    def test_correct_semantic_patch_version(self):
        valid_version = build_utils._get_version(valid_patch_version)
        assert isinstance(valid_version, build_utils.Version)
        version_split = valid_patch_version.split(".")
        assert (
            valid_version.major == version_split[0]
            and valid_version.minor == version_split[1]
            and valid_version.patch == version_split[2]
            and not valid_version.suffix
        )

    def test_correct_semantic_minor_version(self):
        valid_version = build_utils._get_version(valid_minor_version)
        assert isinstance(valid_version, build_utils.Version)
        version_split = valid_minor_version.split(".")
        assert (
            valid_version.major == version_split[0]
            and valid_version.minor == version_split[1]
            and valid_version.patch == version_split[2]
            and not valid_version.suffix
        )

    def test_no_semantic_version(self):
        with pytest.raises(Exception):
            build_utils._get_version("foobar")

    def test_with_too_small_patch(self):
        with pytest.raises(Exception):
            build_utils._get_version("1.1.2")


class TestBuildClass:
    def test_release_without_version(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(["--release"])

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_release_in_feature_branch(self):
        mock_branch("foobar")
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(
                ["--release", "--test", "--make", "--version=foo"]
            )

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_release_with_invalid_version_in_main_branch(self):
        mock_branch("main")
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(
                ["--release", "--test", "--make", "--version=foo"]
            )

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_release_with_already_existing_version(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(
                ["--release", "--test", "--make", "--version 1.0.0"]
            )

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_release(self):

        sanitized_arguments = build_utils.get_sanitized_arguments(
            ["--release", "--test", "--make", f"--version={valid_patch_version}"]
        )
        assert isinstance(sanitized_arguments["version"], str)
        assert sanitized_arguments["version"] == valid_patch_version

    def test_build_with_dev_tag_in_branch(self):
        mock_branch("foo-branch", "feature")

        sanitized_args = build_utils.get_sanitized_arguments()
        assert sanitized_args["version"] == "1.2.0-dev.foo-branch"

    def test_build_with_no_dev_tag_in_branch(self):
        mock_branch("bar-branch", "feature")

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments()

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 3

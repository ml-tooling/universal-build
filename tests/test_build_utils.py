from typing import Tuple
from universal_build import build_utils
import pytest
import sys

from universal_build.build_utils import (
    VersionInvalidFormatException,
    VersionInvalidPatchNumber,
)

valid_patch_version = "1.1.4"
valid_minor_version = "2.2.0"


def _mocked_get_remote_git_tags() -> list:
    return sorted(
        ["1.0.0", "1.1.3", "2.1.0", "1.2.0-dev.foo-branch", "1.0.0-dev"], reverse=True
    )


def exit_process(code: int = 0):
    sys.exit(code)


build_utils._get_remote_git_tags = _mocked_get_remote_git_tags
build_utils.exit_process = exit_process


def mock_branch(branch_name: str = "main", branch_type: str = ""):
    """Override the build_utils._get_current_branch method since the test might not run in a git repository.

    Args:
        branch_name (str, optional): Name of the branch the `_get_current_branch` method should return. Defaults to "main".
        branch_type (str, optional): Type of the branch the `_get_current_branch` method should return. Defaults to "".
    """

    def _mocked_get_current_branch() -> Tuple[str, str]:
        return (branch_name, branch_type)

    build_utils._get_current_branch = _mocked_get_current_branch


def mock_version(version: str = "v1.1.0", suffix: str = ""):
    """Override the build_utils._get_latest_branch_version method since the test might not run in a git repository.

    Args:
        version (str, optional): The version that should be returned as the latest version tag. Defaults to "v1.1.0".
        suffix (str, optional): A suffix that is appended to version in the form of `-${suffix}`. Defaults to "".
    """

    version = version if suffix == "" else f"{version}-{suffix}"

    def _mocked_get_latest_branch_version() -> "Version":
        return build_utils.Version.get_version_from_string(version)

    build_utils._get_latest_branch_version = _mocked_get_latest_branch_version


# Default version override
mock_version()


class TestGetVersionClass:
    def setup_method(self):
        """" Runs before each function. """
        mock_branch()
        mock_version()

    def test_correct_semantic_patch_version(self):
        valid_version = build_utils._get_version(
            valid_patch_version, existing_versions=build_utils._get_version_tags()
        )
        assert isinstance(valid_version, build_utils.Version)
        version_split = valid_patch_version.split(".")
        assert (
            valid_version.major == version_split[0]
            and valid_version.minor == version_split[1]
            and valid_version.patch == version_split[2]
            and not valid_version.suffix
        )

    def test_correct_semantic_minor_version(self):
        valid_version = build_utils._get_version(
            valid_minor_version, existing_versions=build_utils._get_version_tags()
        )
        assert isinstance(valid_version, build_utils.Version)
        version_split = valid_minor_version.split(".")
        assert (
            valid_version.major == version_split[0]
            and valid_version.minor == version_split[1]
            and valid_version.patch == version_split[2]
            and not valid_version.suffix
        )

    def test_no_semantic_version(self):
        with pytest.raises(VersionInvalidFormatException) as pytest_wrapped_e:
            build_utils._get_version(
                "foobar", existing_versions=build_utils._get_version_tags()
            )

        assert pytest_wrapped_e.type is VersionInvalidFormatException

    def test_with_too_small_patch(self):
        too_small_patch_version = "1.1.2"
        with pytest.raises(VersionInvalidPatchNumber) as pytest_wrapped_e:
            build_utils._get_version(
                version=too_small_patch_version,
                existing_versions=build_utils._get_version_tags(),
            )
        assert pytest_wrapped_e.type is VersionInvalidPatchNumber

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(
                [f"--{build_utils.FLAG_VERSION}={too_small_patch_version}"]
            )

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_INVALID_VERSION

    def test_version_formats(self):
        git_tags = ["1.0.0", "1.0.0-dev", "1.0.0-dev.foo", "v1.0.0", "v1.0.0-dev"]
        invalid_git_tags = ["f1.0.0", "f1.0.0-dev-foo"]
        validated_tags = []
        for tag in git_tags:
            version = build_utils.Version.get_version_from_string(tag)
            if version == None:
                continue
            validated_tags.append(version)

        for tag in invalid_git_tags:
            version = build_utils.Version.get_version_from_string(tag)
            if version == None:
                continue
            validated_tags.append(version)

        assert len(validated_tags) == len(git_tags)


class TestBuildClass:
    def setup_method(self):
        """" Runs before each function. """
        mock_branch()
        mock_version()

    def test_release_without_version(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments([f"--{build_utils.FLAG_RELEASE}"])

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_INVALID_ARGUMENTS

    def test_release_with_invalid_version_in_main_branch(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(
                [
                    f"--{build_utils.FLAG_RELEASE}",
                    f"--{build_utils.FLAG_TEST}",
                    f"--{build_utils.FLAG_MAKE}",
                    f"--{build_utils.FLAG_VERSION}=foo",
                ]
            )

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_INVALID_VERSION

    def test_release_with_already_existing_version(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments(
                [
                    f"--{build_utils.FLAG_RELEASE}",
                    f"--{build_utils.FLAG_TEST}",
                    f"--{build_utils.FLAG_MAKE}",
                    f"--{build_utils.FLAG_VERSION}=1.0.0",
                ]
            )

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_INVALID_VERSION

    def test_release(self):
        sanitized_arguments = build_utils.get_sanitized_arguments(
            [
                f"--{build_utils.FLAG_RELEASE}",
                f"--{build_utils.FLAG_TEST}",
                f"--{build_utils.FLAG_MAKE}",
                f"--{build_utils.FLAG_VERSION}={valid_patch_version}",
            ]
        )
        assert isinstance(sanitized_arguments[build_utils.FLAG_VERSION], str)
        assert sanitized_arguments[build_utils.FLAG_VERSION] == valid_patch_version

    def test_build_with_dev_tag_in_branch(self):
        branch_name = "foo-branch"
        mock_branch(branch_name, "feature")
        mock_version("v1.2.0", suffix=build_utils._get_dev_suffix(branch_name))

        sanitized_args = build_utils.get_sanitized_arguments([f"--{build_utils.FLAG_MAKE}"])
        assert sanitized_args[build_utils.FLAG_VERSION] == "1.2.0-dev.foo-branch"

    def test_build_with_wrong_dev_tag_in_branch(self):
        branch_name = "foo-branch"
        mock_branch(branch_name, "feature")
        mock_version("v1.2.0", suffix=build_utils._get_dev_suffix("bar-branch"))

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments([f"--{build_utils.FLAG_MAKE}"])

        assert pytest_wrapped_e.type == SystemExit
        assert (
            pytest_wrapped_e.value.code
            == build_utils.EXIT_CODE_DEV_VERSION_NOT_MATCHES_BRANCH
        )

    def test_build_with_release_tag_in_branch(self):
        branch_name = "foo-branch"
        mock_branch(branch_name, "feature")

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments([f"--{build_utils.FLAG_MAKE}"])

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_DEV_VERSION_REQUIRED

    def test_build_with_force_without_version(self):
        sanitized_args = build_utils.get_sanitized_arguments(
            [f"--{build_utils.FLAG_MAKE}", f"--{build_utils.FLAG_FORCE}"]
        )
        assert sanitized_args[build_utils.FLAG_VERSION] == "1.1.0"

    def test_build_without_version_and_no_dev_tag_in_branch(self):
        mock_branch("bar-branch", "feature")

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.get_sanitized_arguments([f"--{build_utils.FLAG_MAKE}"])

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_DEV_VERSION_REQUIRED

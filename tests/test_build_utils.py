import os
import sys
from typing import Tuple

import pytest

from universal_build import build_utils

valid_patch_version = "1.1.4"
valid_minor_version = "2.2.0"


def setup_module(module):
    build_utils._get_remote_git_tags = _mocked_get_remote_git_tags
    build_utils.exit_process = _mocked_exit_process
    build_utils._get_current_branch = _mocked_get_current_branch
    build_utils._get_latest_branch_version = _mocked_get_latest_branch_version


class TestGetVersionClass:
    def test_correct_semantic_patch_version(self):
        valid_version = build_utils._get_version(
            valid_patch_version, existing_versions=build_utils._get_version_tags()
        )
        assert isinstance(valid_version, build_utils._Version)
        version_split = valid_patch_version.split(".")
        assert (
            valid_version.major == int(version_split[0])
            and valid_version.minor == int(version_split[1])
            and valid_version.patch == int(version_split[2])
            and not valid_version.suffix
        )

    def test_correct_semantic_minor_version(self):
        valid_version = build_utils._get_version(
            valid_minor_version, existing_versions=build_utils._get_version_tags()
        )
        assert isinstance(valid_version, build_utils._Version)
        version_split = valid_minor_version.split(".")
        assert (
            valid_version.major == int(version_split[0])
            and valid_version.minor == int(version_split[1])
            and valid_version.patch == int(version_split[2])
            and not valid_version.suffix
        )

    def test_no_semantic_version(self):
        with pytest.raises(
            build_utils._VersionInvalidFormatException
        ) as pytest_wrapped_e:
            build_utils._get_version(
                "foobar", existing_versions=build_utils._get_version_tags()
            )

        assert pytest_wrapped_e.type is build_utils._VersionInvalidFormatException

    # TODO: the version check uses force has default for dev builds now
    # def test_with_too_small_patch(self):
    #     too_small_patch_version = "1.1.2"
    #     with pytest.raises(
    #         build_utils._VersionInvalidFormatException
    #     ) as pytest_wrapped_e:
    #         build_utils._get_version(
    #             version=too_small_patch_version,
    #             existing_versions=build_utils._get_version_tags(),
    #         )
    #     assert pytest_wrapped_e.type is build_utils._VersionInvalidFormatException

    #     with pytest.raises(SystemExit) as pytest_wrapped_e:
    #         build_utils.parse_arguments(
    #             [f"--{build_utils.FLAG_VERSION}={too_small_patch_version}"]
    #         )

    #     assert pytest_wrapped_e.type == SystemExit
    #     assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_INVALID_VERSION

    def test_version_formats(self):
        git_tags = ["1.0.0", "1.0.0-dev", "1.0.0-dev.foo", "v1.0.0", "v1.0.0-dev"]
        invalid_git_tags = ["f1.0.0", "f1.0.0-dev-foo"]
        validated_tags = []
        for tag in git_tags:
            version = build_utils._Version.get_version_from_string(tag)
            if version is None:
                continue
            validated_tags.append(version)

        for tag in invalid_git_tags:
            version = build_utils._Version.get_version_from_string(tag)
            if version is None:
                continue
            validated_tags.append(version)

        assert len(validated_tags) == len(git_tags)


class TestBuildClass:
    def test_release_without_version(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.parse_arguments([f"--{build_utils.FLAG_RELEASE}"])

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == build_utils.EXIT_CODE_INVALID_ARGUMENTS

    def test_release_with_invalid_version_in_main_branch(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            build_utils.parse_arguments(
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
            build_utils.parse_arguments(
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
        sanitized_arguments = build_utils.parse_arguments(
            [
                f"--{build_utils.FLAG_RELEASE}",
                f"--{build_utils.FLAG_TEST}",
                f"--{build_utils.FLAG_MAKE}",
                f"--{build_utils.FLAG_VERSION}={valid_patch_version}",
            ]
        )
        assert isinstance(sanitized_arguments[build_utils.FLAG_VERSION], str)
        assert sanitized_arguments[build_utils.FLAG_VERSION] == valid_patch_version

    def test_build_with_force_with_version(self):
        sanitized_args = build_utils.parse_arguments(
            [
                f"--{build_utils.FLAG_MAKE}",
                f"--{build_utils.FLAG_FORCE}",
                "--version=1.1.0",
            ]
        )
        assert sanitized_args[build_utils.FLAG_VERSION] == "1.1.0"

    @pytest.mark.parametrize(
        "args",
        [{"test": True}, {"test_2": True}, {"test-3": True}],
    )
    def test_concat_command_line_arguments_arg(self, args: dict):
        cli_args = build_utils._concat_command_line_arguments(args)
        assert "_" not in cli_args
        arg, arg_value = args.popitem()
        if "_" not in arg:
            assert f"--{arg}" == cli_args

    @pytest.mark.parametrize(
        "args",
        [
            {"test": True},
            {"docker_image_prefix": "test"},
            {"skip_path": ["awesome-frontend"]},
            {"skip_path2": ["awesome-frontend", "awesome-backend"]},
            {"pypi_token": False},
        ],
    )
    def test_concat_command_line_arguments_arg_value(self, args: dict):
        cli_args = build_utils._concat_command_line_arguments(args)
        arg, arg_value = args.popitem()

        if arg == "test":
            assert cli_args == "--test"

        if arg == "docker_image_prefix":
            assert cli_args == "--docker-image-prefix=test"

        if arg == "skip_path":
            assert cli_args == "--skip-path=awesome-frontend"

        if arg == "skip_path2":
            assert (
                cli_args == "--skip-path2=awesome-frontend --skip-path2=awesome-backend"
            )

        if arg == "pypi_token":
            assert not cli_args

    @pytest.mark.parametrize(
        "cli_args_string",
        [
            "--my_token=111 --deployment-token=666 --my_bool",
            "--my_token=111 --deployment-token 666 --my_bool",
            "--my_token 111 --deployment-token 666 --my_bool",
        ],
    )
    def test_arguments_passed_to_submodule(self, cli_args_string: str):
        """Tests whether the cli args passed to a module will be passed
        in the same way to a submodule. The reason is that the argparser
        converts all dashes to underscores.
        """
        HERE = os.path.abspath(os.path.dirname(__file__))
        build_file_path = os.path.join(HERE, "build.py")

        completed_process = build_utils.run(
            f"python -u {build_file_path} {cli_args_string}",
            exit_on_error=False,
        )
        assert completed_process.returncode == 0

    def test_arguments_passed_as_env_to_submodule(self):
        """Tests whether the args passed as env variables to a module correctly to submodules."""
        HERE = os.path.abspath(os.path.dirname(__file__))
        build_file_path = os.path.join(HERE, "build.py")

        completed_process = build_utils.run(
            f"MY_TOKEN=111 python -u {build_file_path} --deployment-token 666 --my_bool",
            exit_on_error=False,
        )
        assert completed_process.returncode == 0

    @pytest.mark.parametrize(
        "cli_args_string",
        [
            "--my-token=111 --deployment-token=666 --my_bool",
            "--my_token=111 --deployment_token 666 --my_bool",
            "--my_token 111 --deployment-token 666 --my-bool",
        ],
    )
    def test_arguments_passed_to_submodule_error(self, cli_args_string: str):
        """Tests whether the cli args passed to a module will be passed in the same way to a submodule. The reason is that the argparser converts all dashes to underscores."""
        HERE = os.path.abspath(os.path.dirname(__file__))
        build_file_path = os.path.join(HERE, "build.py")
        completed_process = build_utils.run(
            f"python -u {build_file_path} --my-token=111 --deployment-token=666 --my_bool",
            exit_on_error=False,
        )
        assert completed_process.returncode != 0


def _mocked_get_remote_git_tags() -> list:
    return sorted(
        ["1.0.0", "1.1.3", "2.1.0", "1.2.0-dev.foo-branch", "1.0.0-dev"], reverse=True
    )


def _mocked_exit_process(code: int = 0):
    sys.exit(code)


def _mocked_get_current_branch(
    branch_name: str = "main", branch_type: str = ""
) -> Tuple[str, str]:
    return (branch_name, branch_type)


def _mocked_get_latest_branch_version(
    version: str = "v1.1.0", suffix: str = ""
) -> build_utils._Version:
    version = version if suffix == "" else f"{version}-{suffix}"
    return build_utils._Version.get_version_from_string(version)

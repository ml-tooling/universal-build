"""Utilities to help building Docker images."""

import argparse
import os
import subprocess
from typing import List

from universal_build import build_utils

FLAG_DOCKER_IMAGE_PREFIX = "docker_image_prefix"


def parse_arguments(
    input_args: List[str] = None, argument_parser: argparse.ArgumentParser = None
) -> dict:
    """Parses all arguments and returns a sanitized & augmented list of arguments.

    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Args:
        input_args (List[str], optional): List of arguments that are used instead of the arguments passed to the process. Defaults to `None`.
        argument_parser (arparse.ArgumentParser, optional): An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones.

    Returns:
        dict: The parsed default arguments thar are already checked for validity.
    """
    if argument_parser is None:
        argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--" + FLAG_DOCKER_IMAGE_PREFIX.replace("_", "-"),
        help="Provide a prefix for a Docker image, e.g. 'mltooling/' or even a repository path. When leaving blank, the default Dockerhub Repository is used.",
        required=False,
        default="",
    )

    return build_utils.parse_arguments(
        input_args=input_args, argument_parser=argument_parser
    )


def check_image(image: str, trivy: bool = True, exit_on_error: bool = True) -> None:
    """Run vulnerability checks on Dockerimage.

    Args:
        image (str): The name of the docker image to check.
        trivy (bool, optional): Activate trivy vulnerability check. Defaults to `True`.
        exit_on_error (bool, optional): If `True`, exit process as soon as an error occurs.
    """
    build_utils.log("Run vulnerability checks on docker image:")

    if trivy and build_utils.command_exists("trivy", exit_on_error=exit_on_error):
        build_utils.run(
            f"trivy image --timeout=20m0s --exit-code 1 --severity HIGH,CRITICAL {image}",
            exit_on_error=exit_on_error,
        )

    # TODO: Implement dockl container scan


def lint_dockerfile(hadolint: bool = True, exit_on_error: bool = True) -> None:
    """Run hadolint on the Dockerfile.

    Args:
        hadolint (bool, optional): Activate hadolint dockerfile linter. Defaults to `True`.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    build_utils.log("Run linters and style checks:")

    if hadolint and build_utils.command_exists("hadolint", exit_on_error=exit_on_error):
        config_file_arg = ""
        if os.path.exists(".hadolint.yml"):
            config_file_arg = "--config=.hadolint.yml"

        build_utils.run(
            f"hadolint {config_file_arg} Dockerfile", exit_on_error=exit_on_error
        )


def get_image_name(name: str, tag: str, image_prefix: str = "") -> str:
    """Get a valid versioned image name.

    Args:
        name (str): Name of the docker image.
        tag (str): Version to use for the tag.
        image_prefix (str, optional): The prefix added to the name to indicate an organization on DockerHub or a completely different repository.

    Returns:
        str: a valid docker image name based on: prefix/name:tag
    """
    versioned_tag = name.strip() + ":" + tag.strip()
    if image_prefix:
        versioned_tag = image_prefix.strip().rstrip("/") + "/" + versioned_tag
    return versioned_tag


def build_docker_image(
    name: str,
    version: str,
    build_args: str = "",
    docker_image_prefix: str = "",
    exit_on_error: bool = True,
) -> subprocess.CompletedProcess:
    """Build a docker image from a Dockerfile in the working directory.

    Args:
        name (str): Name of the docker image.
        version (str): Version to use as tag.
        build_args (str, optional): Add additional build arguments for docker build.
        docker_image_prefix (str, optional): The prefix added to the name to indicate an organization on DockerHub or a completely different repository.
        exit_on_error (bool, optional): If `True`, exit process as soon as an error occurs.

    Returns:
        subprocess.CompletedProcess: Returns the CompletedProcess object of the
    """
    # Check if docker exists on the system
    build_utils.command_exists("docker", exit_on_error=exit_on_error)

    versioned_tag = get_image_name(name=name, tag=version)
    latest_tag = get_image_name(name=name, tag="latest")
    completed_process = build_utils.run(
        "docker build -t "
        + versioned_tag
        + " -t "
        + latest_tag
        + " "
        + build_args
        + " ./",
        exit_on_error=exit_on_error,
    )

    if completed_process.returncode > 0:
        build_utils.log(f"Failed to build Docker image {versioned_tag}")
        return completed_process

    if docker_image_prefix:
        remote_versioned_tag = get_image_name(
            name=name, tag=version, image_prefix=docker_image_prefix
        )
        build_utils.run(
            "docker tag " + versioned_tag + " " + remote_versioned_tag,
            exit_on_error=exit_on_error,
        )

    return completed_process


def release_docker_image(
    name: str, version: str, docker_image_prefix: str, exit_on_error: bool = True
) -> subprocess.CompletedProcess:
    """Push a Docker image to a repository.

    Args:
        name (str): The name of the image. Must not be prefixed!
        version (str): The tag used for the image.
        docker_image_prefix (str): The prefix added to the name to indicate an organization on DockerHub or a completely different repository.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.

    Returns:
        subprocess.CompletedProcess: Returns the CompletedProcess object of the `docker push ...` command.
    """
    # Check if docker exists on the system
    build_utils.command_exists("docker", exit_on_error=exit_on_error)

    if not docker_image_prefix:
        build_utils.log(
            "The flag --docker-image-prefix cannot be blank when pushing a Docker image."
        )
        build_utils.exit_process(build_utils.EXIT_CODE_GENERAL)

    versioned_tag = get_image_name(name=name, tag=version)
    remote_versioned_tag = get_image_name(
        name=name, tag=version, image_prefix=docker_image_prefix
    )
    build_utils.run(
        "docker tag " + versioned_tag + " " + remote_versioned_tag,
        exit_on_error=exit_on_error,
    )
    completed_process = build_utils.run(
        "docker push " + remote_versioned_tag, exit_on_error=exit_on_error
    )

    if completed_process.returncode > 0:
        build_utils.log(f"Failed to release Docker image {name}:{version}")

    # Only push version with latest tag if no suffix is added (pre-release)
    if "-" not in version:
        remote_latest_tag = get_image_name(
            name=name, tag="latest", image_prefix=docker_image_prefix
        )

        build_utils.log(
            "Release Docker image with latest tag as well: " + remote_latest_tag
        )

        build_utils.run(
            "docker tag " + versioned_tag + " " + remote_latest_tag,
            exit_on_error=exit_on_error,
        )
        build_utils.run("docker push " + remote_latest_tag, exit_on_error=exit_on_error)

    return completed_process

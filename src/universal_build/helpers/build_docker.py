import argparse
import subprocess
from typing import Dict, List, Union

from universal_build import build_utils

FLAG_DOCKER_IMAGE_PREFIX = "docker_image_prefix"


def get_sanitized_arguments(
    arguments: List[str] = None, argument_parser: argparse.ArgumentParser = None
) -> Dict[str, Union[str, bool, List[str]]]:
    """Return sanitized default arguments when they are valid.

    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Args:
        arguments (List[str], optional): List of arguments that are used instead of the arguments passed to the process. Defaults to `None`.
        argument_parser (arparse.ArgumentParser, optional): An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. Must be initialized with `add_help=False` flag like argparse.ArgumentParser(add_help=False)!

    Returns:
        Dict[str, Union[str, bool, List[str]]]: The parsed default arguments thar are already checked for validity.
    """
    if argument_parser is None:
        argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--" + FLAG_DOCKER_IMAGE_PREFIX.replace("_", "-"),
        help="With this flag you can provide a prefix for a Docker image, e.g. 'mltooling/' or even a repository path. When leaving blank, the default Dockerhub Repository is used.",
        required=False,
        default=None,
    )

    return build_utils.get_sanitized_arguments(
        arguments=arguments, argument_parser=argument_parser
    )


def build_docker_image(
    name: str, version: str, build_args: str = "", exit_on_error: bool = False
) -> subprocess.CompletedProcess:
    versioned_image = name + ":" + version
    latest_image = name + ":latest"
    completed_process = build_utils.run(
        "docker build -t "
        + versioned_image
        + " -t "
        + latest_image
        + " "
        + build_args
        + " ./",
        exit_on_error=exit_on_error,
    )

    # TODO tag prefixed image names

    if completed_process.returncode > 0:
        build_utils.log(f"Failed to build Docker image {name}:{version}")

    return completed_process


def release_docker_image(
    name: str, version: str, docker_image_prefix: str = "", exit_on_error: bool = False
) -> subprocess.CompletedProcess:
    """Push a Docker image to a repository.

    Args:
        name (str): The name of the image. Must not be prefixed!
        version (str): The tag used for the image.
        docker_image_prefix (str, optional): The prefix added to the name to indicate an organization on DockerHub or a completely different repository. Defaults to "".
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.

    Returns:
        subprocess.CompletedProcess: Returns the CompletedProcess object of the `docker push ...` command.
    """
    if not docker_image_prefix:
        build_utils.log(
            "The flag --docker-image-prefix cannot be blank when pushing a Docker image."
        )
        build_utils.exit_process(build_utils.EXIT_CODE_GENERAL)

    versioned_image = name + ":" + version
    remote_versioned_image = docker_image_prefix + versioned_image
    build_utils.run(
        "docker tag " + versioned_image + " " + remote_versioned_image,
        exit_on_error=exit_on_error,
    )
    completed_process = build_utils.run(
        "docker push " + remote_versioned_image, exit_on_error=exit_on_error
    )

    if completed_process.returncode > 0:
        build_utils.log(f"Failed to release Docker image {name}:{version}")

    if "-dev" not in version:
        build_utils.log("Release Docker image with latest tag as well.")
        latest_image = name + ":latest"
        remote_latest_image = docker_image_prefix + latest_image
        build_utils.run(
            "docker tag " + latest_image + " " + remote_latest_image,
            exit_on_error=exit_on_error,
        )
        build_utils.run(
            "docker push " + remote_latest_image, exit_on_error=exit_on_error
        )

    return completed_process

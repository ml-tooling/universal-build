import subprocess

from universal_build import build_utils


def build_docker_image(
    name: str, version: str, build_args: str = ""
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
        + " ./"
    )

    if completed_process.returncode > 0:
        build_utils.log(f"Failed to build Docker image {name}:{version}")

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
        build_utils.log(
            "The flag --docker-image-prefix cannot be blank when pushing a Docker image."
        )
        build_utils.exit_process(build_utils.EXIT_CODE_GENERAL)

    versioned_image = name + ":" + version
    remote_versioned_image = docker_image_prefix + versioned_image
    build_utils.run("docker tag " + versioned_image + " " + remote_versioned_image)
    completed_process = build_utils.run("docker push " + remote_versioned_image)

    if completed_process.returncode > 0:
        build_utils.log(f"Failed to release Docker image {name}:{version}")

    if "-dev" not in version:
        build_utils.log("Release Docker image with latest tag as well.")
        latest_image = name + ":latest"
        remote_latest_image = docker_image_prefix + latest_image
        build_utils.run("docker tag " + latest_image + " " + remote_latest_image)
        build_utils.run("docker push " + remote_latest_image)

    return completed_process

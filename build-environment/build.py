import os

from universal_build import build_utils
from universal_build.helpers import build_docker

COMPONENT_NAME = "build-environment"
DOCKER_IMAGE_PREFIX = "mltooling"

HERE = os.path.abspath(os.path.dirname(__file__))


def main(args: dict) -> None:
    # set current path as working dir
    os.chdir(HERE)

    version = args.get(build_utils.FLAG_VERSION)
    docker_image_prefix = DOCKER_IMAGE_PREFIX
    if args.get(build_docker.FLAG_DOCKER_IMAGE_PREFIX):
        docker_image_prefix = args.get(
            build_docker.FLAG_DOCKER_IMAGE_PREFIX
        )  # type: ignore

    if args.get(build_utils.FLAG_MAKE):
        build_docker.build_docker_image(COMPONENT_NAME, version, exit_on_error=True)

    if args.get(build_utils.FLAG_CHECK):
        build_docker.lint_dockerfile(exit_on_error=False)

        exit_on_error = False if build_utils.FLAG_FORCE else True
        completed_process = build_docker.check_image(
            image=build_docker.get_image_name(name=COMPONENT_NAME, tag=version),
            exit_on_error=exit_on_error,
        )
        if completed_process and completed_process.returncode != 0:
            build_utils.log(
                f"The security check failed, but is ignored because {build_utils.FLAG_FORCE} flag is set."
            )

    if args.get(build_utils.FLAG_RELEASE):
        build_docker.release_docker_image(
            COMPONENT_NAME, version, docker_image_prefix, exit_on_error=True
        )


if __name__ == "__main__":
    main(build_docker.parse_arguments())

import glob
import os
import shutil

from universal_build import build_utils

HERE = os.path.abspath(os.path.dirname(__file__))

REACT_WEBAPP_COMPONENT = "react-webapp"
DOCS_COMPONENT = "docs"
PYTHON_LIB_COMPONENT = "python-lib"
DOCKER_COMPONENT = "docker"


def main(args: dict) -> None:
    """Execute all component builds."""

    # set script path as working dir
    os.chdir(HERE)

    # Build react webapp
    build_utils.build(REACT_WEBAPP_COMPONENT, args)
    # Build python lib
    build_utils.build(PYTHON_LIB_COMPONENT, args)

    if args.get(build_utils.FLAG_MAKE):
        # Duplicate api docs into the mkdocs documentation
        build_utils.duplicate_folder(
            f"./{PYTHON_LIB_COMPONENT}/docs/", f"./{DOCS_COMPONENT}/docs/api-docs/"
        )

        # Copy python lib distribution to docker container
        try:
            dest_path = os.path.join(
                "./", DOCKER_COMPONENT, "resources", PYTHON_LIB_COMPONENT + ".tar.gz"
            )
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(
                glob.glob(
                    f"./{PYTHON_LIB_COMPONENT}/dist/{PYTHON_LIB_COMPONENT}-*.tar.gz"
                )[0],
                os.path.join(dest_path),
            )
        except Exception as ex:
            build_utils.log(
                f"Failed to copy {PYTHON_LIB_COMPONENT} distribution to {DOCKER_COMPONENT} component: "
                + str(ex)
            )
            build_utils.exit_process(1)

    # Build docker container
    build_utils.build(DOCKER_COMPONENT, args)

    # Build mkdocs documentation
    build_utils.build(DOCS_COMPONENT, args)


if __name__ == "__main__":
    args = build_utils.parse_arguments()

    if args.get(build_utils.FLAG_RELEASE):
        # Run main without release to see whether everthing can be built and all tests run through
        # Run args without release to see whether everthing can be built and all tests run through
        args = dict(args)
        args[build_utils.FLAG_RELEASE] = False
        main(args)
        # Run main again without building and testing the components again
        args = {
            **args,
            build_utils.FLAG_MAKE: False,
            build_utils.FLAG_CHECK: False,
            build_utils.FLAG_TEST: False,
            build_utils.FLAG_RELEASE: True,
            build_utils.FLAG_FORCE: True,
        }
    main(args)

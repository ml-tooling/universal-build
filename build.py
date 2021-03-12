import glob
import os
import shutil

from universal_build import build_utils
from universal_build.helpers import build_python

# Project specific configuration
MAIN_PACKAGE = "universal_build"
GITHUB_URL = "https://github.com/ml-tooling/universal-build"

HERE = os.path.abspath(os.path.dirname(__file__))


def main(args: dict) -> None:
    # set current path as working dir
    os.chdir(HERE)

    version = args.get(build_utils.FLAG_VERSION)

    if version:
        # Update version in _about.py
        build_python.update_version(
            os.path.join(HERE, f"src/{MAIN_PACKAGE}/_about.py"),
            build_utils._Version.get_pip_compatible_string(str(version)),
        )

    if args.get(build_utils.FLAG_MAKE):
        # Install pipenv dev requirements
        build_python.install_build_env()
        # Create API documentation via lazydocs
        build_python.generate_api_docs(github_url=GITHUB_URL, main_package=MAIN_PACKAGE)
        # Build distribution via setuptools
        build_python.build_distribution()

        try:
            dist_name = MAIN_PACKAGE.replace("_", "-")
            dist_file = glob.glob(f"./dist/{dist_name}-*.tar.gz")[0]
            shutil.copy(
                dist_file,
                os.path.join(
                    HERE, "build-environment", "resources", dist_name + ".tar.gz"
                ),
            )
        except Exception:
            build_utils.log("Failed to copy distribution to build container.")
            build_utils.exit_process(1)

    if args.get(build_utils.FLAG_CHECK):
        build_python.code_checks(exit_on_error=True, safety=False)

    if args.get(build_utils.FLAG_TEST):
        # Remove coverage files
        build_utils.run("pipenv run coverage erase", exit_on_error=False)

        test_markers = args.get(build_utils.FLAG_TEST_MARKER)

        if build_utils.TEST_MARKER_SLOW in test_markers:  # type: ignore
            # Run if slow test marker is set: test in multiple environments
            # Python 3.6
            build_python.test_with_py_version(python_version="3.6.12")

            # Python 3.7
            build_python.test_with_py_version(python_version="3.7.9")

            # Activated Python Environment (3.8)
            build_python.install_build_env()
            # Run pytest in pipenv environment
            build_utils.run("pipenv run pytest", exit_on_error=True)

            # Update pipfile.lock when all tests are successfull (lock environment)
            build_utils.run("pipenv lock", exit_on_error=True)
        else:
            # Run fast tests
            build_utils.run('pipenv run pytest -m "not slow"', exit_on_error=True)

    if args.get(build_utils.FLAG_RELEASE):
        # Bump all versions in some filess
        previous_version = build_utils.get_latest_version()
        if previous_version:
            build_utils.replace_in_files(
                previous_version,
                version,
                file_paths=[
                    "./actions/build-environment/Dockerfile",
                    "./README.md",
                    "./workflows/build-pipeline.yml",
                    "./workflows/release-pipeline.yml",
                ],
                regex=False,
                exit_on_error=True,
            )

        # Publish distribution on pypi
        build_python.publish_pypi_distribution(
            pypi_token=args.get(build_python.FLAG_PYPI_TOKEN),
            pypi_repository=args.get(build_python.FLAG_PYPI_REPOSITORY),
        )

        # TODO: Publish coverage report: if private repo set CODECOV_TOKEN="token" or use -t
        # build_utils.run("curl -s https://codecov.io/bash | bash -s", exit_on_error=False)

    # Build the build-environment component
    build_utils.build("build-environment", args)
    # Build all examples components
    build_utils.build("examples", args)


if __name__ == "__main__":
    args = build_python.parse_arguments()

    if args.get(build_utils.FLAG_RELEASE):
        # Run main without release to see whether everthing can be built and all tests run through
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

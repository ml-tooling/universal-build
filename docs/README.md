<!-- markdownlint-disable -->

# API Overview

## Modules

- [`universal_build.build_utils`](./universal_build.build_utils.md#module-universal_buildbuild_utils): Universal build utilities.
- [`universal_build.helpers`](./universal_build.helpers.md#module-universal_buildhelpers): Collection of helper modules with build utilities for specific technologies.
- [`universal_build.helpers.build_docker`](./universal_build.helpers.build_docker.md#module-universal_buildhelpersbuild_docker): Utilities to help building Docker images.
- [`universal_build.helpers.build_mkdocs`](./universal_build.helpers.build_mkdocs.md#module-universal_buildhelpersbuild_mkdocs): Utilities to help building MkDocs documentations.
- [`universal_build.helpers.build_python`](./universal_build.helpers.build_python.md#module-universal_buildhelpersbuild_python): Utilities to help building Python libraries.

## Classes


## Functions

- [`build`](./universal_build.build_utils.md#function-build): Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths.
- [`create_git_tag`](./universal_build.build_utils.md#function-create_git_tag): Create an annotated git tag in the current HEAD via `git tag` and the provided version.
- [`duplicate_folder`](./universal_build.build_utils.md#function-duplicate_folder): Duplicate a folder into another folder.
- [`exit_process`](./universal_build.build_utils.md#function-exit_process): Exit the process with exit code.
- [`log`](./universal_build.build_utils.md#function-log): Log message to stdout.
- [`parse_arguments`](./universal_build.build_utils.md#function-parse_arguments): Parses all arguments and returns a sanitized & augmented list of arguments.
- [`run`](./universal_build.build_utils.md#function-run): Run a specified command.
- [`build_docker_image`](./universal_build.helpers.build_docker.md#function-build_docker_image): Build a docker image from a Dockerfile in the working directory.
- [`lint_dockerfile`](./universal_build.helpers.build_docker.md#function-lint_dockerfile): Run hadolint on the Dockerfile.
- [`parse_arguments`](./universal_build.helpers.build_docker.md#function-parse_arguments): Parses all arguments and returns a sanitized & augmented list of arguments.
- [`release_docker_image`](./universal_build.helpers.build_docker.md#function-release_docker_image): Push a Docker image to a repository.
- [`build_mkdocs`](./universal_build.helpers.build_mkdocs.md#function-build_mkdocs): Build mkdocs markdown documentation.
- [`deploy_gh_pages`](./universal_build.helpers.build_mkdocs.md#function-deploy_gh_pages): Deploy mkdocs documentation to Github pages.
- [`install_build_env`](./universal_build.helpers.build_mkdocs.md#function-install_build_env): Installs a new virtual environment via pipenv.
- [`lint_markdown`](./universal_build.helpers.build_mkdocs.md#function-lint_markdown): Run markdownlint on markdown documentation.
- [`run_dev_mode`](./universal_build.helpers.build_mkdocs.md#function-run_dev_mode): Run mkdocs development server.
- [`build_distribution`](./universal_build.helpers.build_python.md#function-build_distribution): Build python package distribution.
- [`code_checks`](./universal_build.helpers.build_python.md#function-code_checks): Run linting and style checks.
- [`generate_api_docs`](./universal_build.helpers.build_python.md#function-generate_api_docs): Generates API documentation via lazydocs.
- [`install_build_env`](./universal_build.helpers.build_python.md#function-install_build_env): Installs a new virtual environment via pipenv.
- [`parse_arguments`](./universal_build.helpers.build_python.md#function-parse_arguments): Parses all arguments and returns a sanitized & augmented list of arguments.
- [`publish_pypi_distribution`](./universal_build.helpers.build_python.md#function-publish_pypi_distribution): Publish distribution to pypi.
- [`test_with_py_version`](./universal_build.helpers.build_python.md#function-test_with_py_version): Run pytest in a environment wiht the specified python version.
- [`update_version`](./universal_build.helpers.build_python.md#function-update_version): Update version in specified module.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

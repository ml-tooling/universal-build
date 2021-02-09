<!-- markdownlint-disable -->

# API Overview

## Modules

- [`universal_build.build_utils`](./universal_build.build_utils.md#module-universal_buildbuild_utils): Universal build utilities.
- [`universal_build.helpers`](./universal_build.helpers.md#module-universal_buildhelpers): Collection of helper modules with build utilities for specific technologies.
- [`universal_build.helpers.build_docker`](./universal_build.helpers.build_docker.md#module-universal_buildhelpersbuild_docker): Utilities to help building Docker images.
- [`universal_build.helpers.build_mkdocs`](./universal_build.helpers.build_mkdocs.md#module-universal_buildhelpersbuild_mkdocs): Utilities to help building MkDocs documentations.
- [`universal_build.helpers.build_python`](./universal_build.helpers.build_python.md#module-universal_buildhelpersbuild_python): Utilities to help building Python libraries.
- [`universal_build.helpers.openapi_utils`](./universal_build.helpers.openapi_utils.md#module-universal_buildhelpersopenapi_utils): OpenAPI utilities.

## Classes

- [`openapi_utils.OpenApiGenerator`](./universal_build.helpers.openapi_utils.md#class-openapigenerator): Enum of generators that can generate clients based on OpenAPI specifications.

## Functions

- [`build_utils.build`](./universal_build.build_utils.md#function-build): Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths.
- [`build_utils.command_exists`](./universal_build.build_utils.md#function-command_exists): Checks whether the `command` exists and is marked as executable.
- [`build_utils.copy`](./universal_build.build_utils.md#function-copy): Copy the files from source to target.
- [`build_utils.create_git_tag`](./universal_build.build_utils.md#function-create_git_tag): Create an annotated git tag in the current HEAD via `git tag` and the provided version.
- [`build_utils.duplicate_folder`](./universal_build.build_utils.md#function-duplicate_folder): Deprecated. Use `build_utils.copy` instead.
- [`build_utils.exit_process`](./universal_build.build_utils.md#function-exit_process): Exit the process with exit code.
- [`build_utils.get_latest_version`](./universal_build.build_utils.md#function-get_latest_version): Returns the latest version based on Git tags.
- [`build_utils.log`](./universal_build.build_utils.md#function-log): Log message to stdout.
- [`build_utils.parse_arguments`](./universal_build.build_utils.md#function-parse_arguments): Parses all arguments and returns a sanitized & augmented list of arguments.
- [`build_utils.replace_in_files`](./universal_build.build_utils.md#function-replace_in_files): Replaces a string or regex occurence in a collection of files.
- [`build_utils.run`](./universal_build.build_utils.md#function-run): Run a specified command.
- [`build_docker.build_docker_image`](./universal_build.helpers.build_docker.md#function-build_docker_image): Build a docker image from a Dockerfile in the working directory.
- [`build_docker.check_image`](./universal_build.helpers.build_docker.md#function-check_image): Run vulnerability checks on Dockerimage.
- [`build_docker.get_image_name`](./universal_build.helpers.build_docker.md#function-get_image_name): Get a valid versioned image name.
- [`build_docker.lint_dockerfile`](./universal_build.helpers.build_docker.md#function-lint_dockerfile): Run hadolint on the Dockerfile.
- [`build_docker.parse_arguments`](./universal_build.helpers.build_docker.md#function-parse_arguments): Parses all arguments and returns a sanitized & augmented list of arguments.
- [`build_docker.release_docker_image`](./universal_build.helpers.build_docker.md#function-release_docker_image): Push a Docker image to a repository.
- [`build_mkdocs.build_mkdocs`](./universal_build.helpers.build_mkdocs.md#function-build_mkdocs): Build mkdocs markdown documentation.
- [`build_mkdocs.deploy_gh_pages`](./universal_build.helpers.build_mkdocs.md#function-deploy_gh_pages): Deploy mkdocs documentation to Github pages.
- [`build_mkdocs.install_build_env`](./universal_build.helpers.build_mkdocs.md#function-install_build_env): Installs a new virtual environment via pipenv.
- [`build_mkdocs.lint_markdown`](./universal_build.helpers.build_mkdocs.md#function-lint_markdown): Run markdownlint on markdown documentation.
- [`build_mkdocs.run_dev_mode`](./universal_build.helpers.build_mkdocs.md#function-run_dev_mode): Run mkdocs development server.
- [`build_python.build_distribution`](./universal_build.helpers.build_python.md#function-build_distribution): Build python package distribution.
- [`build_python.code_checks`](./universal_build.helpers.build_python.md#function-code_checks): Run linting and style checks.
- [`build_python.generate_api_docs`](./universal_build.helpers.build_python.md#function-generate_api_docs): Generates API documentation via lazydocs.
- [`build_python.install_build_env`](./universal_build.helpers.build_python.md#function-install_build_env): Installs a new virtual environment via pipenv.
- [`build_python.is_pipenv_environment`](./universal_build.helpers.build_python.md#function-is_pipenv_environment): Check if current working directory is a valid pipenv environment.
- [`build_python.parse_arguments`](./universal_build.helpers.build_python.md#function-parse_arguments): Parses all arguments and returns a sanitized & augmented list of arguments.
- [`build_python.publish_pypi_distribution`](./universal_build.helpers.build_python.md#function-publish_pypi_distribution): Publish distribution to pypi.
- [`build_python.test_with_py_version`](./universal_build.helpers.build_python.md#function-test_with_py_version): Run pytest in a environment wiht the specified python version.
- [`build_python.update_version`](./universal_build.helpers.build_python.md#function-update_version): Update version in specified module.
- [`openapi_utils.generate_openapi_client`](./universal_build.helpers.openapi_utils.md#function-generate_openapi_client): Generate an open api client.
- [`openapi_utils.generate_openapi_js_client`](./universal_build.helpers.openapi_utils.md#function-generate_openapi_js_client): Calls `generate_openapi_client` to generate a javascript client.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

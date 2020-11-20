
# API Overview

## Modules

- [`universal_build.build_utils`](./universal_build.build_utils.md#module-universal_buildbuild_utils)
- [`universal_build.helpers`](./universal_build.helpers.md#module-universal_buildhelpers)
- [`universal_build.helpers.build_docker`](./universal_build.helpers.build_docker.md#module-universal_buildhelpersbuild_docker)
- [`universal_build.helpers.build_mkdocs`](./universal_build.helpers.build_mkdocs.md#module-universal_buildhelpersbuild_mkdocs)
- [`universal_build.helpers.build_python`](./universal_build.helpers.build_python.md#module-universal_buildhelpersbuild_python)

## Classes

- [`Version`](./universal_build.build_utils.md#class-version)
- [`VersionInvalidFormatException`](./universal_build.build_utils.md#class-versioninvalidformatexception)
- [`VersionInvalidPatchNumber`](./universal_build.build_utils.md#class-versioninvalidpatchnumber)

## Functions

- [`build`](./universal_build.build_utils.md#function-build): Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths.
- [`concat_command_line_arguments`](./universal_build.build_utils.md#function-concat_command_line_arguments)
- [`create_git_tag`](./universal_build.build_utils.md#function-create_git_tag): Create an annotated git tag in the current HEAD via `git tag` and the provided version.
- [`exit_process`](./universal_build.build_utils.md#function-exit_process): Exit the process with exit code.
- [`get_sanitized_arguments`](./universal_build.build_utils.md#function-get_sanitized_arguments): Return sanitized default arguments when they are valid.
- [`log`](./universal_build.build_utils.md#function-log)
- [`run`](./universal_build.build_utils.md#function-run): Run a specified command.
- [`build_docker_image`](./universal_build.helpers.build_docker.md#function-build_docker_image)
- [`get_sanitized_arguments`](./universal_build.helpers.build_docker.md#function-get_sanitized_arguments): Return sanitized default arguments when they are valid.
- [`release_docker_image`](./universal_build.helpers.build_docker.md#function-release_docker_image): Push a Docker image to a repository.
- [`build_mkdocs`](./universal_build.helpers.build_mkdocs.md#function-build_mkdocs): Build mkdocs markdown documentation.
- [`deploy_gh_pages`](./universal_build.helpers.build_mkdocs.md#function-deploy_gh_pages): Deploy mkdocs documentation to Github pages.
- [`install_build_env`](./universal_build.helpers.build_mkdocs.md#function-install_build_env): Installs a new virtual environment via pipenv.
- [`lint_markdown`](./universal_build.helpers.build_mkdocs.md#function-lint_markdown): Run markdownlint on markdown documentation.
- [`run_dev_mode`](./universal_build.helpers.build_mkdocs.md#function-run_dev_mode): Run mkdocs development server.
- [`build_distribution`](./universal_build.helpers.build_python.md#function-build_distribution): Build python package distribution.
- [`code_checks`](./universal_build.helpers.build_python.md#function-code_checks): Run linting and style checks.
- [`generate_api_docs`](./universal_build.helpers.build_python.md#function-generate_api_docs): Generates API documentation via lazydocs.
- [`get_sanitized_arguments`](./universal_build.helpers.build_python.md#function-get_sanitized_arguments): Return sanitized default arguments when they are valid.
- [`install_build_env`](./universal_build.helpers.build_python.md#function-install_build_env): Installs a new virtual environment via pipenv.
- [`publish_pypi_distribution`](./universal_build.helpers.build_python.md#function-publish_pypi_distribution): Publish distribution to pypi.
- [`test_with_py_version`](./universal_build.helpers.build_python.md#function-test_with_py_version): Run pytest in a environment wiht the specified python version.
- [`update_version`](./universal_build.helpers.build_python.md#function-update_version): Update version in specified module.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

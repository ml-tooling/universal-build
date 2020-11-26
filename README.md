<!-- markdownlint-disable MD033 MD041 -->
<h1 align="center">
    universal-build
</h1>

<p align="center">
    <strong>Universal build utilities for containerized build pipelines.</strong>
</p>

<p align="center">
    <a href="https://pypi.org/project/universal-build/" title="PyPi Version"><img src="https://img.shields.io/pypi/v/universal-build?color=green&style=flat"></a>
    <a href="https://pypi.org/project/universal-build/" title="Python Version"><img src="https://img.shields.io/badge/Python-3.6%2B-blue&style=flat"></a>
    <a href="https://github.com/ml-tooling/universal-build/actions?query=workflow%3Abuild-pipeline" title="Build status"><img src="https://img.shields.io/github/workflow/status/ml-tooling/universal-build/build-pipeline?style=flat"></a>
    <a href="https://github.com/ml-tooling/universal-build/blob/main/LICENSE" title="Project License"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat"></a>
    <a href="https://gitter.im/ml-tooling/universal-build/" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/universal-build.svg"></a>
    <a href="https://twitter.com/mltooling" title="ML Tooling on Twitter"><img src="https://img.shields.io/twitter/follow/mltooling.svg?label=follow&style=social"></a>
</p>

<p align="center">
  <a href="#getting-started">Getting Started</a> •
  <a href="#features">Features</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support--feedback">Support</a> •
  <a href="#contribution">Contribution</a> •
  <a href="https://github.com/ml-tooling/universal-build/releases">Changelog</a> •
  <a href="#faq--known-issues">FAQ</a>
</p>

Universal-build allows to implement your build and release pipeline with Python scripts once and run it either on your local machine, in a containerized environment via [Act](https://github.com/nektos/act), or automated via [Github Actions](https://github.com/features/actions). It supports a monorepo or polyrepo setup and can be used with any programming language or technology. It also provides a full release pipeline for automated releases with changelog generation.

> _**WIP**: This project is still an alpha version and not ready for general usage._

## Highlights

- 🐳&nbsp; Implement once and run locally, containerized, or on Github Actions.
- 🧰&nbsp; Build utilities for Python, Docker, React & MkDocs.
- 🔗&nbsp; Predefined Github Action Workflows for CI & CD.
- 🛠&nbsp; Integrated with [devcontainer](https://code.visualstudio.com/docs/remote/containers) for containerized development.

## Getting Started

### Installation

> _Requirements: Python 3.6+._

```bash
pip install universal-build
```

### Usage

To make use of universal build for your project, create a build script with the name `build.py` in your project root. The example below is for a single yarn-based webapp component:

```python
from universal_build import build_utils

args = build_utils.parse_arguments()

version = args.get(build_utils.FLAG_VERSION)

if args.get(build_utils.FLAG_MAKE):
    build_utils.log("Build the componet:")
    build_utils.run("yarn build")

if args.get(build_utils.FLAG_CHECK):
    build_utils.log("Run linters and style checks:")
    build_utils.run("yarn run lint:js")
    build_utils.run("yarn run lint:css")

if args.get(build_utils.FLAG_TEST):
    build_utils.log("Test the component:")
    build_utils.run("yarn test")

if args.get(build_utils.FLAGE_RELEASE):
    build_utils.log("Release the component:")
    # TODO: release the component to npm with version

```

Next, copy the [`build-environment`](https://github.com/ml-tooling/universal-build/blob/main/actions/build-environment) action from the [actions](https://github.com/ml-tooling/universal-build/tree/main/actions) folder into the  `.github/actions` folder of your repository. In addition, you need to copy the [build-](https://github.com/ml-tooling/universal-build/blob/main/workflows/build-pipeline.yml) and [release-pipeline](https://github.com/ml-tooling/universal-build/blob/main/workflows/release-pipeline.yml) workflows from the [workflows](https://github.com/ml-tooling/universal-build/tree/main/workflows) folder into the `.github/workflows` folder of your repository as well. Your repository should now contain atleast the following files:

```
your-repository
  - build.py
  - .github:
    - actions:
      - build-enviornment:
        - Dockerfile
        - actions.yaml
    - workflows:
      - release-pipeline.yml
      - build-pipeline.yml
```

Once you have pushed the `build-environment` action and the [build-](https://github.com/ml-tooling/universal-build/blob/main/workflows/build-pipeline.yml) and [release-pipelines](https://github.com/ml-tooling/universal-build/blob/main/workflows/release-pipeline.yml), please look into the [Automated Build Pipeline](#automated-build-pipeline-ci) and [Automated Release Pipeline](#automated-release-pipeline-cd) sections for information on how to run your build- and release-pipelines.

You can find a more detailed example project with multiple components in the [examples](https://github.com/ml-tooling/universal-build/tree/main/examples) folder.

---

<br>

## Support & Feedback

This project is maintained by [Benjamin Räthlein](https://twitter.com/raethlein), [Lukas Masuch](https://twitter.com/LukasMasuch), and [Jan Kalkan](https://www.linkedin.com/in/jan-kalkan-b5390284/). Please understand that we won't be able to provide individual support via email. We also believe that help is much more valuable if it's shared publicly so that more people can benefit from it.

| Type                     | Channel                                              |
| ------------------------ | ------------------------------------------------------ |
| 🚨&nbsp; **Bug Reports**       | <a href="https://github.com/ml-tooling/universal-build/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3Abug+sort%3Areactions-%2B1-desc+" title="Open Bug Report"><img src="https://img.shields.io/github/issues/ml-tooling/universal-build/bug.svg?label=bug"></a>                                 |
| 🎁&nbsp; **Feature Requests**  | <a href="https://github.com/ml-tooling/universal-build/issues?q=is%3Aopen+is%3Aissue+label%3Afeature+sort%3Areactions-%2B1-desc" title="Open Feature Request"><img src="https://img.shields.io/github/issues/ml-tooling/universal-build/feature.svg?label=feature"></a>                                 |
| 👩‍💻&nbsp; **Usage Questions**   |   <a href="https://stackoverflow.com/questions/tagged/ml-tooling" title="Open Question on Stackoverflow"><img src="https://img.shields.io/badge/stackoverflow-ml--tooling-orange.svg"></a> <a href="https://gitter.im/ml-tooling/universal-build" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/universal-build.svg"></a> |
| 🗯&nbsp; **General Discussion** | <a href="https://gitter.im/ml-tooling/universal-build" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/universal-build.svg"></a> <a href="https://twitter.com/mltooling" title="ML Tooling on Twitter"><img src="https://img.shields.io/twitter/follow/mltooling.svg?style=social"></a>|
| ❓&nbsp; **Other Requests** | <a href="mailto:team@mltooling.org" title="Email ML Tooling Team"><img src="https://img.shields.io/badge/email-ML Tooling-green?logo=mail.ru&style=flat-square&logoColor=white"></a> |

---

<br>

## Documentation

<p align="center">
  <a href="#build-script-cli">Build Script CLI</a> •
  <a href="#default-flags">Default Flags</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#update-universal-build">Update Universal Build</a>
</p>

### Build Script CLI

Any build script that utilizes the `build_utils.parse_arguments()` method to parse the CLI arguments can be executed with the following options:

```bash
python build.py [OPTIONS]
```

**Options**:

> _These options correspond to the default flags documented in the next section._

- `--make`: Make/compile/package all artifacts.
- `--test`: Run unit and integration tests.
- `--check`: Run linting and style checks.
- `--release`: Release all artifacts (e.g. to  registries like DockerHub or NPM).
- `--run`: Run the component in development mode (e.g. dev server).
- `--version VERSION`: Version of the build (`MAJOR.MINOR.PATCH-TAG`).
- `--force`: Ignore all enforcements and warnings.
- `--skip-path SKIP_PATH`: Skips the build phases for all (sub)paths provided here. This option can be used multiple times.
- `--test-marker TEST_MARKER`: Provide custom markers for testing. The default marker for slow tests is `slow`. This option can be used multiple times.
- `-h, --help`: Show the help message and exit.

### Default Flags

At its core, universal-build will parse all arguments provided to the build script via `build_utils.parse_arguments()` and returns a sanitized and augmented list of arguments. Those arguments are the building blocks for your build script. You can utilize those arguments in whatever way you like. Here is an example on how to use those arguments in a `build.py` script:

```python
from universal_build import build_utils

args = build_utils.parse_arguments()

version = args.get(build_utils.FLAG_VERSION)

if args.get(build_utils.FLAG_MAKE):
  # Run all relevant build commands.

if args.get(build_utils.FLAG_TEST):
  # Run all relevant commands for testing
  test_markers = args.get(build_utils.FLAG_TEST_MARKER)
  if "slow" in test_markers:
    # Run additional slow tests.
```

The following list contains all of the default flags currently supported by universal-build:

| Flag  | Type | Description |
| --- | --- | --- |
|  `FLAG_MAKE`  | `bool` | Build/compile/package all artifacts. |
|  `FLAG_CHECK`  | `bool` | Run linting and style checks. |
|  `FLAG_TEST`  | `bool` | Run unit and integration tests. |
|  `FLAG_RELEASE`  | `bool` | Release all artifacts (e.g. to  registries like DockerHub or NPM). |
|  `FLAG_RUN`  | `bool` | Run the component in development mode (e.g. dev server). |
|  `FLAG_FORCE`  | `bool` | Ignore all enforcements and warnings. |
|  `FLAG_VERSION`  | `str` | Semantic version for the build. If not provided via CLI arguments, a valid dev version will be automatically calculated. |
|  `FLAG_TEST_MARKER`  | `List[str]` | Custom markers for testing. Can be used to skip or execute certain tests. |

### API Reference

In addition to argument parsing capabilities, universal-build also contains a variety of utility functions to make building complex projects with different technologies easy. You can find all utilities in the Python API documentation [here](https://github.com/ml-tooling/universal-build/tree/main/docs).

### Update Universal Build

To update the universal-build version of your project, simply look up the most recent version of build-environment on [DockerHub](https://hub.docker.com/repository/docker/mltooling/build-environment) and set this version in the `.github/actions/build-environment/Dockerfile` file of your repository:

```Dockerfile
FROM mltooling/build-environment:<UPDATED_VERSION>
```

In case you also run your build outside of the build-environment (locally), make sure to also upgrade universal-build on your local machine from [PyPi](https://pypi.org/project/universal-build/):

```bash
pip install --upgrade universal-build
```

Furthermore, you can also check if the [build-](https://github.com/ml-tooling/universal-build/blob/main/workflows/build-pipeline.yml) and [release-pipeline](https://github.com/ml-tooling/universal-build/blob/main/workflows/release-pipeline.yml) workflows have changed. In case of changes, update the workflows in your `.github/workflows` folder of your repository as well.

---

<br>

## Features

<p align="center">
  <a href="#support-for-nested-components">Support for Nested Components</a> •
  <a href="#automated-build-pipeline-ci">Automated Build Pipeline</a> •
  <a href="#automated-release-pipeline-cd">Automated Release Pipeline</a> •
  <a href="#containerized-development">Containerized Development</a> •
  <a href="#simplified-versioning">Simplified Versioning</a> •
  <a href="#mkdocs-utilities">MkDocs Utilities</a> •
  <a href="#python-utilities">Python Utilities</a> •
  <a href="#docker-utilities">Docker Utilities</a> •
  <a href="#extensibility">Extensibility</a>
</p>

### Automated Build Pipeline (CI)

Universal-build enables you to run your build pipeline on your local machine, in a containerized environment via [Act](https://github.com/nektos/act), or automated via [Github Actions](https://github.com/features/actions) (= Continuous Integration).

#### Local machine via build script (not recommended):

> _Requirements: [universal-build](#installation) and all the build requirements that your build script is using (e.g. yarn, pipenv, maven, ...) need to be installed on your machine._

Execute the following command in the root folder of any component with a valid `build.py` script:

```bash
python build.py --make --check --test
```

Executing the build-pipeline directly via the build scripts is not recommended.

#### Containerized environment via Act:

> _Requirements: [Docker](https://docs.docker.com/get-docker/) and [Act](https://github.com/nektos/act#installation) are required to be installed on your machine._

Execute this command in the root folder of your repository:

```bash
act -b -s BUILD_ARGS="--check --make --test" -j build
```

#### Manually via Github Actions:

In the Github UI, go to `Actions` -> select `build-pipeline` -> select `Run Workflow` and provide the build arguments, e.g. `--check --make --test`.

#### Automated via Github Actions (CI):

With the default configuration, the build pipeline will run automatically via Github Actions on any `push` event to your repository. This automation can be referred to as continuous integration. You can also change the events that trigger the build-pipeline by modifying the `on` section in the `.github/workflows/build-pipeline.yml` file. You can find more information about Github Actions events [here](https://docs.github.com/en/free-pro-team@latest/actions/reference/events-that-trigger-workflows).

### Automated Release Pipeline (CD)

To release a new version and publish all relevant artifacts to the respective registries (e.g. Docker image to DockerHub) you can either trigger our release pipeline on your local machine, in a containerized environment via [Act](https://github.com/nektos/act), or automated via [Github Actions](https://github.com/features/actions) (= Continuous Delivery).

#### Local machine via build script (not recommended):

> _Requirements: [universal-build](#installation) and all the build requirements that your build script is using (e.g. yarn, pipenv, maven, ...) need to be installed on your machine._

Execute the following command in the root folder of any component with a valid `build.py` script:

```bash
python build.py --make --check --test --release --version="<MAJOR.MINOR.PATCH>"
```

Executing the release step directly via the build scripts is not recommended.

#### Containerized environment via Act:

> _Requirements: [Docker](https://docs.docker.com/get-docker/) and [Act](https://github.com/nektos/act#installation) are required to be installed on your machine._

Execute this command in the root folder of your repository:

```bash
act -b -s VERSION="<MAJOR.MINOR.PATCH>" -j release
```

In case you also want to automatically create a valid Github release, you also need to provide a valid `GITHUB_TOKEN` as a secret (`-s GITHUB_TOKEN=<token>`). Please refer to the next section for information on how to finish and publish the release.

#### On Github Actions (CD):

> _Make sure that all required secrets for you release pipeline are configured in your Github repository. More information [here](ttps://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository)._

To trigger our release pipeline from Github UI, you can either close a milestone that has a valid version name (`vMAJOR.MINOR.PATCH`) or execute the release pipeline manually via the `workflow_dispatch` UI in the Action Tab (`Actions -> release-pipeline -> Run Workflow`). The release pipeline will automatically run the build, check, test, and release steps, and create a pull request for the new version as well as a draft release on Github. This automation can be referred to as continuous delivery.

After successful execution of the release pipeline, the following steps are required to finish the release:

1. Merge the release PR into `main`. Preferably via merge commit to keep the version tag in the `main` branch. We suggest to use the following message for the merge commit: `Finalize release for version <VERSION> (#<PR>)`.
2. Adapt the changelog of the draft release on Github (in the release section). Mention all other changes that are not covered by pull requests.
3. Publish the release.

#### Resolve an unsuccessful release:

In case the release pipeline fails at any step, we suggest to fix the problem based on the release pipeline logs and create a new release with an incremented `patch` version. To clean up the unsuccessful release, make sure to delete the following artifacts (if they exist): the release branch, the release PR, the version tag, the draft release, and any release artifact that was already published (e.g. on DockerHub, NPM or PyPi).

### Support for Nested Components

> _You can find the implementation of this multi-nested example in the [examples](https://github.com/ml-tooling/universal-build/tree/main/examples) folder._

Universal-build has excellent support for repositories that contain multiple nested components (aka Monorepo). The following [`examples`](https://github.com/ml-tooling/universal-build/tree/main/examples) repository has four components: `docs`, `react-webapp`, `docker`, and `python-lib`:

```plain
examples:
  - build.py
  - docs:
    - build.py
  - react-webapp:
    - build.py
  - docker:
    - build.py
  - python-lib:
    - build.py
```

Every component needs its own `build.py` script in the component root folder that implements all the logic to build, check, test, and release the given component. The `build.py` script in the repo root folder contains the build logic that orchestrates all component builds. Universal-build provides the [`build_utils.build()`](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.build_utils.md#function-build) function that allows to call the build script of a sub-component with the parsed arguments (find more info on `build` function in the [API documentation](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.build_utils.md#function-build)).

In between the build steps, you can execute any required operations, for example, duplicating build artifacts from one component to another. The following example, shows the `build.py` script that would support the `examples` repository structure:

```python
from universal_build import build_utils

args = build_utils.parse_arguments()

build_utils.build("react-webapp", args)
build_utils.build("python-lib", args)
build_utils.duplicate_folder("./python-lib/docs/", "./docs/docs/api-docs/")
build_utils.build("docker", args)
build_utils.build("docs", args)
```

With this setup, you can execute the build pipeline for the full project or any individual component. In case you only apply changes to a single component, you only need to execute the `build.py` script of the given component. This is a major advantage since it might massively speed up your development time.

To run the build pipeline on you local machine only for a specific component, navigate to the component and run the `build.py` script in the component root folder (you can find all CLI build arguments [here](#build-script-cli)):

```bash
cd "./docs" && python build.py [BUILD_ARGUMENTS]
```

Alternatively, you can also run the component build containerized via Act:

```bash
act -b -s BUILD_ARGS="[BUILD_ARGUMENTS]" -s WORKING_DIRECTORY="./docs" -j build
```

Or directly from the Github UI: `Actions` -> `build-pipeline` -> `Run workflow`. The Github UI will allow you to set the build arguments and working directory.

### Simplified Versioning

> Only [semantic versioning](https://semver.org/) is supported at the moment.

If you do not provide an explicit version via the build arguments (`--version`), universal-build will automatically detect the latest version via Git tags and pass a dev version to your build scripts. The dev version will have the following format: `<MAJOR>.<MINOR>.<PATCH>-dev.<BRANCH>`. This should be sufficient for the majority of development builds. However, the release step still requires to have a valid semantic version provided via the arguments.

### Python Utilities

The [`build_python`](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_python.md) module of universal-build provides a collection of utilities to simplify the process of building and releasing Python packages. Refer to the [API documentation](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_python.md) for full documentation on all python utilities. An example for a build script for a Python package is shown below:

```python
from universal_build import build_utils
from universal_build.helpers import build_python

# Project specific configuration
MAIN_PACKAGE = "template_package"

args = build_python.parse_arguments()

version = args.get(build_utils.FLAG_VERSION)

# Update version in __version__.py
build_python.update_version(os.path.join(HERE, f"src/{MAIN_PACKAGE}/__version__.py"), str(version))

if args.get(build_utils.FLAG_MAKE):
  # Install pipenv dev requirements
  build_python.install_build_env()
  # Build distribution via setuptools
  build_python.build_distribution()

if args.get(build_utils.FLAG_CHECK):
  build_python.code_checks()

if args.get(build_utils.FLAG_TEST):
  build_utils.run('pipenv run pytest -m "not slow"')

  if "slow" in args.get(build_utils.FLAG_TEST_MARKER):
    build_python.test_with_py_version(python_version="3.6.12")

if args.get(build_utils.FLAG_RELEASE):
  # Publish distribution on pypi
  build_python.publish_pypi_distribution(pypi_token=args.get(build_python.FLAG_PYPI_TOKEN),pypi_repository=args.get(build_python.FLAG_PYPI_REPOSITORY))
```

The [`build_python.parse_arguments()`](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_python.md#function-parse_arguments) argument parser has the following additional flags:

| Flag  |  Type  | Description |
| --- | --- | --- |
|  `FLAG_PYPI_TOKEN`  | `str` | Personal access token for PyPI account. |
|  `FLAG_PYPI_REPOSITORY`  | `str` | PyPI repository for publishing artifacts. |

And the following additional CLI options:

- `--pypi-token`: Personal access token for PyPI account.
- `--pypi-repository`: PyPI repository for publishing artifacts.

### Docker Utilities

The [`build_docker`](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_docker.md) module of universal-build provides a collection of utilities to simplify the process of building and releasing Docker images. Refer to the [API documentation](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_docker.md) for full documentation on all docker utilities. An example for a build script for a Docker image is shown below:

```python
from universal_build import build_utils
from universal_build.helpers import build_docker

IMAGE_NAME = "build-environment"
DOCKER_IMAGE_PREFIX = "mltooling"

args = build_docker.parse_arguments()

version = args.get(build_utils.FLAG_VERSION)

if args.get(build_utils.FLAG_MAKE):
  build_docker.build_docker_image(COMPONENT_NAME, version)

if args.get(build_utils.FLAG_CHECK):
  build_docker.lint_dockerfile()

if args.get(build_utils.FLAG_RELEASE):
  build_docker.release_docker_image(IMAGE_NAME, version, DOCKER_IMAGE_PREFIX)
```

The [`build_docker.parse_arguments()`](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_docker.md#function-parse_arguments) argument parser has the following additional flags:

| Flag  |  Type  | Description |
| --- | --- | --- |
|  `FLAG_DOCKER_IMAGE_PREFIX`  | `str` | Docker image prefix. This should be used to define the container registry where the image should be pushed to. |

And the following additional CLI options:

- `--docker-image-prefix`: Docker image prefix. This should be used to define the container registry where the image should be pushed to.

### MkDocs Utilities

The [`build_mkdocs`](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_mkdocs.md) module of universal-build provides a collection of utilities to simplify the process of building and releasing MkDocs documentation. Refer to the [API documentation](https://github.com/ml-tooling/universal-build/blob/main/docs/universal_build.helpers.build_mkdocs.md) for full documentation on all MkDocs utilities. An example for a build script for  MkDocs documentation is shown below:

```python
from universal_build import build_utils
from universal_build.helpers import build_mkdocs

args = build_utils.parse_arguments()

if args.get(build_utils.FLAG_MAKE):
  # Install pipenv dev requirements
  build_mkdocs.install_build_env()
  # Build mkdocs documentation
  build_mkdocs.build_mkdocs()

if args.get(build_utils.FLAG_CHECK):
  build_mkdocs.lint_markdown()

if args.get(build_utils.FLAG_RELEASE):
  # Deploy to Github pages
  build_mkdocs.deploy_gh_pages()
```

### Extensibility

#### Extend your build-environment image with additional tools

Install the tools in the Dockerfile in your `.github/actions/build-environment/Dockerfile` as demonstrated in this example:

```Dockerfile
FROM mltooling/build-environment:0.4.2

# Install Go Runtime
RUN apt-get update \
    && apt-get install -y golang-go
```

#### Extend the entrypoint of the build-environment

You can extend or overwrite the default entrypoint with your custom entrypoint script (e.g. `extended-entrypoint.sh`) as shown below:

```Dockerfile
FROM mltooling/build-environment:0.4.2

COPY extended-entrypoint.sh /extended-entrypoint.sh

RUN chmod +x /extended-entrypoint.sh

ENTRYPOINT ["/tini", "-g", "--", "/extended-entrypoint.sh"]
```

The following `extended-entrypoint.sh` example demonstrates how to extend and reuse the existing default entrypoint:

```bash
# Stops script execution if a command has an error
set -e

echo "Setup Phase"

# TODO: Do your custom setups here

# Call the default build-environment entrypoint.
# Disable the immediate script execution stop so that the cleanup phase can run in any case
set +e
# Thereby, you can reuse the existing implementation:
/bin/bash /entrypoint.sh "$@"
# Save the exit code of the previous command
exit_code=$?

echo "Cleanup Phase"

# TODO: Do additional cleanup

# Exit the script with the exit code of the actual entrypoint execution
exit $exit_code

```

#### Support additional build arguments

The following example demonstrates how you can support custom build arguments (CLI) in your `build.py` script:

```python
import argparse

from universal_build import build_utils

parser = argparse.ArgumentParser()
parser.add_argument("--deployment-token", help="Token to deploy component.", default="")

args = build_utils.parse_arguments(argument_parser=parser)

deployment_token = args.get("deployment_token")
```

Once it is implemented in your build script, you can provide the build argument via the CLI options: `python build.py --deployment-token=my-token`. If your custom argument is a `string` and has a default string value (e.g. `default=""`), you can also provide the build argument via environment variables: `DEPLOYMENT_TOKEN=mytoken python build.py`.

To use your custom build arguments inside the release pipeline, you need to add the `DEPLOYMENT_TOKEN` as a secret to your Github repository (more info [here](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository)) and adapt the `.github/workflows/release-pipeline.yml` file by adding the `DEPLOYMENT_TOKEN` as an environment variable (`env`) to the steps that need this build argument, for example:

```yaml
- name: release-components
  uses: ./.github/actions/build-environment
  env:
    DEPLOYMENT_TOKEN: ${{ secrets.DEPLOYMENT_TOKEN }}
```

#### Use custom test markers to select tests for execution

You can provide any number of custom test markers via the `--test-marker` build argument. The following example shows how to react to custom test markers in your build script:

```python
if args.get(build_utils.FLAG_TEST):
  # Run your default tests
  if "integration" in args.get(build_utils.FLAG_TEST_MARKER):
    # Run integration tests
```

### Containerized Development

The [build-environment](./build-environment) can also be used for development inside a container. It is fully compatible with the [devcontainer](https://code.visualstudio.com/docs/remote/containers#_create-a-devcontainerjson-file) standard that is used by VS Code and Github Codespaces. The big advantage of using the build-environment for containerized development is that you only have to define your project dependencies in one location, and use this for development, local builds, and automated CI / CD pipelines.

To use the build-environment for containerized development, just define a `.devcontainer/devcontainer.json` configuration inside your repository and link the `build.dockerfile` to the build-environment action in the `.github/actions/build-environment/Dockerfile` folder. A minimal `devcontainer.json` configuration could look like this:

```
{
  "name": "build-environment",
  "build": {
    "dockerfile": "../.github/actions/build-environment/Dockerfile"
  },
  "settings": {
    // Set default container specific vs code settings
    "terminal.integrated.shell.linux": "/bin/bash"
  },
  "extensions": [
    // Add required extensions
  ]
}
```

You can find a full example [here](https://github.com/ml-tooling/universal-build/blob/main/.devcontainer/devcontainer.json).

---

<br>

## FAQ & Known Issues

<details>

<summary><b>Act: Error response from daemon - volume is in use</b> (click to expand...)</summary>

Sometimes the act containers are not removed properly and are blocking any subsequent act executions of your workflow. As a workaround, you can just remove all act containers:

```bash
docker rm -f $(docker ps -a --filter="name=^act-" -q)
```

</details>

<details>
<summary><b>How to access the host from Docker Containers in GitHub Actions / Act or containers from the host</b> (click to expand...)</summary>

If you want to access the host (in act the pipeline container and on GitHub Actions the Linux VM) from within a container, you can set an environment variable in the workflow file with this step:

```yaml
- name: set-host-ip
  run: echo "::set-env name=_HOST_IP::$(hostname -I | cut -d ' ' -f 1)"
  # new syntax which is not yet supported on act:
  # run: echo "_HOST_IP=$(hostname -I | cut -d ' ' -f 1)" >> "$GITHUB_ENV"
```

and then access the environment variable from within a container. This way you can, for example, access other containers with published ports or other host services.

If you want to access a container directly without going through the host, you can get the IP address for example in the following way:

```bash
container_id=<CONTAINER-ID-OR-NAME>
container_ip=$(docker inspect $container_id | jq -r '.[0].NetworkSettings.Networks.bridge.IPAddress')
```

> Note that the tool `jq` has to be installed. If you run a python script and use the Docker client, the command looks different, of course.

When you don't put starting containers into a custom network, the container is now reachable from the host (GitHub Actions & Act) as well as other containers under this `$container_ip` address. Yet, it is *not* reachable from your local machine (e.g. your Mac). For that, you have to publish the port and use the `$_HOST_IP` address as explained above. The host port should be assigned randomly so that the setup is as host-independent as possible. To dynamically get the random port you can get it in the following way via bash:

```bash
container_id=<CONTAINER-ID-OR-NAME>
container_port=<INNER-CONTAINER-PORT>
container_host_port=$(docker inspect $container_id | jq -r '.[0].NetworkSettings.Ports["'$container_port'/tcp"][0].HostPort')
```

In your code, you should then check whether the `$_HOST_IP` variable is set and if not, use `localhost`. This way, it will work on GitHub Actions, Act, and your local machine. Here is a Python example:

```python
import docker

client = docker.from_env()
container_name = "test-container"
container_port = 8080
container = client.containers.run(
    "some-image:1.2.3",
    name=container_name,
    ports={f"{container_port}/tcp": None},
    detach=True,
)

container.reload()
ip_address = os.getenv("_HOST_IP", "localhost")
os.environ["CONTAINER_NAME"] = container_name
os.environ["CONTAINER_IP"] = ip_address
container_host_port = container.attrs["NetworkSettings"]["Ports"][f"{container_port}/tcp"][0]["HostPort"]
os.environ["CONTAINER_HOST_PORT"] = container_host_port
```

</details>

---

<br>

## Contributors

[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/0)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/0)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/1)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/1)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/2)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/2)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/3)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/3)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/4)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/4)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/5)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/5)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/6)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/6)[![](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/images/7)](https://sourcerer.io/fame/LukasMasuch/ml-tooling/universal-build/links/7)

## Contribution

- Pull requests are encouraged and always welcome. Read our [contribution guidelines](https://github.com/ml-tooling/universal-build/tree/main/CONTRIBUTING.md) and check out [help-wanted](https://github.com/ml-tooling/lazydocs/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3A"help+wanted"+sort%3Areactions-%2B1-desc+) issues.
- Submit Github issues for any [feature request and enhancement](https://github.com/ml-tooling/universal-build/issues/new?assignees=&labels=feature&template=02_feature-request.md&title=), [bugs](https://github.com/ml-tooling/lazydocs/issues/new?assignees=&labels=bug&template=01_bug-report.md&title=), or [documentation](https://github.com/ml-tooling/universal-build/issues/new?assignees=&labels=documentation&template=03_documentation.md&title=) problems.
- By participating in this project, you agree to abide by its [Code of Conduct](https://github.com/ml-tooling/universal-build/blob/main/.github/CODE_OF_CONDUCT.md).
- The [development section](#development) below contains information on how to build and test the project after you have implemented some changes.

## Development

> _**Requirements**: [Docker](https://docs.docker.com/get-docker/) and [Act](https://github.com/nektos/act#installation) are required to be installed on your machine to execute the build process._

To simplify the process of building this project from scratch, we provide build-scripts that run all necessary steps (build, check, test, and release) within a containerized environment. To build and test your changes, execute the following command in the project root folder:

```bash
act -b -j build
```

Refer to our [contribution guides](https://github.com/ml-tooling/universal-build/blob/main/CONTRIBUTING.md#development-instructions) for more detailed information on our build scripts and development process.

---

Licensed **MIT**. Created and maintained with ❤️&nbsp; by developers from Berlin.

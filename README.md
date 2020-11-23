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
  <a href="https://github.com/ml-tooling/universal-build/releases">Changelog</a>
</p>

> _**WIP**: This project is still an alpha version and not ready for general usage._

Universal Build allows to implement your build and release pipeline with Python scripts once and run it either on your local machine, in a containerized environment via [Act](https://github.com/nektos/act), or automated via [Github Actions](https://github.com/features/actions). It supports a monorepo or polyrepo setup and can be used with any programming language or technology. It also provides a full release pipeline for automated releases with changelog generation.

## Highlights

- 🧰&nbsp; Build utilities for Python, Docker, React & MkDocs
- 🔗&nbsp; Predefined Github Action Workflows for CI & CD
- 🛠&nbsp; Integrated with [devcontainer](https://code.visualstudio.com/docs/remote/containers) for containerized development.
- 🐳&nbsp; Run builds locally, containerized via Act, or on Github Actions

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

args = build_utils.get_sanitized_arguments()

version = args.get(build_utils.FLAG_VERSION)

if args.get(build_utils.FLAG_MAKE):
    build_utils.log("Build the componet:")
    build_utils.run("yarn build", exit_on_error=True)

if args.get(build_utils.FLAG_CHECK):
    build_utils.log("Run linters and style checks:")
    build_utils.run("yarn run lint:js", exit_on_error=True)
    build_utils.run("yarn run lint:css", exit_on_error=True)

if args.get(build_utils.FLAG_TEST):
    build_utils.log("Test the component:")
    build_utils.run("yarn test", exit_on_error=True)

if args.get(build_utils.FLAGE_RELEASE):
    build_utils.log("Release the component:")
    # TODO: release the component to npm with version

```

Next, copy the build and release-pipeline workflows into your repo into the `.github/workflows` folder. Once you have pushed the build and release pipelines, you have the following options to trigger your build pipeline:

On your local machine via the build script (you need to have all dependencies for the build installed):

```bash
python build.py --make --check --test
```

In a containerized environment on your local machine via [Act](https://github.com/nektos/act):

```bash
act -b -s BUILD_ARGS="--check --make --test" -j build
```

On Github via Github Actions: In the Github UI, go to `Actions` -> select `build-pipeline` -> select `Run Workflow` and provide the build arguments, e.g. `--check --make --test`. You build pipeline will also run via Github Actions automatically on any push to your repository.

You can find more information on the release pipeline or other features in the [features](#features) section.

## Support & Feedback

This project is maintained by [Benjamin Räthlein](https://twitter.com/raethlein), [Lukas Masuch](https://twitter.com/LukasMasuch), and [Jan Kalkan](https://www.linkedin.com/in/jan-kalkan-b5390284/). Please understand that we won't be able to provide individual support via email. We also believe that help is much more valuable if it's shared publicly so that more people can benefit from it.

| Type                     | Channel                                              |
| ------------------------ | ------------------------------------------------------ |
| 🚨&nbsp; **Bug Reports**       | <a href="https://github.com/ml-tooling/universal-build/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3Abug+sort%3Areactions-%2B1-desc+" title="Open Bug Report"><img src="https://img.shields.io/github/issues/ml-tooling/universal-build/bug.svg?label=bug"></a>                                 |
| 🎁&nbsp; **Feature Requests**  | <a href="https://github.com/ml-tooling/universal-build/issues?q=is%3Aopen+is%3Aissue+label%3Afeature+sort%3Areactions-%2B1-desc" title="Open Feature Request"><img src="https://img.shields.io/github/issues/ml-tooling/universal-build/feature.svg?label=feature"></a>                                 |
| 👩‍💻&nbsp; **Usage Questions**   |   <a href="https://stackoverflow.com/questions/tagged/ml-tooling" title="Open Question on Stackoverflow"><img src="https://img.shields.io/badge/stackoverflow-ml--tooling-orange.svg"></a> <a href="https://gitter.im/ml-tooling/universal-build" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/universal-build.svg"></a> |
| 🗯&nbsp; **General Discussion** | <a href="https://gitter.im/ml-tooling/universal-build" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/universal-build.svg"></a> <a href="https://twitter.com/mltooling" title="ML Tooling on Twitter"><img src="https://img.shields.io/twitter/follow/mltooling.svg?style=social"></a>|
| ❓&nbsp; **Other Requests** | <a href="mailto:team@mltooling.org" title="Email ML Tooling Team"><img src="https://img.shields.io/badge/email-ML Tooling-green?logo=mail.ru&style=flat-square&logoColor=white"></a> |

## Features

<p align="center">
  <a href="#automated-release-pipeline">Automated Build Pipeline</a> •
  <a href="#automated-release-pipeline">Automated Release Pipeline</a> •
  <a href="#containerized-development">Containerized Development</a> •
  <a href="#mkdocs-utilities">MkDocs Utilities</a> •
  <a href="#docker-utilities">Python Utilities</a> •
  <a href="#docker-utilities">Docker Utilities</a>
</p>

### Automated Build Pipeline

_TBD_

### Automated Release Pipeline

_TBD_

### Containerized Development

_TBD_

### Simplified Versioning

_TBD_

### MkDocs Utilities

_TBD_

### Python Utilities

_TBD_

### Docker Utilities

_TBD_

## Documentation

### Build Script CLI

Any build script that utilizes the `build_utils.get_sanitized_arguments()` method to parse the CLI arguments can be executed with the following options:

```bash
python build.py [OPTIONS]
```

**Options**:

*  `--make`: Make/compile/package all artifacts.
*  `--test`: Run unit and integration tests.
*  `--check`: Run linting and style checks.
*  `--release`: Release all artifacts (e.g. to  registries like DockerHub or NPM).
*  `--run`: Run the component in development mode (e.g. dev server).
*  `--version VERSION`: Version of the build (`MAJOR.MINOR.PATCH-TAG`).
*  `--force`: Ignore all enforcements and warnings.
*  `--skip-path SKIP_PATH`: Skips the build phases for all (sub)paths provided here.
*  `--test-marker TEST_MARKER`: Provide custom markers for testing. The default marker for slow tests is `slow`.
*  `-h, --help`: Show the help message and exit.

### Default Flags

At its core, universal-build will parse all arguments provided to the build script via `build_utils.get_sanitized_arguments()` and returns a sanitized and augmented list of arguments. Those arguments are the building blocks for your build script. You can utilize those arguments in whatever way to like. Here is an example on how to use those arguments in a `build.py` script:

```python
from universal_build import build_utils

args = build_utils.get_sanitized_arguments()

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

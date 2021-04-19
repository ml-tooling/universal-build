<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.helpers.build_docker`
Utilities to help building Docker images. 

**Global Variables**
---------------
- **FLAG_DOCKER_IMAGE_PREFIX**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_arguments`

```python
parse_arguments(
    input_args: List[str] = None,
    argument_parser: ArgumentParser = None
) → dict
```

Parses all arguments and returns a sanitized & augmented list of arguments. 

Sanitized means that, for example, the version is already checked and set depending on our build guidelines. If arguments are not valid, exit the script run. 



**Args:**
 
 - <b>`input_args`</b> (List[str], optional):  List of arguments that are used instead of the arguments passed to the process. Defaults to `None`. 
 - <b>`argument_parser`</b> (arparse.ArgumentParser, optional):  An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. 



**Returns:**
 
 - <b>`dict`</b>:  The parsed default arguments thar are already checked for validity. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `check_image`

```python
check_image(
    image: str,
    trivy: bool = True,
    exit_on_error: bool = True
) → CompletedProcess
```

Run vulnerability checks on Dockerimage. 



**Args:**
 
 - <b>`image`</b> (str):  The name of the docker image to check. 
 - <b>`trivy`</b> (bool, optional):  Activate trivy vulnerability check. Defaults to `True`. 
 - <b>`exit_on_error`</b> (bool, optional):  If `True`, exit process as soon as an error occurs. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `lint_dockerfile`

```python
lint_dockerfile(
    hadolint: bool = True,
    dockerfile: str = 'Dockerfile',
    exit_on_error: bool = True
) → None
```

Run hadolint on the Dockerfile. 



**Args:**
 
 - <b>`hadolint`</b> (bool, optional):  Activate hadolint dockerfile linter. Defaults to `True`. 
 - <b>`dockerfile`</b> (str, optional):  Specify a specific Dockerfile. If not specified, the default `Dockerfile` wil be used. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_image_name`

```python
get_image_name(name: str, tag: str, image_prefix: str = '') → str
```

Get a valid versioned image name. 



**Args:**
 
 - <b>`name`</b> (str):  Name of the docker image. 
 - <b>`tag`</b> (str):  Version to use for the tag. 
 - <b>`image_prefix`</b> (str, optional):  The prefix added to the name to indicate an organization on DockerHub or a completely different repository. 



**Returns:**
 
 - <b>`str`</b>:  a valid docker image name based on: prefix/name:tag 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_docker_image`

```python
build_docker_image(
    name: str,
    version: str,
    build_args: str = '',
    docker_image_prefix: str = '',
    dockerfile: Optional[str] = None,
    additional_build_args: str = '',
    exit_on_error: bool = True
) → CompletedProcess
```

Build a docker image from a Dockerfile in the working directory. 



**Args:**
 
 - <b>`name`</b> (str):  Name of the docker image. 
 - <b>`version`</b> (str):  Version to use as tag. 
 - <b>`build_args`</b> (str, optional):  Add additional build arguments for docker build. 
 - <b>`docker_image_prefix`</b> (str, optional):  The prefix added to the name to indicate an organization on DockerHub or a completely different repository. 
 - <b>`dockerfile`</b> (str, optional):  Specify a specific Dockerfile. If not specified, the default `Dockerfile` wil be used. 
 - <b>`exit_on_error`</b> (bool, optional):  If `True`, exit process as soon as an error occurs. 



**Returns:**
 
 - <b>`subprocess.CompletedProcess`</b>:  Returns the CompletedProcess object of the 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `release_docker_image`

```python
release_docker_image(
    name: str,
    version: str,
    docker_image_prefix: str,
    exit_on_error: bool = True
) → CompletedProcess
```

Push a Docker image to a repository. 



**Args:**
 
 - <b>`name`</b> (str):  The name of the image. Must not be prefixed! 
 - <b>`version`</b> (str):  The tag used for the image. 
 - <b>`docker_image_prefix`</b> (str):  The prefix added to the name to indicate an organization on DockerHub or a completely different repository. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 



**Returns:**
 
 - <b>`subprocess.CompletedProcess`</b>:  Returns the CompletedProcess object of the `docker push ...` command. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

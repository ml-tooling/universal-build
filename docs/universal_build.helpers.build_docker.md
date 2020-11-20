
<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.helpers.build_docker`




**Global Variables**
---------------
- **FLAG_DOCKER_IMAGE_PREFIX**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_sanitized_arguments`

```python
get_sanitized_arguments(
    arguments: List[str] = None,
    argument_parser: ArgumentParser = None
) → Dict[str, Union[str, bool, List[str]]]
```

Return sanitized default arguments when they are valid. 

Sanitized means that, for example, the version is already checked and set depending on our build guidelines. If arguments are not valid, exit the script run. 



**Args:**
 
 - <b>`arguments`</b> (List[str], optional):  List of arguments that are used instead of the arguments passed to the process. Defaults to `None`. 
 - <b>`argument_parser`</b> (arparse.ArgumentParser, optional):  An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. Must be initialized with `add_help=False` flag like argparse.ArgumentParser(add_help=False)! 



**Returns:**
 
 - <b>`Dict[str, Union[str, bool, List[str]]]`</b>:  The parsed default arguments thar are already checked for validity. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_docker_image`

```python
build_docker_image(
    name: str,
    version: str,
    build_args: str = '',
    exit_on_error: bool = False
) → CompletedProcess
```






---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_docker.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `release_docker_image`

```python
release_docker_image(
    name: str,
    version: str,
    docker_image_prefix: str = '',
    exit_on_error: bool = False
) → CompletedProcess
```

Push a Docker image to a repository. 



**Args:**
 
 - <b>`name`</b> (str):  The name of the image. Must not be prefixed! 
 - <b>`version`</b> (str):  The tag used for the image. 
 - <b>`docker_image_prefix`</b> (str, optional):  The prefix added to the name to indicate an organization on DockerHub or a completely different repository. Defaults to "". 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 



**Returns:**
 
 - <b>`subprocess.CompletedProcess`</b>:  Returns the CompletedProcess object of the `docker push ...` command. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

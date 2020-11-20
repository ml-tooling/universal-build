<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.build_utils`




**Global Variables**
---------------
- **ALLOWED_BRANCH_TYPES_FOR_RELEASE**
- **MAIN_BRANCH_NAMES**
- **FLAG_MAKE**
- **FLAG_TEST**
- **FLAG_TEST_MARKER**
- **FLAG_RELEASE**
- **FLAG_VERSION**
- **FLAG_CHECK**
- **FLAG_RUN**
- **FLAG_SKIP_PATH**
- **FLAG_FORCE**
- **FLAG_SANITIZED**
- **TEST_MARKER_SLOW**
- **EXIT_CODE_GENERAL**
- **EXIT_CODE_INVALID_VERSION**
- **EXIT_CODE_NO_VERSION_FOUND**
- **EXIT_CODE_VERSION_IS_REQUIRED**
- **EXIT_CODE_DEV_VERSION_REQUIRED**
- **EXIT_CODE_DEV_VERSION_NOT_MATCHES_BRANCH**
- **EXIT_CODE_INVALID_ARGUMENTS**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `log`

```python
log(message: str) → None
```






---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 
 - <b>`arguments`</b> (List[str], optional):  List of arguments that are used instead of the arguments passed to the process. Defaults to None. 
 - <b>`argument_parser`</b> (arparse.ArgumentParser, optional):  An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. Must be initialized with `add_help=False` flag like argparse.ArgumentParser(add_help=False)! 



**Returns:**
 
 - <b>`Dict[str, Union[str, bool, List[str]]]`</b>:  The parsed default arguments thar are already checked for validity. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `concat_command_line_arguments`

```python
concat_command_line_arguments(
    args: Dict[str, Union[str, bool, List[str]]]
) → str
```






---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_git_tag`

```python
create_git_tag(
    version: str,
    push: bool = False,
    force: bool = False
) → CompletedProcess
```

Create an annotated git tag in the current HEAD via `git tag` and the provided version. 

The version will be prefixed with 'v'. If push is set, the tag is pushed to remote but only if the previous `git tag` command was successful. 



**Args:**
 
 - <b>`version`</b> (str):  The tag to be created. Will be prefixed with 'v'. 
 - <b>`push`</b> (bool, optional):  If true, push the tag to remote. Defaults to False. 
 - <b>`force`</b> (bool, optional):  If true, force the tag to be created. Defaults to False. 



**Returns:**
 
 - <b>`subprocess.CompletedProcess`</b>:  Returns the CompletedProcess object of either the `git tag` or the `git push tag` command. If `push` is set to true, the CompletedProcess of `git tag` is returned if it failed, otherwise the CompletedProcess object from the `git push tag` command is returned. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build`

```python
build(component_path: str, args: Dict[str, Union[str, bool, List[str]]]) → None
```

Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths. 



**Args:**
 
 - <b>`component_path`</b> (str):  The path of the component to be built. The path must contain a build.py file. 
 - <b>`args`</b> (Dict):  The arguments to be passed to the component's build.py file. The default arguments that were used to call this  script are passed down to the component. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run`

```python
run(
    command: str,
    disable_stdout_logging: bool = False,
    disable_stderr_logging: bool = False,
    exit_on_error: bool = False,
    timeout: Optional[int] = None
) → CompletedProcess
```

Run a specified command. 



**Args:**
 
 - <b>`command`</b> (str):  The shell command that is executed via subprocess.Popen. 
 - <b>`disable_stdout_logging`</b> (bool):  Disable stdout logging when it is too much or handled by the caller. 
 - <b>`exit_on_error`</b> (bool):  Exit program if the exit code of the command is not 0. 
 - <b>`timeout`</b> (Optional[int]):  If the process does not terminate after timeout seconds, raise a TimeoutExpired exception. 



**Returns:**
 
 - <b>`subprocess.CompletedProcess`</b>:  State 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `exit_process`

```python
exit_process(code: int = 0) → None
```

Exit the process with exit code. 

`sys.exit` seems to be a bit unreliable, process just sleeps and does not exit. So we are using os._exit instead and doing some manual cleanup. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Version`





<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(major: int, minor: int, patch: int, suffix: str)
```







---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_version_from_string`

```python
get_version_from_string(version: str) → Union[ForwardRef('Version'), NoneType]
```





---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_valid_version_format`

```python
is_valid_version_format(version: str) → Union[Match[str], NoneType]
```





---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_string`

```python
to_string() → str
```






---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L527"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `VersionInvalidFormatException`





### <kbd>method</kbd> `__init__`

```python
__init__(*args, **kwargs)
```

Initialize self.  See help(type(self)) for accurate signature. 




---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L531"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `VersionInvalidPatchNumber`





### <kbd>method</kbd> `__init__`

```python
__init__(*args, **kwargs)
```

Initialize self.  See help(type(self)) for accurate signature. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

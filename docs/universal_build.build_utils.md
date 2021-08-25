<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.build_utils`
Universal build utilities. 

**Global Variables**
---------------
- **FLAG_MAKE**
- **FLAG_TEST**
- **FLAG_TEST_MARKER**
- **FLAG_RELEASE**
- **FLAG_VERSION**
- **FLAG_CHECK**
- **FLAG_RUN**
- **FLAG_FORCE**
- **TEST_MARKER_SLOW**
- **EXIT_CODE_GENERAL**
- **EXIT_CODE_INVALID_VERSION**
- **EXIT_CODE_NO_VERSION_FOUND**
- **EXIT_CODE_VERSION_IS_REQUIRED**
- **EXIT_CODE_DEV_VERSION_REQUIRED**
- **EXIT_CODE_DEV_VERSION_NOT_MATCHES_BRANCH**
- **EXIT_CODE_INVALID_ARGUMENTS**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `log`

```python
log(message: str) → None
```

Log message to stdout. 



**Args:**
 
 - <b>`message`</b> (str):  Message to log. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `command_exists`

```python
command_exists(
    command: str,
    silent: bool = False,
    exit_on_error: bool = False
) → bool
```

Checks whether the `command` exists and is marked as executable. 



**Args:**
 
 - <b>`command`</b> (str):  Command to check. 
 - <b>`silent`</b> (bool):  If `True`, no message will be logged in case the command does not exist. Default is `False`. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if the command does not exist. Defaults to `False`. 



**Returns:**
 
 - <b>`bool`</b>:  `True` if the commend exist and is executable. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 
 - <b>`input_args`</b> (List[str], optional):  List of arguments that are used instead of the arguments passed to the process. Defaults to None. 
 - <b>`argument_parser`</b> (arparse.ArgumentParser, optional):  An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. 



**Returns:**
 
 - <b>`dict`</b>:  The parsed default arguments thar are already checked for validity. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_git_tag`

```python
create_git_tag(
    version: str,
    push: bool = False,
    force: bool = False,
    exit_on_error: bool = False
) → CompletedProcess
```

Create an annotated git tag in the current HEAD via `git tag` and the provided version. 

The version will be prefixed with 'v'. If push is set, the tag is pushed to remote but only if the previous `git tag` command was successful. 



**Args:**
 
 - <b>`version`</b> (str):  The tag to be created. Will be prefixed with 'v'. 
 - <b>`push`</b> (bool, optional):  If true, push the tag to remote. Defaults to False. 
 - <b>`force`</b> (bool, optional):  If true, force the tag to be created. Defaults to False. 
 - <b>`exit_on_error`</b> (bool):  Exit program if the tag creation fails. 



**Returns:**
 
 - <b>`subprocess.CompletedProcess`</b>:  Returns the CompletedProcess object of either the `git tag` or the `git push tag` command. If `push` is set to true, the CompletedProcess of `git tag` is returned if it failed, otherwise the CompletedProcess object from the `git push tag` command is returned. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build`

```python
build(component_path: str, args: Dict[str, Union[str, bool, List[str]]]) → None
```

Run the build logic of the specified component, except if the path is a (sub-)path in skipped-paths. 



**Args:**
 
 - <b>`component_path`</b> (str):  The path of the component to be built. The path must contain a build.py file. 
 - <b>`args`</b> (Dict):  The arguments to be passed to the component's build.py file. The default arguments that were used to call this  script are passed down to the component. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L343"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run`

```python
run(
    command: str,
    disable_stdout_logging: bool = False,
    disable_stderr_logging: bool = False,
    exit_on_error: bool = True,
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

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L403"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `exit_process`

```python
exit_process(code: int = 0) → None
```

Exit the process with exit code. 

`sys.exit` seems to be a bit unreliable, process just sleeps and does not exit. So we are using os._exit instead and doing some manual cleanup. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L418"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `replace_in_files`

```python
replace_in_files(
    find: str,
    replace: str,
    file_paths: List[str],
    regex: bool = False,
    exit_on_error: bool = True
) → None
```

Replaces a string or regex occurence in a collection of files. 



**Args:**
 
 - <b>`find`</b> (str):  A string to find and replace in the files. 
 - <b>`replace`</b> (str):  The string to replace it with. 
 - <b>`file_paths`</b> (List[str]):  Collection of file paths. 
 - <b>`regex`</b> (bool, optional):  If `True`, apply the find string as a regex notation. Defaults to `False`. 
 - <b>`exit_on_error`</b> (bool, optional):  If `True`, exit process as soon as error occures. Defaults to True. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L459"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_latest_version`

```python
get_latest_version() → Union[str, NoneType]
```

Returns the latest version based on Git tags. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L469"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `duplicate_folder`

```python
duplicate_folder(
    src_path: str,
    target_path: str,
    preserve_target: bool = False,
    exit_on_error: bool = True
) → bool
```

Deprecated. Use `build_utils.copy` instead. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/build_utils.py#L479"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `copy`

```python
copy(
    src_path: str,
    target_path: str,
    preserve_target: bool = False,
    exit_on_error: bool = True
) → bool
```

Copy the files from source to target. 

Depending on the mode, it will either completely replace the target path with the source path or it will copy all files of the source directory to the target directory. If `preserve_target` is `True`, if a file or directory with the same name exists at the target, it will be deleted first. Required directories will be created at the target so that the structure is preserved. 



**Example:**
 ```
copy(
     source_path="./temp/generated-openapi-client/src/",
     target_path="./webapp/src/services/example-client/"
)
``` 



**Args:**
 
 - <b>`src_path`</b> (str):  Source path to duplicate. 
 - <b>`target_path`</b> (str):  Target path to move the source folder.  The existing content in the folder will be deleted. 
 - <b>`preserve_target`</b> (bool, optional):  If `True`, the files/directories of the source target will be put into the target path instead of replacing the target directory. 
 - <b>`exit_on_error`</b> (bool, optional):  If `True`, exit process as soon as error occures. Defaults to True. 



**Returns:**
 
 - <b>`bool`</b>:  Returns `True` if the copy process was successful and `False` otherwise; if `exit_on_error` is True, the process exists instead of returning `False`. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

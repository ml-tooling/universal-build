<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.helpers.build_python`




**Global Variables**
---------------
- **FLAG_PYPI_TOKEN**
- **FLAG_PYPI_REPOSITORY**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `test_with_py_version`

```python
test_with_py_version(python_version: str, exit_on_error: bool = True) → None
```

Run pytest in a environment wiht the specified python version. 



**Args:**
 
 - <b>`python_version`</b> (str):  Python version to use inside the virutal environment. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `install_build_env`

```python
install_build_env() → None
```

Installs a new virtual environment via pipenv. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_api_docs`

```python
generate_api_docs(
    github_url: str,
    main_package: str,
    command_prefix: str = 'pipenv run',
    exit_on_error: bool = True
) → None
```

Generates API documentation via lazydocs. 



**Args:**
 
 - <b>`github_url`</b> (str):  Github URL 
 - <b>`main_package`</b> (str):  The main package name to use for docs generation. 
 - <b>`command_prefix`</b> (str, optional):  Prefix to use for all commands. Defaults to `pipenv run`. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `publish_pypi_distribution`

```python
publish_pypi_distribution(
    pypi_token: str,
    pypi_user: str = '__token__',
    pypi_repository: Optional[str] = None
) → None
```

Publish distribution to pypi. 



**Args:**
 
 - <b>`pypi_token`</b> (str):  Token of PyPi repository. 
 - <b>`pypi_user`</b> (str, optional):  User of PyPi repository. Defaults to "__token__". 
 - <b>`pypi_repository`</b> (Optional[str], optional):  PyPi repository. If `None` provided, use the production instance. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `code_checks`

```python
code_checks(
    command_prefix: str = 'pipenv run',
    black: bool = True,
    isort: bool = True,
    pydocstyle: bool = True,
    mypy: bool = True,
    flake8: bool = True,
    safety: bool = True,
    exit_on_error: bool = True
) → None
```

Run linting and style checks. 



**Args:**
 
 - <b>`command_prefix`</b> (str, optional):  Prefix to use for all check commands. Defaults to `pipenv run`. 
 - <b>`black`</b> (bool, optional):  Activate black formatting check. Defaults to True. 
 - <b>`isort`</b> (bool, optional):  Activate isort import sorting check. Defaults to True. 
 - <b>`pydocstyle`</b> (bool, optional):  Activate pydocstyle docstring check. Defaults to True. 
 - <b>`mypy`</b> (bool, optional):  Activate mypy typing check. Defaults to True. 
 - <b>`flake8`</b> (bool, optional):  Activate flake8 linting check. Defaults to True. 
 - <b>`safety`</b> (bool, optional):  Activate saftey check via pipenv. Defaults to True. 
 - <b>`exit_on_error`</b> (bool, optional):  If `True`, exit process as soon as error occures. Defaults to True. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `update_version`

```python
update_version(module_path: str, version: str) → None
```

Update version in specified module. 



**Args:**
 
 - <b>`module_path`</b> (str):  Python module with a `__version__` attribute. 
 - <b>`version`</b> (str):  New version number to write into `__version__` attribute. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_python.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_distribution`

```python
build_distribution() → None
```

Build python package distribution. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

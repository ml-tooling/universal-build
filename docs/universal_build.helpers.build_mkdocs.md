<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.helpers.build_mkdocs`
Utilities to help building MkDocs documentations. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `install_build_env`

```python
install_build_env(exit_on_error: bool = True) → None
```

Installs a new virtual environment via pipenv. 



**Args:**
 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `lint_markdown`

```python
lint_markdown(markdownlint: bool = True, exit_on_error: bool = True) → None
```

Run markdownlint on markdown documentation. 



**Args:**
 
 - <b>`markdownlint`</b> (bool, optional):  Activate markdown linting via `markdownlint`. Defaults to `True`. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_mkdocs`

```python
build_mkdocs(exit_on_error: bool = True) → None
```

Build mkdocs markdown documentation. 



**Args:**
 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `deploy_gh_pages`

```python
deploy_gh_pages(exit_on_error: bool = True) → None
```

Deploy mkdocs documentation to Github pages. 



**Args:**
 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run_dev_mode`

```python
run_dev_mode(port: int = 8001, exit_on_error: bool = True) → None
```

Run mkdocs development server. 



**Args:**
 
 - <b>`port`</b> (int, optional):  Port to use for mkdocs development server. Defaults to 8001. 
 - <b>`exit_on_error`</b> (bool, optional):  Exit process if an error occurs. Defaults to `True`. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

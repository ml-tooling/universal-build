<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.helpers.build_mkdocs`
Utilities to help building MkDocs documentations. 

**Global Variables**
---------------
- **PIPENV_RUN**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `install_build_env`

```python
install_build_env() → None
```

Installs a new virtual environment via pipenv. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `lint_markdown`

```python
lint_markdown() → None
```

Run markdownlint on markdown documentation. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_mkdocs`

```python
build_mkdocs(command_prefix: str = 'pipenv run') → None
```

Build mkdocs markdown documentation. 



**Args:**
 
 - <b>`command_prefix`</b> (str, optional):  Prefix to use for all commands. Defaults to `pipenv run`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `deploy_gh_pages`

```python
deploy_gh_pages(command_prefix: str = 'pipenv run') → None
```

Deploy mkdocs documentation to Github pages. 



**Args:**
 
 - <b>`command_prefix`</b> (str, optional):  Prefix to use for all commands. Defaults to `pipenv run`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/build_mkdocs.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run_dev_mode`

```python
run_dev_mode(port: int = 8001, command_prefix: str = 'pipenv run') → None
```

Run mkdocs development server. 



**Args:**
 
 - <b>`port`</b> (int, optional):  Port to use for mkdocs development server. Defaults to 8001. 
 - <b>`command_prefix`</b> (str, optional):  Prefix to use for all commands. Defaults to `pipenv run`. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

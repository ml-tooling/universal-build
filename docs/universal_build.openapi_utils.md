<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/openapi_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.openapi_utils`
OpenAPI utilities. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/openapi_utils.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_openapi_client`

```python
generate_openapi_client(
    openapi_spec_file: str,
    swagger_target_language: str,
    swagger_additional_properties: str = '',
    temp_dir: str = '/temp',
    swagger_codegen_cli_path: str = None
) → Union[str, NoneType]
```

Generate an open api client. 

The passed OpenAPI specification file will be taken to generate a client using swagger for the given programming language and optional swagger properties (see the swagger cli for more information). The client will be generated at the passed `temp_dir` directory. 



**Args:**
 
 - <b>`openapi_spec_file`</b> (str):  The OpenAPI specification for which the client will be generated. 
 - <b>`swagger_target_language`</b> (str):  The client's programming language (e.g. `"javascript"`). 
 - <b>`swagger_additional_properties`</b> (str, optional):  Additional properties passed to the swagger client (e.g. `"useES6=true"`) 
 - <b>`temp_dir`</b> (str, optional):  The directory in which the generated client will be placed. If it does not exist, it will be created. 
 - <b>`swagger_codegen_cli_path`</b> (str, optional):  The function requires the Java swagger codegen cli to generate the client. If no path is provided, it will try downloading it according to the `_check_and_download_swagger_cli` function. 



**Returns:**
 
 - <b>`Union[str, None]`</b>:  Returns the output path if the client generation was successful and None otherwise. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/openapi_utils.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_openapi_js_client`

```python
generate_openapi_js_client(
    openapi_spec_file: str,
    temp_dir: str = '/temp'
) → Union[str, NoneType]
```

Calls `generate_openapi_client` to generate a javascript client with the swagger properties "useES6=true". 

For more information, see `generate_openapi_client`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/openapi_utils.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `copy_openapi_client`

```python
copy_openapi_client(source_dir: str, target_dir: str) → bool
```

Copy the files, e.g. a generated OpenAPI client, from `source_dir` to `target_dir`. 

It will copy all files in the source directory to the target directory. If a file or directory with the same name exists at the target, it will be deleted first. Required directories will be created at the target so that the structure is preserved. 



**Example:**
 ```
copy_openapi_client(
     source_dir="./temp/generated-openapi-client/src/",
     target_dir="./webapp/src/services/example-client/"
)
``` 



**Args:**
 
 - <b>`source_dir`</b> (str):  The source directory from which the files will be copied. 
 - <b>`target_dir`</b> (str):  The target directory to which the files will be copied. 



**Returns:**
 
 - <b>`bool`</b>:  Returns True if the copy process was successful and False otherwise. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

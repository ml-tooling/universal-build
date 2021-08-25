<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/openapi_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `universal_build.helpers.openapi_utils`
OpenAPI utilities. 

**Global Variables**
---------------
- **DEFAULT_TEMP_DIR**

---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/openapi_utils.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_openapi_client`

```python
generate_openapi_client(
    openapi_spec_file: str,
    target_language: str,
    work_dir: str = './temp',
    client_generator: OpenApiGenerator = <OpenApiGenerator.OPENAPI_CODEGEN: ('openapi-generator-cli.jar', 'https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/5.0.1/openapi-generator-cli-5.0.1.jar', 'openapi_client', 'java -jar {cli_path} generate -i {openapi_spec_file} -g {target_language} -o {output_path} {additional_flags} {additional_properties}')>,
    additional_properties: str = '',
    additional_flags: str = ''
) → Union[str, NoneType]
```

Generate an open api client. 

The passed OpenAPI specification file will be taken to generate a client using the passed openapi-generator for the given programming language and optional additional properties (see the respective openapi cli for more information). The client will be generated at the passed `work_dir` directory. 



**Args:**
 
 - <b>`openapi_spec_file`</b> (str):  The OpenAPI specification for which the client will be generated. 
 - <b>`target_language`</b> (str):  The client's programming language (e.g. `"javascript"`). 
 - <b>`work_dir`</b> (str, optional):  The directory in which the generator cli will be looked for and also the generated client will be placed. If it does not exist, it will be created. 
 - <b>`client_generator`</b> (OpenApiGenerator, optional):  The OpenApiGenerator which will be used to generate the client. It will check whether the cli can be found within the `work_dir` directory and if not it will try to download it according to the `_check_and_download_generator_cli` function. 
 - <b>`additional_properties`</b> (str, optional):  Additional properties passed to the OpenAPI generator client client (e.g. `"useES6=true"`) 



**Returns:**
 
 - <b>`Union[str, None]`</b>:  Returns the output path if the client generation was successful and None otherwise. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/openapi_utils.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_openapi_js_client`

```python
generate_openapi_js_client(
    openapi_spec_file: str,
    work_dir: str = './temp',
    client_generator: OpenApiGenerator = <OpenApiGenerator.OPENAPI_CODEGEN: ('openapi-generator-cli.jar', 'https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/5.0.1/openapi-generator-cli-5.0.1.jar', 'openapi_client', 'java -jar {cli_path} generate -i {openapi_spec_file} -g {target_language} -o {output_path} {additional_flags} {additional_properties}')>,
    additional_flags: str = ''
) → Union[str, NoneType]
```

Calls `generate_openapi_client` to generate a javascript client. 

For more information, see `generate_openapi_client`. 


---

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/openapi_utils.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OpenApiGenerator`
Enum of generators that can generate clients based on OpenAPI specifications. 

<a href="https://github.com/ml-tooling/universal-build/blob/main/src/universal_build/helpers/openapi_utils.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    cli_name: str,
    download_url: str,
    client_dir_name: str,
    generate_command: str
)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

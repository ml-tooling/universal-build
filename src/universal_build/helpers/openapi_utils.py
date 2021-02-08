"""OpenAPI utilities."""

import pathlib
from typing import Union

import urllib3

from universal_build import build_utils


def _check_and_download_swagger_cli(file_path: str) -> bool:
    """Checks whether the the `swagger-codegen-cli.jar` tool exists under the given `file_path` and if not, downloads it to that path.

    Args:
        file_path (str): Where the swagger-codegen-cli.jar can be found or will be downloaded to.

    Returns:
        bool: Returns True if the swagger-cli tool was found / successfully downloaded and False otherwise.
    """
    if not pathlib.Path(file_path).is_file():
        swagger_codegen_cli_download_url = "https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.23/swagger-codegen-cli-3.0.23.jar"
        response = urllib3.PoolManager().request(
            "GET", swagger_codegen_cli_download_url
        )
        if response.status == 200:
            with open(file_path, "wb") as f:
                f.write(response.data)
        else:
            return False
    return True


def generate_openapi_client(
    openapi_spec_file: str,
    swagger_target_language: str,
    swagger_additional_properties: str = "",
    temp_dir: str = "./temp",
    swagger_codegen_cli_path: str = None,
) -> Union[str, None]:
    """Generate an open api client.

    The passed OpenAPI specification file will be taken to generate a client using swagger for the given programming language and optional swagger properties (see the swagger cli for more information).
    The client will be generated at the passed `temp_dir` directory.

    Args:
        openapi_spec_file (str): The OpenAPI specification for which the client will be generated.
        swagger_target_language (str): The client's programming language (e.g. `"javascript"`).
        swagger_additional_properties (str, optional): Additional properties passed to the swagger client (e.g. `"useES6=true"`)
        temp_dir (str, optional): The directory in which the generated client will be placed. If it does not exist, it will be created.
        swagger_codegen_cli_path (str, optional): The function requires the Java swagger codegen cli to generate the client. If no path is provided, it will try downloading it according to the `_check_and_download_swagger_cli` function.

    Returns:
        Union[str, None]: Returns the output path if the client generation was successful and None otherwise.
    """
    pathlib.Path(temp_dir).mkdir(exist_ok=True)
    swagger_codegen_cli = (
        swagger_codegen_cli_path or f"{temp_dir}/swagger-codegen-cli.jar"
    )
    is_successful = _check_and_download_swagger_cli(swagger_codegen_cli)
    if not is_successful:
        return None
    output_path = f"{temp_dir}/client"
    if not pathlib.Path(openapi_spec_file).is_file():
        build_utils.log(f"The OpenAPI spec file {openapi_spec_file} does not exist")
        return None

    build_utils.run(
        f"java -jar {swagger_codegen_cli} generate -i {openapi_spec_file} -l {swagger_target_language} -o {output_path} --additional-properties {swagger_additional_properties}"
    )

    return output_path


def generate_openapi_js_client(
    openapi_spec_file: str, temp_dir: str = "./temp"
) -> Union[str, None]:
    """Calls `generate_openapi_client` to generate a javascript client with the swagger properties "useES6=true".

    For more information, see `generate_openapi_client`.
    """
    return generate_openapi_client(
        openapi_spec_file=openapi_spec_file,
        temp_dir=temp_dir,
        swagger_target_language="javascript",
        swagger_additional_properties="useES6=true",
    )
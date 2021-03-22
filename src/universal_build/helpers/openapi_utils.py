"""OpenAPI utilities."""

import pathlib
from enum import Enum
from typing import Union

import urllib3

from universal_build import build_utils

DEFAULT_TEMP_DIR = "./temp"


class OpenApiGenerator(Enum):
    """Enum of generators that can generate clients based on OpenAPI specifications."""

    OPENAPI_CODEGEN = (
        "openapi-generator-cli.jar",
        "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/5.0.1/openapi-generator-cli-5.0.1.jar",
        "openapi_client",
        "java -jar {cli_path} generate -i {openapi_spec_file} -g {target_language} -o {output_path} {additional_flags} {additional_properties}",
    )
    SWAGGER_CODEGEN = (
        "swagger-codegen-cli.jar",
        "https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.23/swagger-codegen-cli-3.0.23.jar",
        "client",
        "java -jar {cli_path} generate -i {openapi_spec_file} -l {target_language} -o {output_path} {additional_flags} {additional_properties}",
    )

    def __init__(
        self,
        cli_name: str,
        download_url: str,
        client_dir_name: str,
        generate_command: str,
    ):
        self.cli_name = cli_name
        self.download_url = download_url
        self.client_dir_name = client_dir_name
        self.generate_command = generate_command

    def get_cli_path(self, work_dir: str = DEFAULT_TEMP_DIR) -> str:
        return f"{work_dir}/{self.cli_name}"

    def get_output_path(self, work_dir: str) -> str:
        return f"{work_dir}/{self.client_dir_name}"

    def get_generate_command(
        self,
        openapi_spec_file: str,
        target_language: str,
        work_dir: str,
        additional_properties: str = None,
        additional_flags: str = "",
    ) -> str:

        if additional_properties:
            additional_properties = f"--additional-properties {additional_properties}"
        else:
            additional_properties = ""

        return self.generate_command.format(
            cli_path=self.get_cli_path(work_dir),
            openapi_spec_file=openapi_spec_file,
            target_language=target_language,
            output_path=self.get_output_path(work_dir=work_dir),
            additional_properties=additional_properties,
            additional_flags=additional_flags,
        )


def _check_and_download_generator_cli(
    codegen_cli_path: str,
    client_generator: OpenApiGenerator = OpenApiGenerator.OPENAPI_CODEGEN,
) -> bool:
    """Checks whether `codegen_cli_path` exists and if not, downloads it to that path using the information from the `client_generator`.

    Args:
        codegen_cli_path (str): Where the cli tool (e.g. openapi-codegen-cli.jar) can be found or will be downloaded to.

    Returns:
        bool: Returns True if `codegen_cli_path` was found or the tool successfully downloaded and False otherwise.
    """
    if not pathlib.Path(codegen_cli_path).is_file():
        response = urllib3.PoolManager().request("GET", client_generator.download_url)
        if response.status == 200:
            with open(codegen_cli_path, "wb") as f:
                f.write(response.data)
        else:
            return False
    return True


def generate_openapi_client(
    openapi_spec_file: str,
    target_language: str,
    work_dir: str = DEFAULT_TEMP_DIR,
    client_generator: OpenApiGenerator = OpenApiGenerator.OPENAPI_CODEGEN,
    additional_properties: str = "",
    additional_flags: str = "",
) -> Union[str, None]:
    """Generate an open api client.

    The passed OpenAPI specification file will be taken to generate a client using the passed openapi-generator for the given programming language and optional additional properties (see the respective openapi cli for more information).
    The client will be generated at the passed `work_dir` directory.

    Args:
        openapi_spec_file (str): The OpenAPI specification for which the client will be generated.
        target_language (str): The client's programming language (e.g. `"javascript"`).
        work_dir (str, optional): The directory in which the generator cli will be looked for and also the generated client will be placed. If it does not exist, it will be created.
        client_generator (OpenApiGenerator, optional): The OpenApiGenerator which will be used to generate the client. It will check whether the cli can be found within the `work_dir` directory and if not it will try to download it according to the `_check_and_download_generator_cli` function.
        additional_properties (str, optional): Additional properties passed to the OpenAPI generator client client (e.g. `"useES6=true"`)

    Returns:
        Union[str, None]: Returns the output path if the client generation was successful and None otherwise.
    """

    pathlib.Path(work_dir).mkdir(exist_ok=True)
    codegen_cli_path = f"{work_dir}/{client_generator.cli_name}"
    is_successful = _check_and_download_generator_cli(
        codegen_cli_path, client_generator=client_generator
    )
    if not is_successful:
        return None
    if not pathlib.Path(openapi_spec_file).is_file():
        build_utils.log(f"The OpenAPI spec file {openapi_spec_file} does not exist")
        return None

    build_utils.run(
        client_generator.get_generate_command(
            openapi_spec_file=openapi_spec_file,
            target_language=target_language,
            work_dir=work_dir,
            additional_properties=additional_properties,
            additional_flags=additional_flags,
        )
    )

    return client_generator.get_output_path(work_dir=work_dir)


def generate_openapi_js_client(
    openapi_spec_file: str,
    work_dir: str = DEFAULT_TEMP_DIR,
    client_generator: OpenApiGenerator = OpenApiGenerator.OPENAPI_CODEGEN,
    additional_flags: str = "",
) -> Union[str, None]:
    """Calls `generate_openapi_client` to generate a javascript client.

    For more information, see `generate_openapi_client`.
    """
    return generate_openapi_client(
        openapi_spec_file=openapi_spec_file,
        work_dir=work_dir,
        target_language="javascript",
        client_generator=client_generator,
        additional_properties="usePromises=true",
        additional_flags=additional_flags,
    )

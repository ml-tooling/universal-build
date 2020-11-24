"""Command line interface."""

import typer

from template_package import api

app = typer.Typer()


@app.command()
def hello(name: str) -> None:
    typer.echo(f"Hello {name}")


@app.command()
def start_api_server(host: str = "0.0.0.0", port: int = 8081) -> None:
    import uvicorn

    typer.echo("Starting API Server.")

    uvicorn.run(
        api.app, host=host, port=port, log_level="info"
    )  # cannot use reload=True anymore


if __name__ == "__main__":
    app()

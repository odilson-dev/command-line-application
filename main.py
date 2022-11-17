import typer
from pathlib import Path
from typing import Optional

app = typer.Typer()


@app.command('run')
def main(extension: str,
         directory: Optional[str] = typer.Argument(None, help=""),
         delete: bool = typer.Option(False, help="Delete found files")):
    """
    Display found files with given extension
    Args:
        delete: bool
        extension: str
        directory: str

    Returns: None

    """
    if directory:
        directory = Path(directory)
    else:
        directory = Path.cwd()

    if not directory.exists():
        typer.secho(f"Sorry! The folder '{directory}' doesn't exist!", fg=typer.colors.RED)
        raise typer.Exit()

    files = list(directory.rglob(f"*.{extension}"))

    if files:
        typer.secho(f"Great! Some files ending with .{extension} were found in {directory.name}",
                    fg=typer.colors.BRIGHT_GREEN)
        for file in files:
            typer.secho(f"{file.name}", fg=typer.colors.BRIGHT_GREEN)
    else:
        typer.secho(f"Sorry! Any files ending with .{extension} were found in {directory.name}",
                    fg=typer.colors.BRIGHT_RED)

    if delete:
        confirm = typer.confirm("Do you really want to remove all files found?")
        if not confirm:
            typer.secho("The deletion is canceled", fg=typer.colors.BLUE)
            raise typer.Exit()
        for file in files:
            file.unlink()
            typer.secho(f"The file {file.name} has been deleted!", fg=typer.colors.BRIGHT_RED)


@app.command()
def search(extension: str):
    """
    Find files with data extensions
    Args:
        extension: str

    Returns: None

    """
    main(extension=extension, directory=None, delete=False)


@app.command()
def delete(extension: str):
    """
    Remove files with data extensions
    Args:
        extension: str

    Returns: None

    """
    main(extension=extension, directory=None, delete=True)


if __name__ == "__main__":
    app()

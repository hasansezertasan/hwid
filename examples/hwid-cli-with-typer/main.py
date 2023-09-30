import typer
from hwid import get_hwid


app = typer.Typer()


@app.command(
    help="HWID Extractor",
    short_help="HWID Extractor",
    hidden=False,
    add_help_option=True,
)
def main():
    """
    HWID Extractor
    """

    hwid = get_hwid()
    typer.echo(f"HWID: {hwid}")

if __name__ == "__main__":
    app()

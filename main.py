import typer
from login import FacebookLogIn

app = typer.Typer()


@app.command()
def login():
    typer.echo("Logging in")

import typer
from login import FacebookLogIn

app = typer.Typer()


@app.command()
def login():
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    facebook.login_2_step()


if __name__ == "__main__":
    app()

import typer
from login import FacebookLogIn
from scraper import FacebookScraper

app = typer.Typer()


@app.command()
def login():
    typer.echo("Logging in")
    facebook = FacebookLogIn()
    facebook.login_2_step()


# TODO add arguments for the command
@app.command()
def scrape():
    facebook = FacebookScraper("zuzia.lipinska.37")
    facebook.pipeline()


if __name__ == "__main__":
    app()

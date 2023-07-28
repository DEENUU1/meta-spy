from dotenv import load_dotenv
from cli.commands import (
    app,
    home,
    version,
    login,
    login_2_step,
    scrape,
    scrape_friend_list,
    scrape_images,
    scrape_recent_places,
)

load_dotenv()

app.command()(home)
app.command()(version)
app.command()(login_2_step)
app.command()(login)
app.command()(scrape)
app.command()(scrape_friend_list)
app.command()(scrape_images)
app.command()(scrape_recent_places)

if __name__ == "__main__":
    app()

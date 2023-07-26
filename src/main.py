from dotenv import load_dotenv
from commands import (
    app,
    home,
    version,
    login,
    login_2_step,
    scrape,
    scrape_friend_list,
    scrape_images,
)

load_dotenv()

app.command()(home)
app.command()(version)
app.command()(login_2_step)
app.command()(login)
app.command()(scrape)
app.command()(scrape_friend_list)
app.command()(scrape_images)

if __name__ == "__main__":
    app()

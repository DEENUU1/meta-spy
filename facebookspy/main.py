from dotenv import load_dotenv
from src.commands import (
    app,
    home,
    version,
    login,
    login_2_step,
    scrape,
    scrape_friend_list,
    scrape_images,
    scrape_recent_places,
    scrape_reels,
    scrape_videos,
    scrape_reviews,
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
app.command()(scrape_reels)
app.command()(scrape_videos)
app.command()(scrape_reviews)


if __name__ == "__main__":
    app()

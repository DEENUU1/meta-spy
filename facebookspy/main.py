from dotenv import load_dotenv
from src.commands import (
    app,
    home,
    version,
    scrape_full_name,
    scrape_full_account,
    scrape_work_and_education,
    scrape_localization,
    scrape_family_member,
    login,
    login_2_step,
    scrape_friend_list,
    scrape_images,
    scrape_recent_places,
    scrape_reels,
    scrape_videos_urls,
    scrape_reviews,
    server,
    server_backend,
    download_all_person_videos,
    download_new_person_videos,
    download_video,
    download_all_person_reels,
    download_new_person_reels,
)

load_dotenv()

app.command()(home)
app.command()(version)
app.command()(login_2_step)
app.command()(login)
app.command()(scrape_friend_list)
app.command()(scrape_images)
app.command()(scrape_recent_places)
app.command()(scrape_reels)
app.command()(scrape_videos_urls)
app.command()(scrape_reviews)
app.command()(scrape_full_name)
app.command()(scrape_full_account)
app.command()(scrape_work_and_education)
app.command()(scrape_localization)
app.command()(scrape_family_member)
app.command()(server)
app.command()(server_backend)
app.command()(download_all_person_videos)
app.command()(download_new_person_reels)
app.command()(download_video)
app.command()(download_all_person_reels)
app.command()(download_new_person_videos)

if __name__ == "__main__":
    app()

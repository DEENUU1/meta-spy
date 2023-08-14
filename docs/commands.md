# Commands

## Basic commands
#### Home
Display basic information about project
```bash
python main.py home 
```

#### Version
Display current version of the project
```bash
python main.py version
```

## Log in
#### 2-step verification
```bash
python main.py login_2_step
```
#### Default log in
```bash
python main.py login
```

## Account scrapers
#### Friend list
```bash
python main.py scrape-friend-list --name <facebook_id>
```
#### Image
Scrape and download images from user's facebook profile
```bash
python main.py scrape-images --name <facebook_id>
```
#### Recent places
```bash
python main.py scrape-recent-places --name <facebook_id>
```
#### Videos
Scrape only urls of videos from user's facebook profile
```bash
python main.py scrape-videos-urls --name <facebook_id>
```
#### Reels
Scrape only urls of reels from user's facebook profile
```bash
python main.py scrape-reels --name <facebook_id>
```
#### Reviews
```bash
python main.py scrape-reviews --name <facebook_id>
```
#### Full name
```bash
python main.py scrape-full-name --name <facebook_id>
```
#### Full account
Scrape full name, work and education, localization, family member
```bash
python main.py full-account --name <facebook_id>
```
#### Work and education
```bash
python main.py scrape-work-and-education --name <facebook_id>
```
#### Localization
```bash
python main.py scrape-localization --name <facebook_id>
```
#### Family member
```bash
python main.py scrape-family-member --name <facebook_id>
```
#### Posts
Scrape post urls from user's facebook profile
```bash
python main.py scrape-posts --name <facebook_id>
```

## Local Web Application
#### Run application using docker
```bash
python main.py server
```
#### Run only fastapi application
```bash
python main.py server-backend
```

## Video downloader
#### All user's videos
This command download all videos based on scraped urls
```bash
python main.py download-all-person-videos --name <facebook_id>
```
#### Only new videos
This command download only not downloaded yet videos
```bash
python main.py download-new-person-videos --name <facebook_id>
```
#### Download single video
This command download single video based on given url
```bash
python main.py download_video --url <facebook_video_url>
```

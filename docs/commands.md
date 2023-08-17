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
python main.py scrape-friend-list <facebook_id>
```
#### Image
Scrape and download images from user's facebook profile
```bash
python main.py scrape-images <facebook_id>
```
#### Recent places
```bash
python main.py scrape-recent-places <facebook_id>
```
#### Videos
Scrape only urls of videos from user's facebook profile
```bash
python main.py scrape-video-urls <facebook_id>
```
#### Reels
Scrape only urls of reels from user's facebook profile
```bash
python main.py scrape-reels <facebook_id>
```
#### Reviews
```bash
python main.py scrape-reviews <facebook_id>
```
#### Full name
```bash
python main.py scrape-full-name <facebook_id>
```
#### Full account
Scrape full name, work and education, localization, family member
```bash
python main.py full-account <facebook_id>
```
#### Work and education
```bash
python main.py scrape-work-education <facebook_id>
```
#### Localization
```bash
python main.py scrape-localization <facebook_id>
```
#### Family member
```bash
python main.py scrape-family-member <facebook_id>
```
#### Posts
Scrape post urls from user's facebook profile
```bash
python main.py scrape-person-posts <facebook_id>
```

Scrape post details (content, number of likes;comments;shares etc) based on previously scraped post urls for specified facebook profile
```bash
python main.py scrape-person-post-details <facebook_id>
```

## Local Web Application
#### Run FastAPI and React application 
App is available under this local url - http://localhost:5173/
```bash
python main.py server
```

#### Run Web Application using Docker 
```bash
python main.py server --d 
```


## Video downloader
#### All user's videos
This command download all videos based on scraped urls
```bash
python main.py download-all-person-videos <facebook_id>
```
#### Only new videos
This command download only not downloaded yet videos
```bash
python main.py download-new-person-videos <facebook_id>
```
#### Download single video
This command download single video based on given url
```bash
python main.py download_video <facebook_video_url>
```

# Commands

## Info!
For user's with default account id in url (https://www.facebook.com/profile.php?id=100063142210972)
some of the scrapers may not work 
- work and education
- contact data
- visited place
- family member 
- recent places
- reviews
- likes 

This issue doesn't occur while facebook account has a custom id in url (https://www.facebook.com/zuck)

I am working on to fix this issue. 

## Basic commands

#### Version
Display current version of the project
```bash
python main.py version
```

## Log in
#### 2-step verification
```bash
python main.py login-2-step
```
#### Default log in
```bash
python main.py login
```

## Account scrapers

#### Basic scraping 
This command allows to scrape history of employment and education, full name, family members, contact data and visited places
```bash
python main.py scrape-basic-data <facebook_id>
```
After running this command use arrows keys to navigate through the list of possible scrapers <br>
- Use Arrow Up/Arrow Down to go Up and Down 
- Use Arrow Right to select scraper 
- User Arrow Left to delete selected scraper

![Basic Scraper Console](https://github.com/DEENUU1/facebook-spy/blob/main/assets/scrapebasicdataconsole.png?raw=true)

#### Full scraping
This command allows to choose all available commands to scrape facebook profile
```bash
python main.py full-scrape <facebook_id>
```
After running this command use arrows keys to navigate through the list of possible scrapers <br>
- Use Arrow Up/Arrow Down to go Up and Down 
- Use Arrow Right to select scraper 
- User Arrow Left to delete selected scraper

![Basic Scraper Console](https://github.com/DEENUU1/facebook-spy/blob/main/assets/fullscrapeconsole.png?raw=true)


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

#### Posts
Scrape post urls from user's facebook profile
```bash
python main.py scrape-person-posts <facebook_id>
```

Scrape post details (content, number of likes;comments;shares etc) based on previously scraped post urls for specified facebook profile
```bash
python main.py scrape-person-post-details <facebook_id>
```

#### Likes
Scrape likes from facebook account 
```bash
python main.py scrape-person-likes <facebook_id> 
```

#### Groups
Scrape groups from facebook account
```bash
python main.py scrape-person-groups <facebook_id>
```

#### Events
Scrape events from facebook account
```bash
python main.py scrape-person-events <facebook_id>
```



## Local Web Application
#### Run FastAPI and React application 
App is available under this local url - http://localhost:5173/

For now running React application without docker is not possible and you can only run FastAPI app with this command.
To run React go to this directory 
```bash
facebookspy/src/server/frontend
```
And use this command 
```bash
npm run dev 
```

```bash
python main.py server
```

#### Run Web Application using Docker 
```bash
python main.py server --d 
```


## Video downloader
Download Videos based on previously scraped urls from facebook profile 
```bash
python main.py download-person-videos <facebook_id>
```
After running this command use arrows keys to navigate through the list of possible scrapers <br>
- Use Arrow Up/Arrow Down to go Up and Down 
- Use Arrow Right to select scraper 
- User Arrow Left to delete selected scraper

![Basic Scraper Console](https://github.com/DEENUU1/facebook-spy/blob/main/assets/downloadvideosconsole.png?raw=true)

Download single video from facebook 
```bash
python main.py download-video <facebook_video_url>
```


## Analitics 
#### Graph
To create a graph of connections between Person objects based on their Friends use this command
```bash
python main.py graph 
```
![Basic Scraper Console](https://github.com/DEENUU1/facebook-spy/blob/main/assets/graph.png?raw=true)


#### Report
Save scraped data for specified Person object to PDF file 
```bash
python main.py report <facebook_id> 
```

#### AI Summary
Use free open source LLM model to create a short summary for specified Person object based on scraped data 
```bash
python main.py summary <facebook_id>
```


## Friend Crawler 
This command works similarly to the command that scrapes data about a given user's friends list. The difference, however, is that after scraping and creating Friend objects, it also creates objects for the CrawlerQueue model and after successfully scraping friends for one user, it proceeds to scraping the list of friends for the next user in the queue.

![Friend crawler schema](https://github.com/DEENUU1/facebook-spy/blob/main/assets/crawlerfriendscheama.png?raw=true)


#### Run crawler
Start crawler for specified facebook account 
```bash
python main.py friend-crawler <facebook_id>
```

#### Display queue
Display all objects available in the queue
```bash
python main.py display-queue
```

#### Delete queue object
Delete specified queue object 
```bash
python main.py delete-queue-object <id>
```

#### Clear queue
Delete all objects from the queue 
```bash
python main.py clear-queue
```
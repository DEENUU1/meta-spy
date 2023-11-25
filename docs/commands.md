# Facebook commands

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

## Log in
#### 2-step verification
```bash
python main.py login-2-step
```
#### Default log in
```bash
python main.py login
```

## Account & Page scrapers
- By default this commands were created to scrape accounts but many of them also works for pages 
- If some option doesn't work for a PAGE there is a note like this "🛑 Page not support"

#### fb-account

```bash
python main.py fb-account <facebook_id> <option_1> <option_2> ...

Options:
--work # Scrape work and education information from the given facebook account
--contact # Scrape contact data from the given facebook account
--location # Scrape location data from the given facebook account
--family # Scrape family members data from the given facebook account
--name # Scrape full name from the given facebook account
--friends # Scrape friends list from the given facebook account 🛑 Page not support
--images # Scrape images from the given facebook account 
--recent # Scrape recent places from the given facebook account 🛑 Page not support
--reels # Scrape urls for reels from the given facebook account
--reviews # Scrape reviews from the given facebook account
--videos # Scrape urls for videos from the given facebook account
--da # Download all videos from the given facebook account
--dn # Download only new videos from the given facebook account
--posts # Scrape all posts from the given facebook account
--details # Scrape details of posts from the given facebook account
--likes # Scrape likes from the given facebook account
--groups # Scrape groups from the given facebook account
--events # Scrape events from the given facebook account
```

##### For example 
```bash
python main.py zuck --work --contact --family --friends
```
## Posts

#### post-details
Scrape post details based on post URL 
- In database Posts scraped based on a given URL are in relation with object Person with ID - "Anonymous"
```bash
python main.py post-details "<post_url>"
```
I recommend to paste post url inside " " to avoid errors 


## Local Web Application
#### Run FastAPI application 
App is available under this local url - http://localhost:8000/

```bash
python main.py server
```


## Video downloader
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

## Search
This command allows to search for: places, pages, person, groups, events, posts 


```bash
python main.py fb-search <"Search Query"> <results> <option_1> <option_2> ... 

Options:
--post # Search for posts based on given query
--results # Number of results 
--people # Search for people based on given query
--group # Search for group based on given query
--place # Search for place based on given query
--event # Search for event based on given query
--page # Search for page based on given query
```

- Search query should be in double " "
- Number of results MUST be an integer 

After running this command you can select which data you would like to scrape 
Result's will be saved in this directory /facebookspy/scraped_data/

#### Example
```bash
python main.py fb-search "Poland" 20 --post --place --event
```

![Search  Scraper Console](https://github.com/DEENUU1/facebook-spy/blob/main/assets/v1_2/search.gif?raw=true)
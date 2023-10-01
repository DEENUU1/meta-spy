# Change log


## Current version: 1.1

## Version history

### 1.1
- Improve local web application 
  - Delete React application
  - Add templates for fastAPI 
  - Display all information about specified Person on a single page
  - Delete docker and docker-compose files 

```bash
python main.py server 
```


### 1.0
- Delete command to run web application without docker 
- Post classification using transformers to check if post content is possitive or negative and save those data to database

```bash
python post-classifier <option>

Options:
--all-posts // Run post classification for all posts from the database
--id // Run post classification for specified post from the database
--person-id // Run post classification for a specified person from the database
```

- Add missing typehints 
- Change the structure of a project 
- Friend crawler (This command works similarly to the command that scrapes data about a given user's friends list. The difference, however, is that after scraping and creating Friend objects, it also creates objects for the CrawlerQueue model and after successfully scraping friends for one user, it proceeds to scraping the list of friends for the next user in the queue.)

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

- Option to scrape multiply users in full-scrape command 

```bash
python main.py full-scrape <facebook_id> <facebook_id> <facebook_id>


```

### 0.9
- Add repository functions to return all data for specified Person object
- Implement LangChain and free Open Source LLM model to create summary for specified Person object based on scraped data
- Add command to create summary
- Add command to save all scraped data and summary to PDF file for specified Person object
- Fix saving events and groups if there is no data
- Disable displaying logs from Selenium in the console 
- Add command to create graph of the connections between Person objects based on their friends 

#### New commands

To create a graph of connections between Person objects based on their Friends use this command
```bash
python main.py graph 
```
![Basic Scraper Console](https://github.com/DEENUU1/facebook-spy/blob/main/assets/graph.png?raw=true)


Save scraped data for specified Person object to PDF file 
```bash
python main.py report <facebook_id> 
```

Use free open source LLM model to create a short summary for specified Person object based on scraped data 
```bash
python main.py summary <facebook_id>
```


### V0.8
- Scrape user's groups
- Scrape user's likes
- Scrape user's Events
- Optimalized scrolling 
- Add number_of_friend field in Person model
- Pytest for all FastAPI endpoints and models 
- Add email and phone_number field to Person model 
- Fix saving full_name field to Person model
- Add scraper for Contact data
- Refactor scrapers to make them simpler
- Create a few commands (more details in commands page) with a drop down list to select which scrapers use

### V0.7
- Scrape facebook posts urls from a facebook account
- Scrape post details (number of likes;comments;shares, content etc.)
- Add information about saving data to database
- FastAPI endpoint to return a list of posts for a give Person object
- React page to display a list of posts for a given Person object
- Refactor commands 
- Display time that was taken to finish pipeline
- Update 'server' command to run FastAPI + React app with or without Docker
```bash
python main.py server --d 
python main.py server 
```
- Add shell script to run React application with Python
- Add Docs website which you are using now 

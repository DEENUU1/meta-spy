# Change log


## Current version: 0.7

## Version history

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

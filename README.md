[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]




<br />
<div align="center">

  <h3 align="center">Facebook Spy</h3>

  <p align="center">
    Scrape user's profile on facebook using CLI app and browse data using local web app.
    <br />
    <br />
    <a href="https://github.com/DEENUU1/OLX-Analytics/issues">Report Bug</a>
    ·
    <a href="https://github.com/DEENUU1/OLX-Analytics/issues">Request Feature</a>
  </p>

  <a href="https://github.com/DEENUU1/">
    <img src="assets/home.png" alt="Logo" >
  </a>
</div>
https://github.com/DEENUU1/facebook-spy/assets/111304236/19032a83-a0f0-4834-9d2c-cb89e504673a

<!-- ABOUT THE PROJECT -->
## About The Project
This project allows to log in using selenium to facebook account (even if you have 2-step verification), 
scrape user information based on a given url address and save data to database and local files.
After that you can browse scraped data, add notes, search more detail in google using local web application.

### Built With
- Python
  - Typer
  - Selenium
- FastAPI 
- React
  - Vite 
- Sqlite
- Docker & docker compose 

## Key Features
- Log in with 2-step verification
- Log in without 2-step verification
- Save cookies to save log in session
- Scrape information like:
  - work and education
  - places
  - full name
  - recent places 
  - videos
    - download videos
  - reels
  - list of friends
  - images
    - downlaod images
  - reviews
- Save scraped data to database
- Local web app (FastAPI + React):
  - Browse scraped data
  - Adding notes in local web app for specified person
  - Automatically search scraped data in google

## Screenshots

<img style="margin-bottom: 20px" src="assets/help.png" alt="home"> 

<img style="margin-bottom: 20px" src="assets/scrapeimage.png" alt="home">

<img style="margin-bottom: 20px" src="assets/fullaccount.png" alt="home">

<img src="assets/scrapefullaccount.png" alt="home">


## Upcoming versions

### v0.6 (In develop)
- Delete and update operations on database  
- Create methods in react app 
- Static page for project with demo etc.

### v0.7 (ideas)
- Scrape:
  - groups
  - music
  - sport
  - movies
  - tv
  - books
  - likes
  - contact data and basic info

<!-- GETTING STARTED -->
## Getting Started

### Installation

First, you need to clone this repository
```bash
git clone https://github.com/DEENUU1/facebook-link-tree.git
```

### Configuration
1. Create dotenv file and add required data 
```bash
cp .env_example .env 
````
2. Then install all requirements
```bash
pip install -r requirements.txt
```
3. Change directory to src and run first command
```bash
# If you have 2-step verification run

python main.py login-2-step

# If you don't have 2-step verification run

python main.py login
```
4. Run command to scrape user's friends list
```bash
python main.py --name <user_id>
```

### Tests
```bazaar
# To run pytest use this command
pytest 
```

### Commands
```bash

# Work dir - facebookspy/

python main.py --help 
# Returns a list of all commands

python main.py home
# Display a home page with information about the application

python main.py version
# Display current version of the app

python main.py login-2-step
# Allows to log in on facebook account with 2-step verification

pyton main.py login
# Allows to log in on facebook account without 2-step verification

python main.py server 
# Run local server to browse scraped data

python main.py scrape-friend-list --name <facebook_id>
# Allows to scrape all friends 

python main.py scrape-images --name <facebook_id>
# Allows to scrape all images and save them locally

python main.py scrape-full-account --name <facebook_id>
# Scrape all basic information from facebook account (family members, full name etc)
  
    python main.py scrape-family-member --name <facebook_id>
    # Scrape family members from specified facebook account

    python main.py scrape-localization --name <facebook_id>
    # Scrape places from facebook account
    
    python main.py scrape-work-and-education --name <facebook_id>
    # Scrape work and education data from facebook account
    
    python main.py scrape-full-name --name <facebook_id>
    # Scrape full name from facebook account
    
python main.py scrape-recent-places --name <facebook_id>
# Scrape recent places from facebook account

python main.py scrape-videos-urls --name <facebook_id>
# Scrape and save to database video urls 

python main.py scrape-and-download-videos --name <facebook_id>
# Scrape, save urls to database and download videos 

python main.py scrape-reels --name <facebook_id>
# Scrape reels from facebook account

python main.py scrape-reviews --name <facebook_id>
# Scrape written reviews from facebook account 

python main.py start-fastapi-server
# Run fastapi server, allows to browse scraped data 


```

<!-- LICENSE -->
## License

Distributed under the Apache-2.0 license. See `LICENSE.txt` for more information.


## Author

- [@DEENUU1](https://www.github.com/DEENUU1)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DEENUU1/facebook-spy.svg?style=for-the-badge
[contributors-url]: https://github.com/DEENUU1/facebook-spy/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DEENUU1/facebook-spy.svg?style=for-the-badge
[forks-url]: https://github.com/DEENUU1/facebook-spy/network/members
[stars-shield]: https://img.shields.io/github/stars/DEENUU1/facebook-spy.svg?style=for-the-badge
[stars-url]: https://github.com/DEENUU1/facebook-spy/stargazers
[issues-shield]: https://img.shields.io/github/issues/DEENUU1/facebook-spy.svg?style=for-the-badge
[issues-url]: https://github.com/DEENUU1/facebook-spy/issues
[license-shield]: https://img.shields.io/github/license/DEENUU1/facebook-spy.svg?style=for-the-badge
[license-url]: https://github.com/DEENUU1/facebook-link-tree/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/kacper-wlodarczyk/

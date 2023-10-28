# Installation


### Download repository using git

```bash
git clone https://github.com/DEENUU1/metaspy.git
```

### Configuration
Create dotenv file and add required data
```bash
cp .env_example .env 
```
Install all requirements
```bash
pip install -r requirements.txt
```
Change directory to metaspy to run commands
```bash
cd metaspy
```

[Check available commands for Facebook](commands.md){ .md-button } <br>

[Check available commands for Instagram](commands2.md){ .md-button}

### Instagram configuration 
To use Instagram scraper go to the .env file and add your sessionid 
To get your sessionid:
1. Go to your browser where you are already logged in to you account 
2. Press F12 and 
3. Go to the "Data" 
4. In the sidebar on your left there is a label "Cookies" and choose cookies for Instagram.
5. Then find sessionid and copy the value. <br>


![GUIDE](https://github.com/DEENUU1/meta-spy/blob/main/assets/instagram/instaguide.png?raw=true)

 

### Tests
```bash
# To run pytest use this command
pytest 
```
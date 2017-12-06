# piTemp

## Installation
1. Install postgresql (On RPi: `sudo apt install postgresql libpq-dev`)
2. Install python3/pip (On RPi: `sudo apt-get install python3-pip`)
3. Clone this repo and switch to the cloned directory
4. Run `sudo pip3 -r requirements.txt` to install all dependencies
5. Create a database + user with access-rights to this db
6. Run `./setup.py` to configure piTemp
7. Setup cronjob for `./cron.py` to automatically save temperatures to db.

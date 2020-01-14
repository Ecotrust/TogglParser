# TogglParser
Scripts to ingest Toggl reports and export Luna Hours

## Installation
### Requirements
* Vagrant
* Virtualbox
* Git

### Get Code On A Clean VM
`cd` to a directory of your choice (likely where you clone other repositories to)
```
git clone https://github.com/Ecotrust/TogglParser.git
cd TogglParser
vagrant up
vagrant ssh
```
You should now be in your new Ubuntu 18.04 VM
```
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-virtualenv virtualenv python3-dev build-essential -y
cd /usr/local/apps/ToggleParser
virtualenv env --python=python3
source /usr/local/apps/TogglParser/env/bin/activate
pip install -r /usr/local/apps/TogglParser/requirements.txt
python manage.py migrate
```

## Setting Up Toggl
* Set your profile up so that 'First day of the week' is Sunday
* If no one on your team has done so already, link up [Asana with Toggl](https://asana.com/apps/toggl)
* Invite teammates to your workspace (if not done already)
* Create client records
   * These should be something like 'project name 1-2345-678-9'
   * everything before the last space will be considered the project name
   * everything after the last space will be considered the project code
   * Toggl cannot support 'Task' codes unless we upgrade to the 'Starter' level
* Associate client records with your Asana projects
* you may need to create Holiday/Sick Leave/PTO project and Client records

## Reporting From Toggl
* Track your time with Toggl, using arbitrary task names and associating all entries with projects
* After you finish your work week, select 'Reports' in the left menu
   * At the top of the report page:
      * select 'Detailed'
      * Click on 'Team' (next to 'Filter By') and make sure you are the only user selected
      * Select the week you wish to export
* In the top right corner, click the 'download' icon (a down arrow pointing at a line)
   * Select 'Download CSV'
   
## Generating your 'Luna-Friendly' Spreadsheet
* Move or copy your downloaded report to the 'input' folder in your cloned git repository (on your host machine)
* open up your terminal inside your VM (`vagrant ssh` in the 'Get Code...' step)
* Activate your virtual environment in your VM
   * `source /usr/local/apps/TogglParser/env/bin/activate`
* Run the parser:
```
python /usr/local/apps/TogglParser/manage.py parse /usr/local/apps/TogglParser/input/YOUR_FILE.csv
```
Your cleaned up report now lives inside your 'input' folder (both on the VM and on your host machine) as 'YOUR_FILE.out.csv' where 'YOUR_FILE' is the name of your original file.


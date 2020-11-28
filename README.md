# A beginning of a bot for Discord

This project was initiated by the participants of the first piscine of 42 Lisboa. This project consists of a Discord bot made for the 42 Lisboa non-official, community-managed server.

## How to bring our baby Moulinette to life 🤖

* [Foreword](#foreword)
* [Install Python v.3.9.0](#install-python-v390)
* [Create an environment in which to run our dear Moulinette](#create-an-environment-in-which-to-run-our-dear-moulinette)
* [Install all dependencies](#install-all-dependencies)
* [Bring our baby Moulinette to life](#bring-our-baby-moulinette-to-life)

### Foreword

These instructions are meant to help people get started and assume you are running on Linux or are using WSL (Windows Subsystem for Linux). If you are on Windows and don't want to run WSL, other options like cygwin and mingwin are available. Alternatively, we recommend you to check Anacond to manage Python environments.

### Install Python v.3.9.0 

To check if you have python v3.9.0 installed, run the command `python3.9 --version`. If you get "Python 3.9.0" as output, congratulations. You have the correct version of python installed.

If however you see "python3.9: command not found" don't panic ~~yet~~. We first need to get "deadsnakes" team PPA on apt's repository list (i.e. we need to add a new place for apt to check for packages). For that, we need to install the add-apt-repository package. To do so, follow these following instruction: 
- Run `sudo apt-get install software-properties-common`. Confirm the installation by pressing 'y' and hit enter
- Run `sudo add-apt-repository ppa:deadsnakes/ppa`. When prompted hit enter to confirm the addition to the list 
- Run `sudo apt update` 
- Run `sudo apt upgrade` (quick sidenote: it's highly recommended to run `sudo apt upgrade` frequently on your system to update all of your packages)

Now, we can finally install Python 3.9. You want to install python3.9 and python3.9-venv. Feel free to install more modules if you want (i.e. python3.9-doc, python3.9-dev, python3.9-distutils, python3.9-lib2to3, python3.9-gdbm, python3.9-tk). You can install Python like any other package. Just run `sudo apt install python3.9 python3.9-venv <other packages>`.

To make sure Python v3.9.0 was installed correctly you can run `python3.9 --version` and "Python 3.9.0" should appear on the screen.

### Create an environment in which to run our dear Moulinette

Now that you have Python 3.9 installed, you can create an environment to run the Moulinette. This step is not required but highly recommended because different Python programs may require different versions of the same library but only one version can be installed at a time. With environments, you can have one version of a library for a program in one environment and a different version of the same library in a different environment.

By now, you should have already cloned the repository to your local machine. If you haven't, go ahead and do it. I'll wait... Done? Great, so first we need to choose a place where to save this environment. A good choice would be the root of repository itself. Navigate to the root of the repository you cloned and run the following command `python3.9 -m venv moulinette`. 

If you decided to call the environement something other than `moulinette` in the previous command, make sure to change the name of the folder ignored by git in the .gitignore file to avoid sending it to GitHub. Per default, this repository is ignoring the folder "moulinette/" so the environment will automatically be ignored by git.

Now you can launch the environment by running `source moulinette/bin/activate`. Every time you want to run the program you'll have to enter this environment in order for it to work. To leave the environment simply type `deactivate`.

### Install all dependencies

To handle dependencies, we use pip. You don't need to worry about installing it because the environment you just set up will provide one for you. Run `moulinette/bin/pip list` to check if the version that was automatically installed is up to date. As of the writing of this file, lastest pip's version is v20.2.4. If you get a warning stating that a new version of pip is available or you see that your current version is older run `moulinette/bin/python -m pip install --upgrade pip`.

Python programs can have a lot of dependencies so we have provided a requirements file to help you download all dependencies easily. Run `moulinette/bin/pip install -r requirements.txt`. Congratulations! You just finished setting up everything and are ready to start programming moulinette.

If during the requirements installation you got a "PEP 517" error, export the variables `export MULTIDICT_NO_EXTENSIONS=1` and `export YARL_NO_EXTENSIONS=1`. Give it another try. 

### Bring our baby Moulinette to life

The hard part is done. Now you can bring the Moulinette to life by typing `moulinette/bin/python bot.py` (assuming that you chose to call the environement "moulinette"). Remember that you need a valid token in a file named 'token.txt' for the bot to connect to Discord.

## Disclaimer

This project has no affiliation with 42 as an entity or organization. The creators and participants do not represent 42 in any way.

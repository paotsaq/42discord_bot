# A beginning of a bot for Discord

This project was initiated by the participants of the first piscine of 42 Lisbon. This project consists of a discord bot made for the 42 Lisbon non-official, community-managed server.

## How to bring our baby Moulinette to life 🤖

* [Foreword](#forword)
* [Install python v.3.9.0](#install-python-v390)
* [Create an environment with which to run our dear Moulinette](#create-an-environment-with-which-to-run-out-dear-moulinette)
* [Install all dependencies](#install-all-dependencies)
* [Bring our baby Moulinette to life](#bring-our-baby-moulinette-to-life)

### Forword

These instruction are meant to help people get started and assume you are running on linux or are using WSL (Windows Subsystem for Linux). If you are on Windows and don't want to run wsl, other options like cygwin and mingwin are available. Alternatively we recomand you to check Anacond to manage python environments.

### Install python v.3.9.0 

To check if you have python v3.9.0 installed you can run the command `python3.9 --version`.	If you get "Python 3.9.0" as output congratulation. You have the correct version of python installed.
<!-- TODO: add cmd `sudo apt-get install software-properties-common` -->
If however you see "python3.9: command not found" don't panic ~~yet~~. We need to first get "deadsnakes" team PPA on apt's repository list (This means we need to add a new place for apt to check for packages). For that we need to first install the add-apt-repository package. Simply run `sudo apt-get install software-properties-common`. Confirm the instalation by pressing 'y' and hit enter. You can now run `sudo add-apt-repository ppa:deadsnakes/ppa`. When prompted hit enter to confirm the addition to the list. After adding the new repository run `sudo apt update` (optionally you may want to run `sudo apt upgrade` to make sure all you packages are up to date).

Now we can finaly install python. You want to install python3.9 and python3.9-venv. Fell free to install more modules if you want (i.e. python3.9-doc, python3.9-dev, python3.9-distutils, python3.9-lib2to3, python3.9-gdbm, python3.9-tk). You can install python like any other package. Just run `sudo apt install python3.9 python3.9-venv <other packages>`

To make sure python v3.9.0 was installed correctly you can run `python3.9 --version` and "Python 3.9.0" should appear on the screen.

### Create an environment with which to run our dear Moulinette

Now that you have python installed you can create an environment to run moulinette. This step is not required but highly recomanded because different python programs may require diferent version of the same libray but only one version can be installed at a time. With environments you can have one version of a library for a program on one evironment and a different version of the same library on a diferent evironemt.

By now you should have already cloned the repository to your local machine. If you haven't go ahead and do it. I'll wait... Done? Ok so first we need to choose a place to save this environment. A good choice would be the repository. Just make sure to not send it to the remote when pushing any changes. Navigate to the repository you cloned and run the following command `python3.9 -m venv moulinette`. This repository is ignoring the folder "moulinette/" so the environment will automatically ignored by git. If you want to change the environment's name you can replace "moulinette" in the command by whatever you want but make sure not to push it to the remote.

Now you can launch the environment by running `source moulinette/bin/activate`. Every time you want to run the program you'll have to enter this environment in order for it to work. To leave the environment simply type `deactivate`.

### Install all dependencies

To handle dependencies we use pip. You don't need to worry about installing it because the environment you just set up will provide one for you. Run `moulinette/bin/pip list` to check if the one that was installed automatically is up to date. If you get a warning stating that a new version of pip is available run `moulinette/bin/python -m pip install --upgrade pip`. Python programs can have a lot of dependencies so we have provided a requirements file to help you download all dependencies easily. Run `moulinette/bin/pip install -r requirements.txt`

### Bring our baby Moulinette to life

## Disclaimer

This project has no afilliation with 42 as an entity or organization. The creators and participants do not represent 42 in any way.

<!-- * Run `python3 -m pip install -r requirements.txt` to download the dependencies
* Run `source discord_env/bin/activate` at the root of the repo.
* `python3 bot.py` -->

<!-- That should wake Moulinette up. Be careful as there is a *personal token* inside the main.py file (yes, I know this is bad practice). It is also needed to manually add the bot to any server you wish.  -->

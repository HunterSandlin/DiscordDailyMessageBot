# Discord Daily Message Bot
## Discord bot for sending a daily message of random tasks to a user. Written in python using [discord.py](https://discordpy.readthedocs.io/en/latest/). 

This bot is made to give the user randomly assigned tasks each day. You decide what the tasks could be and how likely it should be to be selected and once a day the bot will message you on discord with two of them. For me, I have plenty of projects I could be working on but I always focus on one and quickly forget old ones. By having a couple selected for me each day, I feel more obligated to work on them. Plus it's fun to see what your tasks for the day are and being forced to regularly change things up.

The bot works by adding it to a Discord server you own (or making a new one just for it) and running a python script locally or on a server. You set your defaults in the config file but can then changes options in memory by talking to the bot over the server with commands. 


# Set up
## Install python3
This bot requies python 3.5.3 or newer. You can see if it is installed by opening a terminal or command prompt and typing 

``python --version`` 

if that does not work, try

``python3 --verion``

If neither of those work you will most likely have to [install python](https://www.python.org/downloads/). If your python is older than version 3.5.3 you will have to update python.

## Install discord.py
Before you can use this bot you have to install discord.py. This bot is writen in discord.py Rewrite so be sure you are not using an older version. For an up to day installation guide, reference the offical [discord.py documentation](https://discordpy.readthedocs.io/en/latest/intro.html).

## Set up bot on Discord
1. To set up the bot on the server, go to https://discord.com/developers/applications
There you will be asked to login to your Discord account. 

2. From there, select **New Application in the top write corner**, give it a name, and click **Create**.

3. On the server, go to the **Bot** tab on the side bar. On that screen click **Add Bot**.

4. You shold now have a bot created, scroll down to the card labeled **Bot Permissions**. The permissions you give is up to you but at a minimum you must include **Send Messages**, **Read Message History**, and **View Channels**. 

5. Scroll back up to the top and click **Copy** under the **Token**. This will copy the bot's token to your clipboard, which you will use in the next step.

## Set up Code
1. First [clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) this repository. 

2. Rename `ex-config.yaml` to `config.yaml`

3. On the second line of `config.yaml`, replace *YOUR_TOKEN_HERE* with your bot's token. It is important that you do not share this token with anyone or upload it online to ensure safety. 

4. Further down in that file, you will see a **tasks** section with examples of messages the bot can send you. The numbers represent the likelyhood of those tasks being pulled. For exapmle, *Common (lvl4)-ONE* if 4x more likely to be picked than "Rare (1) Example." Add the tasks you would like here. 
     - You can update these in memory later. 

5. TODO: Set time to message **not yet implemented** and number of messages **not yet implemented**

## Run bot
To run the bot, simply run the python script. You can do this this by navigating to the directory in a terminal or command prompt and typying:

```python3 DailyMessageBot.py```

As long as the script is running, the bot will be active. It is easiest to keep it running is to have it [run on a sever](https://techwithtim.net/tutorials/discord-py/hosting-a-discord-bot-for-free/).

# Command List
You can use these commands to talk to the bot on it's server. All commands are prefaced with "dmb" and a space. 

  **addUser** --------- takes list of users mentioned with an @; adds users to list of who to send daily messages.

  ex. ```dmb addUser @johnsmith @janedoe``` 

  **echo** ------------ takes a string; sends string back to you.

  ex. ```dmb Hello World```

  **getUsers**  ------- takes no arguments; responds with list of all users added.

  ex. ```dmb getUsers```

  **help**   ---------- takes no arguments; responds with list of all commands.

  ex. ```dmb help```

  **ping** ------------ takes no arguments; responds with "pong".

  ex. ```dmb ping```

  **removeUser**   ---- takes list of users mentioned with an @; removes users from list of who to send daily messages.

  ex. ```dmb removeUser @johnsmith @janedoe```  

  **setNumTasks** ----- takes one integer; sets number of tasks that will be sent each day.

  ex. ```dmb setNumTasks 3```

  **testTasks** ------- takes no arguments; messages users with random tasks.

  ex. ```dmb testTasks```

  **viewTasks** ------- takes no arguments; sends all tasks and their corresponding weights.

  ex. ```dmb viewTasks``` 

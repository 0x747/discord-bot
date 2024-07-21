# Table of Contents

1. [PREREQUISITES](#prerequisites)
   - [CREATE A NEW BOT](#create-a-new-bot)
   - [INSTALLING DEPENDENCIES](#installing-dependencies)
2. [RUNNING THE BOT](#running-the-bot)
3. [USING THE BOT](#using-the-bot)
   - [MODERATION COMMANDS](#moderation-commands)
   - [MUSIC COMMANDS](#music-commands)
   - [MISCELLANEOUS COMMANDS](#miscellaneous-commands)

# Prerequisites

## Create a new bot


1. Head over to the [Discord developer portal](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) and log in.

2. Click "New Application" and give a name to your new bot/app.

3. Click on your bot and head over to the "Bot" tab.

4. In the Bot section click on "Copy", "View Token", or "Reset Token" to get your token and save it to a secure file. DO NOT SHARE YOUR BOT TOKEN.

5. In the "Privileged Gateway Intents" subsection make sure to enable the following.
   - Server Members Intents
   - Message Content Intents

6. Click on the "OAuth2" tab.

7. Go to the "OAuth2 URL Generator" section.

8. For scope, tick "bot".

9. For permissions either tick "Administrator" (recommended) or the following.
    - General Permissions
      - Manage Roles 
      - Kick Members
      - Ban Members
      - Change Nicknames
      - Manage Nicknames
      - Read Message/View Channels
      - Moderate Members
    - Text Permissions
      - Send Messages
      - Manage Messages
      - Embed Links
      - Attach Files
      - Read Message History
    - Voice Permissions
      - Connect
      - Speak

10. Scroll down and copy the "Generate URL" and paste it into your browser. It'll ask you to pick a server to invite your bot to. 

## Installing Dependencies

#### 1. Install the base library
```
pip install -U discord.py
```

#### 2. For voice support use the following command (For Linux based systems, see step 3)
```
pip install -U discord.py[voice]
```

#### 3. Following dependencies are **required** on Linux based systems for voice support
- [libffi](https://github.com/libffi/libffi)
- [libnacl](https://github.com/saltstack/libnacl)
- [python3-dev](https://packages.debian.org/search?keywords=python3-dev)

#### Use the following command on Debian based systems
```
sudo apt install libffi-dev libnacl-dev python3-dev
```

#### 4. To play audio from YouTube you must install ```yt-dlp```. You may skip this step.
```
pip install yt-dlp
```

#### NOTE: If these steps do not work please refer to the [official documentation](https://discordpy.readthedocs.io/en/stable/intro.html)


# Running the bot

1. Open ```main.py``` and paste your bot token inside the ```bot.start()``` method.
```py
await bot.start("your token here")
```

2. Execute ```main.py``` using the Python interpreter.
```
python3 main.py
```

You should see an output similar to the one given below. Your bot's status should change to online now.
```
bot123 has logged in at 2024-07-21 13:33:59.363232
Member Cog Loaded.
Admin Cog Loaded.
```

# Using the bot

The default command prefix is ```>```. You may change it or specify multiple prefixes in ```main.py```
```py
bot = commands.Bot(command_prefix=[">", "$", "!"], intents=intents)
```

## Available Commands 

You can use ```>help``` command to get a list of all commands with a brief description for each. 

### Moderation Commands
| Command | Description | Usage |
|---------|-------------|-------|
| ban {user} [reason] | Bans a given user from the server with an optional reason | `>ban @user not following rules` |
| unban {username} | Unbans a given user using their username given in plaintext | `>unban username` |
| kick {user} [reason] | Kicks a given user from the server with an optional reason | `>kick @user for being annoying` |
| rename {user} {new name} | Changes a user's display name/nickname | `>rename @user awesome user` |
| whois {user or user id} | Shows a user's information such as pfp and creation date | `>whois @user or 1234567890876542` |
| give {role} {user} | Gives a specified role to the given user | `>give @user @some_role` |
| remove {role} {user} | Removes a specified role from the given user | `>remove @user @some_role` |
| clear {amount} | Deletes the specified amount of messages from the channel. Default amount is 1 | `>clear 7` |
| reboot | Reboots the bot and applies new changes. Bot will be offline for a few seconds | `>reboot` |

### Music Commands 
| Command | Description | Usage |
|---------|-------------|-------|
| ls | Lists the filenames in the music directory with their indexes | `>ls` |
| play {name or index} | Plays the specified file from the local filesystem. | `>play favorite song or 7` |
| yt {name or YouTube url} | Plays the specified audio from YouTube | `>yt home resonance or www.youtube.com/watch?v=dQw4w9WgXcQ` |
| pause | Pauses the audio playback | `>pause` |
| resume | Resumes the audio playback | `>resume` |
| stop | Stops the audio playback | `>stop` |
| join | To manually have bot join the same voice channel the author is in. | `>join` |
| disconnect | Disconnects the bot from the voice channel | `>disconnect` |

### Miscellaneous Commands
| Command | Description | Usage |  
|---------|-------------|-------|
| flip | Flips a coin | `>flip` |
| imdb {title or IMDb url/tag} | Fetches IMDb metadata for a given movie/show | `>imdb the matrix or www.imdb.com/title/tt0133093 or tt0133093` |
| random {lower bound} {upper bound} | Picks a number between the lower and upper bound. Default values are 0 and 100. | `>random 1 10` |

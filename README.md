# VHBot
A Discord bot made to make Discord more like a virtual classroom.

## Usage and features

### Start a "raise your hand" event

    {cmd_prefix}q

The bot renames the people who react to his message with the raised hand emoji and they are brought up in the voice channel (by adding a dot before their nickname). When people stop *virtually* raising their hand (either by removing the reaction or stopping the event), the bot renames them to their previous nickname. 

Moreover, the bot cleans request messages and his messages itself so the tchat doesn't get spammed.

### Stop the "raise your hand" event

    {cmd_prefix}e

Renames all people who "raised their hand" back to their default nicknames, deletes it's "Raise your hand!" message and the request message.

### Invite the bot to your voice channel if you want sounds

    {cmd_prefix}join

### Tell the bot to leave the voice channel

    {cmd_prefix}leave

### Roll call
```$appel <role_name>``` will list everyone from the ```<role_name>``` that is not in the command author's voice channel.
```$appel``` will take the value of ```called_role_name``` value in instance.conf 


## Setup
### Optional dependencies
    sudo apt install ffmpeg
*ffmpeg is used for audio playback, if you don't need it, don't install it*

### Install it
    git clone https://github.com/storca/vhbot.git
    cd vhbot
    pip3 install -r requirements.txt
    cp default.conf instance.conf

## Configuration
Change the settings of the bot in instance.conf *(all settings are detailled in the file)*

**NOTE** : The members intent **must** be enabled with your bot, otherwise the roll call will not work, check [this link](https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents) for further reading.

Then run the bot

    python3 vhbot.py

This bot is meant to be used on only one server, the feature which will not work in multiple servers is the "raise your hand" one. Other features should work fine.
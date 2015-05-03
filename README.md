# twitch-tweaks
Twitch Tweaks, or TwTw for short, is a HexChat plugin for making Twitch IRC a lot more intelligent. Shows the status and game for Twitch channels as the topic, and set the tab name to the properly-capitalized channel's name with a little bullet indicating if that channel is live or not ([here's a screenshot](http://gyazo.com/0f11c934d995a0d49e626481712fb0e1)).

This is an expanded version of a script called twitch-title.py by PDog, which you can find in [Poorchop/hexchat-scripts](https://github.com/Poorchop/hexchat-scripts/blob/master/twitch-title.py).

## Installation

Installation is no different than any other HexChat plugin. You need to have the Python interface installed on your HexChat for it to work (if you don't have it, you can just re-run the HexChat installer to get it -- it won't override your existing settings). I've only tested on Python 3 but maybe it'll work with Python 2, who knows.

Anyway, assuming you have the Python interface plugin for HexChat, you can just drop twitch-tweaks.py into the addons folder inside your HexChat config folder. Don't know where your HexChat config folder is? [No worries bro, I got you covered.](https://hexchat.readthedocs.org/en/latest/settings.html#config-files)

## Usage

You can probably use this script without having to do any tweaking whatsoever, but if you want, there are some commands and configuration options available.

### Commands


* TWTWSET <name> <value...> - Sets/gets the value of a twitch-tweaks configuration option
* TWTWREFRESH - Forces twitch-tweaks to refresh the statuses of all Twitch channels
* TWTWLIST - Lists all preferences set for twitch-tweaks


### Configuration/Preferences

Here are all the settings that can be modified with the TWTWSET command, their default values, and brief descriptions of their purpose

* twitch\_api\_root = https://api.twitch.tv/kraken (where is Twitch's API server located? shouldn't ever need to change this)
* twitch\_base\_domain = twitch.tv (host name used to determine whether or not any given server is a Twitch server. shouldn't ever need to change this)
* bullet\_offline = □  (string displayed beside the names of channels that are currently offline)
* bullet\_online = ■  (string displayed beside the names of channels that are currently online)
* modify\_topic = 1 (should TwTw change the topic of Twitch channels? 0 or 1)
* modify\_tab = 1 (should TwTw change the tab name of Twitch channels? 0 or 1)
* lookup\_offline\_names = 0 (should TwTw look up the proper capitalization of channels which are offline? takes longer, especially if you're joined to a lot of channels. 0 or 1)
* refresh\_rate = 600 (how often, in seconds, should TwTw refresh the Twitch data?)

## License

License is MIT license, see the comment at the top of the script

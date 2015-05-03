# twitch-tweaks
A HexChat plugin for making Twitch IRC a lot more intelligent. Shows the status and game for Twitch channels as the topic, and set the tab name to the properly-capitalized channel's name with a little bullet indicating if that channel is live or not ([here's a screenshot](http://gyazo.com/0f11c934d995a0d49e626481712fb0e1)). This is an expanded version of a script called twitch-title.py by PDog, which you can find in [Poorchop/hexchat-scripts](https://github.com/Poorchop/hexchat-scripts/blob/master/twitch-title.py).

## Installation

Installation is no different than any other HexChat plugin. You need to have the Python interface installed on your HexChat for it to work (if you don't have it, you can just re-run the HexChat installer to get it -- it won't override your existing settings). I've only tested on Python 3 but maybe it'll work with Python 2, who knows.

Anyway, assuming you have the Python interface plugin for HexChat, you can just drop twitch-tweaks.py into the addons folder inside your HexChat config folder. Don't know where your HexChat config folder is? [No worries bro, I got you covered.](https://hexchat.readthedocs.org/en/latest/settings.html#config-files)

## License

License is MIT license, see the comment at the top of the script

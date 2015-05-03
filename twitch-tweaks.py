#!/usr/bin/env python3

"""
The MIT License (MIT)

Copyright (c) 2013

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import requests
import sys
import threading
import hexchat

__module_name__ = "Twitch Tweaks"
__module_author__ = "oxguy3"
__module_version__ = "0.1"
__module_description__ = "Do Twitch better. Forked from PDog's twitch-title.py"
# TODO: Clean up thread handling <PDog>
# TODO: Figure out why get_current_status() sometimes doesn't print updated status <PDog>

t = None
pluginprefix = "twtw_"


class StreamParser:

    def __init__(self, channel):
        self.channel = channel
        self.twitch_chans = []
        self.status = 0
        self.display_name = channel # fallback if Twitch API is down
        self.game = ""
        self.title = ""
        # self.context = hexchat.find_context(hexchat.get_info("server"), "#{0}".format(channel))

    def set_topic(self):
        """
        Set the channel topic (no formatting) and print the topic locally with formatting
        """

        #statusLong = "\00320\002OFF\002\00399"
        statusShort = get_pref("bullet_offline")
        if self.status == 1:
            #statusLong = "\00319\002ON\002\00399"
            statusShort = get_pref("bullet_online")


        if get_pref("modify_topic") == 1:
            msg = "{1}\00318{0}\00399 | {3} | \00318{2}\00399"\
                .format(self.display_name, statusShort, self.game, self.title)

            # HexChat doesn't support hiding characters in the topic bar (Windows), so strip the formatting until it's fixed
            if sys.platform == "win32":
                msg = hexchat.strip(msg, -1, 3)

            if hexchat.get_info("topic") != msg:
                hexchat.command("RECV :Topic!Topic@twitch.tv TOPIC #{0} :{1}".format(self.channel, msg))


        if get_pref("modify_tab") == 1:
            # Set the tab title to the properly capitalized form of the name
            settabCommand = "SETTAB {0}{1}"\
                .format(statusShort, self.display_name)
            hashChannel = "#{0}".format(self.channel)

            cxt = hexchat.find_context(hexchat.get_info("server"), hashChannel)
            if not cxt == None:
                cxt.command(settabCommand)


    def get_twitch_channels(self):
        """
        Get a list of open TwitchTV channels and store them in self.twitch_chans
        """
        self.twitch_chans = []
        for chan in hexchat.get_list("channels"):
            if chan.type == 2 and get_pref("twitch_base_domain") in chan.context.get_info("host"):
                self.twitch_chans.append(chan.channel)

    def update_status(self):
        """
        Check the status of open channels
        """
        if self.twitch_chans:
            for chan in self.twitch_chans:
                self.channel = chan[1:]
                self.get_stream_info()
                self.set_topic()
        else:
            pass

    def get_stream_info(self):
        """
        Get the stream information
        """
        streamUrl = get_pref("twitch_api_root") + "/streams?";
        params = {"channel": self.channel}
        streamReq = requests.get(streamUrl, params=params)
        streamData = streamReq.json()
        
        self.display_name = self.channel
        self.game = ""
        self.title = "\035Stream is offline\017"

        # use the channel object we got if we got one, else query for a channel object
        channelData = None
        if not streamData["streams"]:
            self.status = 0
            if get_pref("lookup_offline_names") == 1:
                chanUrl = get_pref("twitch_api_root") + "/channels/" + self.channel;
                chanReq = requests.get(chanUrl)
                channelData = chanReq.json()
        else:
            self.status = 1
            channelData = streamData["streams"][0]["channel"]

        self.display_name = channelData["display_name"]
        self.game = channelData["game"]
        self.title = channelData["status"]


def is_twitch():
    server = hexchat.get_info("host")
    if server and get_pref("twitch_base_domain") in server:
        return True
    else:
        return False


def get_current_status():
    """
    Update the stream status
    """
    parser = StreamParser(channel=None)
    parser.get_twitch_channels()
    parser.update_status()

def run_update_loop():
    """
    Update the stream status every 10 minutes
    """
    global t
    get_current_status()
    t = threading.Timer(get_pref("refresh_rate"), run_update_loop)
    t.daemon = True
    t.start()


def join_cb(word, word_eol, userdata):
    """
    Set the topic immediately after joining a channel
    """
    if is_twitch():

        channel = word[1][1:]
        parser = StreamParser(channel=channel)
        parser.get_stream_info()
        parser.set_topic()

    return hexchat.EAT_NONE


def unload_cb(userdata):
    """
    These appear to be necessary to prevent HexChat from crashing
    on quit while a thread is active in Python
    """
    global t
    t.cancel()
    t.join()


"""
Methods for handling plugin preferences
"""


def init_pref():
    if get_pref("twitch_api_root") == None:
        set_pref("twitch_api_root", "https://api.twitch.tv/kraken")

    if get_pref("twitch_base_domain") == None:
        set_pref("twitch_base_domain", "twitch.tv")

    if get_pref("bullet_offline") == None:
        set_pref("bullet_offline", "\u25A1 ")

    if get_pref("bullet_online") == None:
        set_pref("bullet_online", "\u25A0 ")

    if get_pref("modify_topic") == None:
        set_pref("modify_topic", 1)

    if get_pref("modify_tab") == None:
        set_pref("modify_tab", 1)

    if get_pref("lookup_offline_names") == None:
        set_pref("lookup_offline_names", 1)

    if get_pref("refresh_rate") == None:
        set_pref("refresh_rate", 600)

def get_pref(key):
    global pluginprefix
    return hexchat.get_pluginpref(pluginprefix + key)

def set_pref(key,value):
    global pluginprefix
    return hexchat.set_pluginpref(pluginprefix + key, value)


"""
Command hook callbacks
"""

twtwset_help_text = "Usage: TWTWSET <name> <value...> - Sets/gets the value of a twitch-tweaks configuration variable"
twtwrefresh_help_text = "Usage: TWTWREFRESH - Forces twitch-tweaks to refresh the statuses of all Twitch channels"
twtwlist_help_text = "Usage: TWTWLIST - Lists all preferences set for twitch-tweaks"

def twtwset_cb(word, word_eol, userdata):
    global twtwset_help_text, pluginprefix
    if len(word) < 2:
        print("Incorrect syntax. "+twtwset_help_text)
    else:
        key = word[1]
        if (get_pref(key) == None):
            print("Unknown variable name. Use TWTWLIST to see existing variables")
        else:
            if len(word) > 2:
                set_pref(key, word_eol[2])
            print("{0} = {1}".format(key, get_pref(key)))
    
    return hexchat.EAT_ALL


def twtwrefresh_cb(word, word_eol, userdata):
    global twtwset_help_text
    get_current_status()
    print("Refreshed all Twitch channels!")
    return hexchat.EAT_ALL


def twtwlist_cb(word, word_eol, userdata):
    global twtwset_help_text, pluginprefix
    for key in hexchat.list_pluginpref():
        if key.startswith(pluginprefix):
            cleanKey = key[len(pluginprefix):]
            print("{0} = {1}".format(cleanKey, get_pref(cleanKey)))

    return hexchat.EAT_ALL


init_pref()
run_update_loop()
hexchat.hook_print("You Join", join_cb, hexchat.PRI_LOWEST)
hexchat.hook_command("TWTWSET", twtwset_cb, help=twtwset_help_text)
hexchat.hook_command("TWTWREFRESH", twtwrefresh_cb, help=twtwrefresh_help_text)
hexchat.hook_command("TWTWLIST", twtwlist_cb, help=twtwlist_help_text)
hexchat.hook_unload(unload_cb)

hexchat.prnt(__module_name__ + " version " + __module_version__ + " loaded")

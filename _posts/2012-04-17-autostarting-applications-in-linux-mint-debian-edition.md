---
layout: post
title: Autostarting applications in Linux Mint Debian Edition
description: None
date: 2012-04-17 12:17:02 -0000
last_modified_at: 2012-04-17 12:17:02 -0000
publish: true
pin: false
categories:
- Linux
- Solution
tags:
- application
- autostart
- Cinnamon
- Gnome
- Linux Mint Debian Edition
- startup
- startup applications
---
A few days ago I finally made the step to switch from Linux Mint main edition (Linux Mint 10 was getting old) to the all new [Linux Mint Debian Edition Release Candidate](http://blog.linuxmint.com/?p=1967 "Blog Post about the LMDE release") with the new Cinnamon desktop. It's been great so far. However I was really missing a feature of the main edition. There you could simply right click on a menu entry and say "Launch on startup", which has been the most convenient way to add an autostart that I've ever seen. Browsing the settings and the web I at first didn't find a way to autostart applications. I found lots of descriptions involving files and directories that don't seem to exist in my Linux Mint Debian Edition. Well enough babbling.

## Solution

Simply run: [sourcecode language="bash"] gnome-session-properties [/sourcecode] You can do this in the terminal or with Alt + F2 (gnome do). There you have a list of all your startup applications and you may add applications by specifying their command (like: "thunderbird" or "firefox") but you may also remove startup applications. This looks something like this: [![](https://pragtob.wordpress.com/wp-content/uploads/2012/04/startup_apps.png?w=300)](https://pragtob.wordpress.com/wp-content/uploads/2012/04/startup_apps.png) This should work with all Gnome based desktops (Gnome 2, Gnome 3, Mate, Cinnamon), I haven't tested it though. It's fairly easy but embarrassingly took me long enough to figure out, so I figured that it's better to blog about it and maybe save somebody else some time.

---
layout: post
title: Getting the "fortune cookies" back in the Linux Mint Debian Edition terminal
description: None
date: 2012-05-13 16:43:35 -0000
last_modified_at: 2012-05-13 16:43:35 -0000
publish: true
pin: false
categories:
- Linux
- Solution
tags:
- fortune cookie
- funny
- greeting message
- Linux Mint
- Linux Mint Debian Edition
- terminal
---
Some weeks ago I installed Linux Mint Debian edition after being a loyal and happy user of the Linux Mint main edition for some years. It was a very nice experience but something was missing... in the main edition, every time you open a terminal you are greeted by an animal, which has something more or less funny to say. I always liked that, it's part of Linux Mint for me. However when I opened the terminal in my freshly installed Linux Mint Debian Edition I saw the following: [![empty_terminal](/assets/uploads/2012/05/empty_terminal.png?w=300)](/assets/uploads/2012/05/empty_terminal.png) No one greeted me. So I decided to [ask on the forums](http://forums.linuxmint.com/viewtopic.php?f=199&t=99860 "Linux Mint forums"). Gladly there is a solution for this (thanks to äxl for the answer!). You can simply run: 
```bash
 gconftool -s -t bol /desktop/linuxmint/terminal/show_fortunes true 
```
 Alternatively you can open the graphical configuration tool with "gconf-editor", navigate to that path and change the value by hand. And then there they are again, my beloved "funny greeting messages", "fortune cookies" or whatever you want to call them. And notice what really important wisdom my terminal has to share with me this time: [![funny terminal](/assets/uploads/2012/05/funny_terminal.png?w=300)](/assets/uploads/2012/05/funny_terminal.png)

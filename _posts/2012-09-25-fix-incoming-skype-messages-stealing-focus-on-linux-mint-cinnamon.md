---
layout: post
title: 'Fix: Incoming Skype messages stealing focus on Linux Mint (Cinnamon) '
description: None
date: 2012-09-25 18:35:25 -0000
last_modified_at: 2012-10-22 18:48:15 -0000
publish: true
pin: false
categories:
- Solution
tags:
- attention
- Cinnamon
- foreground
- grab focus
- incoming message
- Linux Mint
- Skype
- window
---
After upgrading my PCs to Linux Mint Debian Edition, and thereby using the Cinnamon user interfacen, I encountered a particularly bothersome behaviour: For every incoming Skype message the skype window would come to the front and grab focus. So while typing you would even continue to type in the Skype Window. Luckily I found a fix in the [Skype Linux support forums](http://community.skype.com/t5/Linux/chat-window-pops-up-on-every-received-message/td-p/728576/page/2). This behaviour is already [fixed in the Cinnamon Repository](https://github.com/linuxmint/Cinnamon/commit/c5bbcad1cc4cc8183f2556deef867d0fae5f0109), But you can fix it yourself and don't have to wait for an update. For instance the problem doesn't seem to be fixed in the Update Pack 5 to Linux Mint Debian Edition.

### Solution

At first locate the file called windowAttentionHandler.js - this can easily be done on the command line: [sourcecode language="bash"] locate windowAttentionHandler.js [/sourcecode] For me the path is /usr/share/cinnamon/js/ui/windowAttentionHandler.js - now you just need to open this file as a super user and make the same change as in[the commit](https://github.com/linuxmint/Cinnamon/commit/c5bbcad1cc4cc8183f2556deef867d0fae5f0109). More easily speaking, at first open the file in a simple editor (pluma, gedit, nano, vi...) as the super user: [sourcecode language="bash"] sudo gedit /usr/share/cinnamon/js/ui/windowAttentionHandler.js [/sourcecode] now find this line: [sourcecode language="js"] if (!window || window.has_focus() || window.is_skip_taskbar()) [/sourcecode] And replace it with this line (or just adjust the latter part so it lookes like the line below): [sourcecode language="js"] if (!window || window.has_focus() || window.is_skip_taskbar() || window.get_wm_class() == "Skype") [/sourcecode] For some weird reason the line wrapping of the code block doesn't work. So hover that code box with your mouse and select view source code, you can then copy and paste from there! Please be careful not to mess with the file, that could **break your system** (or at least the handling of the attention of windows). So make sure to make a backup of that file. After this a restart is probably required for the changes to take effect, at least it was for me. As commenter Clement said you can also just hit Alt + F2 and type "r" and hit ENTERin order to restart cinnamon (Thanks for the comment!). So now, happy using Skype ;-) (By the way: there is a [new Skype version for Linux](http://blogs.skype.com/linux/2012/06/skype_40_for_linux.html) \- which doesn't seem to be in the repositories yet. Check it out!)

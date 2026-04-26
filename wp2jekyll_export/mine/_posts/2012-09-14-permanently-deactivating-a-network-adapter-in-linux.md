---
layout: post
permalink: https://pragtob.wordpress.com/2012/09/14/permanently-deactivating-a-network-adapter-in-linux/
title: Permanently deactivating a network adapter in Linux
description: None
date: 2012-09-14 09:57:06 -0000
last_modified_at: 2012-09-14 09:57:06 -0000
publish: true
pin: false
categories:
- Linux
- Solution
tags:
- blacklist
- boot
- deactivate
- driver
- kernel module
- wifi
- wireless card
---
So my PC has 2 wireless adapters. One crappy internal one and a good external one which I bought because the internal one is so bad. But on system start I now had the problem that the crappy wifi card always wanted to connect which I didn't want it to do. So I had to go through the trouble of running the following command in my shell: [sourcecode language="bash"] sudo ifconfig wlan0 down [/sourcecode] mostly a few times, since it didn't seem to pick it up from the beginning. I tried to run this command at system startup using rc.local [as described here](http://www.upubuntu.com/2012/01/how-to-disable-your-network-adapter.html), but that didn't work for some reason. But there is a different solution, that worked for me!

### Solution

Blacklist the kernel module that is responsible for running the wifi adapter. In other words, don't load the Linux driver for the bad wifi adapter so it won't work. You can do this the following way: At first you need to find out which kernel module is responsible for the wireless card you want to deactivate. The following command shows you all currently loaded kernel modules: [sourcecode language="bash"] sudo lsmod [/sourcecode] I grepped this list for part of the name of the chipset of my wireless card, which is "RTL8185" so I went with: [sourcecode language="bash"] sudo lsmod | grep rtl81 [/sourcecode] There the "rtl8180" kernel module showed up as being loaded, with no other modules using it. Now we can try to remove this module from the currently loaded modules with [sourcecode language="bash"] sudo modprobe -r rtl8180 [/sourcecode] If everything worked, the unwanted wifi card should just have disappeared from your network control panel. It also shouldn't show up any more when running the "ifconfig" command. If not, you probably removed the wrong module in that case you should rather add that Linux kernel module back in: [sourcecode language="bash"] sudo modprobe -a removed_module_name [/sourcecode] However if it worked and the wireless adapter really disappeared, then we don't want to remove it every time we boot our system. That should be done automatically! And there indeed is a mechanism for that. There is a blacklist of modules that shouldn't be loaded on system boot. In order to use this you have to modify /etc/modprobe.d/blacklist (or create it, as I had to) with a text editor and admin rights. So I did: [sourcecode language="bash"] sudo nano /etc/modprobe.d/blacklist [/sourcecode] And modified the file to look like this: [sourcecode] blacklist rtl8180 [/sourcecode] Of course you have to modify my module name with yours. This will blacklist the module/driver automatically on system boot/startup. This worked beautifully for me on my Linux Mint Debian Testing operating system. I hope it works for you as well. Of course this technique is more general and can be used to blacklist any kernel module/driver.

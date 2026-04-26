---
layout: post
title: 'Solution: Converting a series of pictures to a PDF'
description: None
date: 2013-08-15 16:04:58 -0000
last_modified_at: 2013-08-15 16:04:58 -0000
publish: true
pin: false
categories:
- Linux
- Solution
tags:
- conversion
- imagemagick
- images
- pdf
- screenshots
- slides
---
So with my last presentation given in a not really mature presentation tool I still wanted to provide PDF slides for people to look at. So I took screenshots of every single slide and then wanted to put those into a PDF. But how to do it? I started out with Libreoffice and inserting images there maximizing them - but that's way too boring, repetitive and time consuming. So a quick google search came up with [this](http://stackoverflow.com/questions/8955425/how-can-i-convert-a-series-of-images-to-a-pdf-from-the-command-line-on-linux) instead which worked instantly. You got to have [imagemagick](http://www.imagemagick.org) installed (on Linux at least it should already be installed as many packages depend on it, otherwise do sudo apt-get install imagemagick). With imagemagick you can just do the following on the console: [code lang="bash"] convert image_pattern*.png my_presentation.pdf [/code] Or for me personally it was: [code lang="bash"] convert Screenshot\ from\ 2013-08-14\ 10\:4*.png shoes.pdf [/code] Et voila a beautiful PDF with all my slides. Hope this helps you! Tobi

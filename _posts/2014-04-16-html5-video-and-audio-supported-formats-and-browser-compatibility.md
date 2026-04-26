---
layout: post
title: HTML5 &lt;video&gt;  and &lt;audio&gt; - supported formats and browser compatibility
description: None
date: 2014-04-16 11:24:29 -0000
last_modified_at: 2014-05-26 17:31:18 -0000
publish: true
pin: false
categories:
- Software Engineering
- Solution
tags:
- audio
- browser compatibility
- browser support
- codec
- format
- HTML5
- media
- support
- video
---
With HTML5 [video and audio tags are here](https://developer.mozilla.org/de/docs/HTML/Using_HTML5_audio_and_video) and ready for use to easily enhance your websites with audio and video. The tags are available in all major browsers now, except for Opera Mini ([audio](http://caniuse.com/audio) [video](http://caniuse.com/video)). You even got [popcorn.js](http://popcornjs.org/) to interact with the media, make you web pages react to the progress of a video and build cool new media enriched websites. The major problem with HTML5 media though so far has been browser support for the different media formats/codecs. Support has gotten a lot better - not great, but better. At the time of this writing it seems like you only have to offer 2 different formats for audio and video to support a wide range of browsers. Disclaimer: I didn't try this all out manually. I trust the data for Browser compatibility I found on the Internet: [Mozilla Developer Network media format support](https://developer.mozilla.org/de/docs/HTML/Supported_media_formats#Browser_compatibility), Wikipedia([HTML5 audio](http://en.wikipedia.org/wiki/HTML5_Audio), [HTML5 video](http://en.wikipedia.org/wiki/HTML5_video#Browser_support))

### Audio

Support **mp3** and **Ogg Vorbis** \- you can use other formats in place of ogg as well (and AAC in place of mp3).

### **Video**

Support **H.264 (.mp4)** \+ **Theora (.ogv)** or **VP8****(WebM)** should do the trick. On a last not, if you want to convert video files you can use ffmpeg, e.g. for instance theora/.ogv to H.264/WebM: 

```bash
 ffmpeg -i demo.ogv -f mp4 demo.mp4 
```

 Hope that this helped :-)    

---
layout: post
permalink: https://pragtob.wordpress.com/2011/09/09/oauth-out-of-bandpin-authentication-with-ruby/
title: OAuth out of band/PIN authentication with Ruby
description: None
date: 2011-09-09 14:51:37 -0000
last_modified_at: 2011-09-09 14:51:37 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- desktop application
- OAuth
- out of band
- PIN
- ruby
- twitter
---
[OAuth](http://oauth.net/ "OAuth") is a protocol used to authenticate an application in order to use the API of a service. Here we'll use [Twitter](https://twitter.com/ "Twitter") as an example. The [developer documentation](https://dev.twitter.com/docs "developer documentation") of Twitter is a really good resource, when you look for general information or even specific libraries. It is quite common to authenticate with such services using a callback URL, so this case is pretty easy and well covered. Take for instance the [ruby oauth gem](http://github.com/oauth/oauth-ruby "Ruby oauth gem"), authentication using callback URL is described pretty well in their documentation. But this just works for web applications. If you want to do OAuth with a desktop application or a mobile application you mostly can't handle callback URLs. So if you are unsure about which authentication to choose, Twitter has an excellent help page called ["Which authentication path should I choose?"](https://dev.twitter.com/docs/auth "Which authentication path should I use?"). So I realised I needed to do authentication using OAuth out of band/PIN. I found very few resources on how to exactly do that, so here is my solution.

# Solution

Of course first you need the oauth gem. [sourcecode language="bash"] gem install oauth [/sourcecode] Now you have got to [register your application at Twitter](https://dev.twitter.com/apps "register application at Twitter"). You may then get your consumer key and your consumer secret from the page of your application. Then you can go ahead and I'll just show you a little script for doing that kind of authentication: [sourcecode language="ruby"] # this makes oauth pretty easy require 'oauth' # used to launch the web browser with the authorization page # gem install launchy require 'launchy' consumer = OAuth::Consumer.new(YOUR_CONSUMER_KEY, YOUR_CONSUMER_SECRET, :site => "https://api.twitter.com" ) request_token = consumer.get_request_token # open browser for authorization Launchy.open request_token.authorize_url puts "Please authorize the app to have access to your Twitter account. A pincode will be displayed to you, please enter it here:" pincode = gets.chomp # last step of the authentication access_token = request_token.get_access_token :pin => pincode access_token.token # user token access_token.secret # user oauth secret [/sourcecode] Be aware of the fact, that you need to (securely) save the token and secret somewhere. But now that you got those you may use the **[twitter gem](https://github.com/jnunemaker/twitter "Twitter gem")** , to do whatever your app aims to do with Twitter! So have fun with out of band OAuth authentication! _Sidenote: Where to save your consumer secret is a quite hard problem, you might want to check out[this stackoverflow discussion](http://stackoverflow.com/questions/1934187/oauth-secrets-in-mobile-apps "How to secure consumer secret"). If you got better ideas please leave a comment ;-)_ Question or feedback? Please leave a comment!

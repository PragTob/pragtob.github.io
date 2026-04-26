---
layout: post
title: Never ever modify objects used as hash keys
description: None
date: 2011-12-22 17:26:41 -0000
last_modified_at: 2011-12-22 17:26:41 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- hash
- key
- object
- weird behaviour
---
Before we get to the real topic and the source of some quite big headaches for me, I want to explain something first.

### How can I use my own objects as keys in a hash (dictionary)?

You simply have to define the eql? and hash methods of those objects in some meaningful way so that they reflect the equality you want to achieve in the hash (dictionary). Please don't be confused by the double use of the word hash. The method computes a number that should be unique to the object. Or put it in another way, if two objects return the same they are considered to be the same. Think MD5 or SHA1. The hash as a construct is more like a dictionary, mapping from a key to a value.

### Problem

Now to the real problem. I had a finite number of external representations for something. In this example let's take the coordinates of cities (the real example was different, but I don't want to spoil the test taken at ThoughWorks). The coordinates are the internal representation whereas symbols like :city_a are the external representation. In the beginning I had to start with the external representation, convert it into an internal representation for computation and in the end I had to output the external representation once again. So I thought that it would be nice to have a one-to-one mapping instead of case statements and possibly duplicated code. So my idea was to go with a hash and thanks to the hash#invert method I could get both the internal and the external representation. So I went ahead and wrote that hash (this was the actual cause for my former blog post) and the corresponding methods: (sorry for the lack of indention, wordpress makes that awfull hard on me) [sourcecode lang="ruby"] class City def initialize x, y @x = x @y = y end CITIES_COORDINATES = { city_a: City.new(10, 5), city_b: City.new(15, 25), city_c: City.new(30, 3), city_d: City.new(40, 12) } def self.for symbol CITIES_COORDINATES[symbol] end def to_sym CITIES_COORDINATES.invert[self] end # stuff omitted end</pre> [/sourcecode] Everything good so far. So where is the problem? The problem was that 2 of my tests started going nuts for real. When I instantiated a new object and said that it was facing North it claimed to be facing East. I thought that maybe my before :each wasn't working properly (as the tests involved changing the direction) but I checked and the two objects indeed had different object_ids. So they weren't the same object but the tests seemed to influence each other - somehow. I could comment out all of the tests but the 2 failing ones and they would magically pass. Also running each of them separately would let them pass.

### Solution

The problem essentially was that in a City object, there was a method changing the object (e.g. not immutable). However this doesn't seem to play too well with using those objects as hash keys. I changed the method to instead return a new object representing the new city. After that everything worked as expected.

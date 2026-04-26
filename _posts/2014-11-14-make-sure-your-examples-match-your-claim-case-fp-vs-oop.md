---
layout: post
title: 'Make sure your examples match your claim (case: FP vs. OOP)'
description: None
date: 2014-11-14 20:32:27 -0000
last_modified_at: 2014-11-14 20:32:27 -0000
publish: true
pin: false
categories:
- Software Engineering
tags:
- clojure
- comparison
- functional
- java
- object-oriented
- Programming
- ruby
---
I started reading [Functional Programming Patterns in Scala and Clojure](https://pragprog.com/book/mbfpp/functional-programming-patterns-in-scala-and-clojure) \- a nice book so far. However, right at the beginning in Chapter 1.1 _"What is Functional Programming?"_ the author compares an object-oriented implementation with a functional implementation. Here is the code, first object-oriented (Java): [sourcecode language="java"] public List filterOdds(List list) { List filteredList = new ArrayList(); for (Integer current : list) { if (isOdd(current)) { filteredList.add(current); } } return filteredList; } private boolean isOdd(Integer integer) { return 0 != integer % 2; } [/sourcecode] Now functional version (Clojure): [sourcecode language="clojure"] (filter odd? list-of-ints) [/sourcecode] After this comparison the author states: _"The functional version is obviously much shorter than the object-oriented version."_. Well let's all just go and do functional programming then! Not so fast. The object-oriented example has a lot of clutter that has **nothing to do with Object-oriented Programming** , they are just due to Java or in part due to a somewhat unfair comparison. Let's walk through the code and remove the clutter to make a better comparison.

## Types

The sample features a lot of type information - that has nothing to do with OOP vs. FP, there are also functional languages that have types, although a lot of them handle them better than Java. Let's Remove them: [sourcecode language="java"] public filterOdds(list) { filteredList = []; for (current : list) { if (isOdd(current)) { filteredList.add(current); } } return filteredList; } private isOdd(integer) { return 0 != integer % 2; } [/sourcecode]

## isOdd method

The Java sample defines a private _isOdd_ method to check if a number is odd. This has nothing to do with OOP, it's just a detail that Java does not implement an _isOdd_ method themselves. There might also be functional languages out there, that doesn't have it built in like Clojure. So let's remove that as well: [sourcecode language="java"] public filterOdds(list) { filteredList = []; for (current : list) { if (isOdd(current)) { filteredList.add(current); } } return filteredList; } [/sourcecode]  

## Method definition

The Clojure version does not define a method while the Java version defines a method. So let's remove that method definition from the Java code. I also omit the return statement, because the result is now saved in the _filteredList,_ which can be used for further computation. [sourcecode language="java"] filteredList = []; for (current : list) { if (isOdd(current)) { filteredList.add(current); } } [/sourcecode]

## Be careful with your comparisons

Compare the final code sample with what we started out with. It's half the lines of code and much more concise. I stripped off parts of the code that I believe have nothing to do with the argument at hand, but are rather details of Java. I still like the _Clojure_ sample better and I'd also prefer coding Clojure over Java any day of the week. That's not the point. The point is that one should be diligent to make examples for comparisons stick to the topic at hand. And in the book the topic was FP vs. OOP - not Java vs. Clojure. On a final note, a lot of cool mainly object-oriented languages have features akin to these of functional programming. Often in the shape of blocks. Let's take a look at **Smalltalk** , the language that is often credited with introducing Object-oriented Programming. Let's implement our little code sample there (I used [GNU Smalltalk](http://smalltalk.gnu.org/), which implements Smalltalk-80, the "original"): [sourcecode] ints select: [:i | i odd] [/sourcecode] That's short and sweet! Now, just for kicks, let's do ruby, which is mainly object-oriented, but well luckily has these functional features: [sourcecode language="ruby"] ints.select &:odd? [/sourcecode] Just saying, be careful with your examples. These two (mainly) object-oriented languages do just as well as Clojure here. Last but not least, let it be duly noted, that yes the Clojure result is lazy and immutable, but then again that's not the point here, although both are col features ;)

---
layout: post
title: 'Interviewing Tips: The Interview'
description: None
date: 2024-03-21 14:27:20 -0000
last_modified_at: 2024-04-02 13:31:24 -0000
publish: true
pin: false
categories:
- Job Search
- Resources
tags:
- applications
- interview
- interview questions
- interviewing
- interviews
- job hunting
- Senior Engineer
- tips &amp; tricks
---
Welcome to the last part of the interview series! In this part we’ll take a look at more general interviews – usually they cover a variety of topics. They also heavily depend on the company. For this purpose the following sections will be split into a bunch of broader topics of discussions (Employment History, Technical Experience etc.). Depending on the interview type you may talk about all of these, some of these or only one of these in specialized interviews. The main focus here are interviews of Senior+ engineers – that said, the concepts are the same but of course the requirements differ for more junior engineers as well as people managers (although we’ll touch on the latter).

Each section will introduce the general topic with some tips and why questions in this bucket may be asked. Each section will feature **a list of example questions** that _may be asked in an interview_. It’s important to note that these aren’t necessarily questions I recommend asking as an interviewer. I purposefully include questions I wouldn’t ask, because **the goal of this post is to prepare people for interviews** they might really encounter in the wild. And the reality is, not all interviews are great.

Why should you read on and think about these? Sadly, interviews are very stressful situations for the candidate. A great interviewer will try their best to make you feel as comfortable as possible, but they can never alleviate all the pressure. Moreover, some don’t care. Regardless of the circumstances **it can be tough to answer questions “on the spot”**. This is especially tough for some questions that require reflection and recalling specific situations – such as “Tell me about a mistake you made and how you fixed it.”. We all make mistakes. That’s clear. However, **failing to come up with an answer on the spot can look extremely bad**. Hence, I encourage you to think about the answers to some of these common questions **in advance** to be prepared and be able to answer and discuss them. I hope to **help you succeed in an interview because you took the chance to reflect about some of these questions beforehand**.

To set yourself up for success, ask before the interview what topics will be covered in the interview to be able to prepare yourself.

Now, what qualifies me to dish out tips & tricks on interviewing? Most recently I did 100+ interviews at Remote for Junior Devs all the way up to Staff Engineers and Engineering Managers. I also used to own the entire engineering hiring process at a smaller startup. Of course I’ve also done my fair share of interviewing as a candidate. With all that & more, I think I have some helpful tips to share. Also thanks to my friend [Roman Kushnir](https://www.linkedin.com/in/rkushnir/) for reviewing this and adding some key aspects.

Speaking of which, this the final part of an interviewing tips series, you can find the other posts here:

* [CV, cover letter & screening interview](https://pragtob.wordpress.com/2023/11/07/interviewing-tips-before-you-apply-cv-cover-letter-screening-interview/)
* [Technical challenges - Coding & More](https://pragtob.wordpress.com/2023/11/29/interviewing-tips-technical-challenges-coding-more/) (Bonus: [Reexamining FizzBuzz Step by Step – and allowing for more varied rules](https://pragtob.wordpress.com/2023/11/28/reexamining-fizzbuzz-step-by-step-and-allowing-for-more-varied-rules/))
* Interviews ←**you are here**

## Mindset

**A good interview can feel like a good conversation** – it flows naturally, and you talk about topics you’re interested in with nice people. That said, **not all interviews are great**. Some are outright terrible and fail you for no good reason at all. This is frustrating beyond belief. I highlight this so that you know: **Failing an interview doesn’t have to be your fault**. There’s a variety of reasons that can contribute to this, most prominent of all: [biases](https://en.wikipedia.org/wiki/List_of_cognitive_biases). This can mean anything from the interviewer having preconceived notions of what makes a good employee which you’re not fitting or assumptions they make about you based on irrelevant factors. Sometimes interviewers are also just trained badly and forced to do interviews. Interviewing is by no means an objective, definitive process that always ends with the “correct” result.

At the end of the day always remember that **interviewing is a two-sided process: You’re applying at the company but it’s also your choice whether you join the company or not**. Naturally, this is a privileged perspective and if money is tight or the market is dry you won’t have as much choice. If you have the luxury to decide, the way the interview process works can be indicative of how a company works. Take note of the questions they ask – would you want to work with people selected by this process? I have aborted interview processes in the past because my answer to that question was “no”. I have in turn also felt right at home during an interview process, as I saw how I was valued and how they asked great questions. This made it much easier to accept their offer when it came to that. That said, sometimes the recruitment experience has almost nothing in common with the experience of working at a company – so take it with a grain of a salt as well.

Broadly speaking I think there are 2 approaches to interviewing: **Seeing the potential and the positives in a candidate or looking for faults in the candidate**. One of my favorite hires ever was [Ali](https://www.linkedin.com/in/alichurcher/) who had been rejected by 2 other companies before interviewing with us. This was mostly due to a lack of experience in current JS frameworks as her last job had an outdated tech stack. However, what we saw was a person who had extremely solid fundamentals in JavaScript, was honest, curious, wanted to learn and had an eye for improving processes and was able to reason extremely well. We hired her in a heartbeat, accounting for some ramp up time. She did so well that I wanted to promote her to team lead later.

### Keep Calm

Interviewing can be extremely challenging but don’t stress it. Do your best. **Stay calm.** **Take time to think.** No one expects you to have all the answers ready at a moment's notice. It is better to think for a bit than to blurb out the first thing that comes to mind. Ask clarifying questions when you don’t know exactly what is meant by the question. This can also give you some extra time to think about an answer. Make sure to also **manage the time** a bit: Talking without end can be bad as you might go off on a tangent they aren’t interested in. Always just giving the shortest answer also isn’t great though as the answer may lack nuance and detail. The ideal length of an answer varies wildly. I usually try to **answer in a couple of sentences** first and then **check in with the interviewers** : “Should I tell you more about this problem or would you like to know about something else?”. As I’m also bound to tell long stories I will often also say “Stop me if I’m going too far with this”.

### Before the Interview

**Don’t forget your research we talked about in the**[**first blog post**](https://pragtob.wordpress.com/2023/11/07/interviewing-tips-before-you-apply-cv-cover-letter-screening-interview/). Many companies use their company values to evaluate interviews: Make sure you’re aware of them, and highlight how you may relate to them in your answers. Knowing the domain of the company and the challenges they are facing right now might help you anticipate questions. If they have blog posts on their transition from a monolith to microservices, that topic is likely to come up!

**Remember what the interviewers may be looking for**. Generally that means taking the context into account. Especially on the higher career ladder levels there’s rarely a definitive answer – the answers are often some approximation of **“it depends”**. When someone asks you for your opinion on “Microservices vs. Monoliths”, even if you are firmly in one camp, it behooves you well to highlight that you know the limitations of both approaches. Show them that you can identify when your favorite approach might not be a good choice. Essentially, people often don’t look for someone who only knows their hammer but someone who may have some preferred tools while knowing when the other tools may be more useful – even if they aren’t experts in those tools.

**For the last couple of minutes before the interview** I’d suggest you to take some time to go over important information again to get ready and into the mindset for the interview. Checking the company values again is a great start, you can read the job description or company business model. I also open up my CV again so that I can refer to it when the interviewers ask about it. If I submitted any type of exercise before the interview, I’ll also briefly review it again.

## Types of Questions/Topics

Before we go to the different areas: Of course these areas aren’t always clearly separated. There are gray areas and questions that may belong in multiple categories. It’s also common for one area to flow into the other. For instance an interview may start with “Why are you applying here?” to which your answer may include “Elixir” which will cause the interviewer to drill down on why you’re interested in Elixir.

This separation into sub-areas isn’t only made for convenience. For a “general non specific topic” interview these areas may _broadly_ cover what interviewers want to talk to you about. Depending on the interview process, some of these might also have dedicated full interviews.

## Introduce yourself

A classic of interviews – which I underestimated for the longest time. Until my friend Pedro Homero pointed out to me, in the[first article of this series](https://pragtob.wordpress.com/2023/11/07/interviewing-tips-before-you-apply-cv-cover-letter-screening-interview/), that **it’s essentially an elevator pitch for yourself answering the question “Why should we hire you?”**. It also gives you the opportunity to guide the conversation – if you mention something that piques the interviewers’ interest, chances are they’ll ask you about it. So, use it to shine the lights on your strengths.

Recently I had an interviewing experience that was a bit too free-form. “Tell me about yourself” was essentially the only question I was answering – for an entire hour. I struggled a bit and only realized late into the interview that I forgot to mention some important facts, like my open source work or my presentations at conferences. This led to me creating a mind map of my biggest “selling points” that I then broke down into a couple of bullet points suitable for a ~2 minute introduction. These cover the breadth of my experience as well as some of the “special” things I did. You don’t need to go that far, but I’ve gotta say – it was a worthwhile experience for me.

**Example Questions**

* Tell us about yourself

## Employment History

One of the easiest ways to get to know you in a professional context is based on your employment history: **What have you done so far and how has it led you to apply at this company?** While it often focuses on your most recent jobs, it is a look at the decisions you’ve made so far in your career. What did you like? What didn’t you like? And most importantly: How has your experience so far made you a good fit for the position you’re interviewing for right now?

Naturally, the most dreaded questions here revolve around **why you left a workplace**. Be it the last one or why you only stayed at one place for a couple of months. A positive minded interviewer asks these questions to make sure that the position won’t have the elements that made you leave a job. The answer to these is delicate – no matter how unhappy you’ve been you shouldn’t completely trash your last company or boss. It’s not a good look on you. Many people opt for non-committal answers (“Time to move on'', “new challenge” etc.) and that’s probably the safest answer. That said, I’m often too honest for my own good and as such also appreciate honesty from candidates a lot. Knowing that you left because of micro management or due to too many meetings and overwork may be valuable for your interviewer and **may help you avoid sliding right into the next bad situation**. That said, it’s a fine line to walk. In one of the worst interviews I’ve ever been a part of, the candidate told us he left his last position because he “just wasn’t appreciated” and didn’t get the promotion he wanted. That can happen, but if it’s the same in the past three positions a pattern emerges and it’s not one of someone I’m likely to want to work with.

Another thing people may worry about are **breaks in their CV**. Usually these are completely fine, I have a few of them – when I can afford it I like to take a couple of months off to relax, do something fun but also spend some time on technology and then make a concentrated effort to find my next gig. I’m on one such break right now, which gives me the time to write this. Most people can empathize with this. Much like anything, it’s ok as long as you can share a good reason. For instance, you might think that only staying at a company for a month looks bad. However, if the company went bankrupt or you figured that the company had barely any direction or interesting work for you then those are fine reasons.

Overall people will want to look at **what experiences you’ve made and how those experiences may help you be an effective part of their company**. This is also your reminder that **everything on your CV is fair game to ask about**. And by that I mean that if someone says “It says on your CV you worked on X, tell me more about that” you should be able to talk about that subject for at least a couple of minutes if need be. If you can’t, consider dropping it from the CV. I’ve been in too many interviews where a candidate seemingly couldn’t recall anything about a point on their CV that intrigued me.

Keep in mind that while asking about past experiences interviewers are often interested in your **reflections on the topic**. They usually aren’t just interested in how processes worked at your last employer, but what you think about them and how they might have been improved.

**Example Questions**

* Why are we here?
* What are you looking for in joining our company?
* Why did you quit your last job?
* I see there’s a gap of 2 years in your CV here, what did you do during that time?
* At company X you lead project Y - what was that like?
* What was the development process like in your last company?
* Who was the product for? Who were the stakeholders? How did it solve their problem? Why was it better than its competition?
* How did the business model work?
* Describe the development process of your last job. What could have been improved?
* Tell me about a recent complex project you worked on
  * What was your role? What part did you work on?
  * Why was the project built?
  * What challenges did you run into?
  * Did the project accomplish its goals?
  * Who were the other team members? How did you work with them?

## Technical Experience

This section is similar to the previous one in that it’s about your past experiences – here the **focus is just more technical** as well as probing your overall knowledge. These sections will usually flow in and out of each other. You’ll talk about your general experiences at an employer and at some point someone may decide to dig deeper into one of these. The questions can also appear separate from that, usually introduced by more specific questions like “Tell me about a complex project you worked on” or “You like technology X, when would you not use it?”.

One of the major goals here is to test your **decision making** and **reasoning skills** as well as your **ability to explain**. These questions are usually broad and leave you room to steer the conversation and showcase your knowledge. As a general rule of thumb, especially here your answers should be nuanced. The more senior you get, the more the answers usually entail some variant of **_“it depends”_**.

**It’s easy to say too much or too little here.** If you immediately dig really deep into a topic there is a chance you’re going off on a tangent the interviewers aren’t interested in at all, but find it hard to stop you (esp. In a video call interview). If you just say a couple of high level things without explaining any of it, it can give the impression that you don’t really know what you’re talking about. As an interviewer I always dig deeper: “I like elixir because of functional programming” Ok, but what does functional programming mean? And how does it help you, what benefits do you get from it? Sadly, there are many candidates who fail to explain concepts beyond the buzzwords. Aim to be able to be better and explain what these buzzwords mean.

I recommend an approach where you **mention some high level points first but offer to dig deeper**. So, if someone asked “Why do you like to work in elixir?” an answer could go something like this: “I think the functional programming approach, especially immutable data structures, makes code more readable as it’s easy to see what data changed. The code becomes a story explicitly transforming data. I also like how parallelism is baked into everything leading to faster compile and test run times. That coupled with the resiliency of the BEAM VM makes for a great platform. I trust the creators of the language and the ecosystem – they often surprise me positively with the problems they decide to tackle. For instance, I really like how explicit ecto is in its database interactions and how much direct control it gives to me. Do you want me to dig deeper into any of these?”. Of course your answer can’t be that prepared – I wanted to emphasize here how important it is to highlight things that you like, but also why you like them to open up a potential discussion.

To close this off, some of the most heartbreaking but also definitive “No''s I have given as an interviewer were for senior engineers who changed the entire tech stack of their previous company – and when asked about it couldn’t give me a better reason other than that they “liked it better”. That’s a fine reason to rewrite your hobby project, not to change a company’s tech stack though no matter if I agree with your choice or not. My expectations for Senior+ engineers are much higher than that.

**Example Questions**

* Why do you like to work in technology X?
* Is Technology X always the best choice? When would another technology be better suited?
* You remodeled the entire architecture at company X - why did you do that? Would you do it again? What motivated the change? How was it planned?
* What’s a mistake you made? How did you fix it?
* Tell me about a big refactoring you did. Why was it necessary? Was it a success? How can you tell?
* What’s a technical design you’re proud of?
* What was the last down time you were involved in? What happened? What steps were taken to prevent it in the future?
* What makes code good vs bad?
* What do you look out for when reviewing a PR?
* Microservices vs. Monoliths – what’s your take?
* What’s your approach to testing?
* How do you deal with technical debt?
* How do you deal with growing/large code bases? What pains do appear? How can you mitigate those?
* How do you go about changing coding guidelines and patterns in a big application with a big team?
* Talk to me about using inheritance vs. composition.
* When should you use metaprogramming?

## Technical Knowledge

I might need to work on naming here, but what this section means is that there are parts where **interviewers “quiz” your knowledge base**. As opposed to the previous section, there are usually right & wrong answers here and much less “it depends”. They’re looking to **gauge how “deep” your knowledge is in a certain area with very specific questions**. Sadly, sometimes this one can feel like an interrogation – keep calm, and also be aware that it’s usually ok to not have all the answers. Whatever you do, **don’t try to confidently act like you know the answer but say something that’s a guess at best**. This may be my bias, but I’d much rather work with someone who admits they don’t know but then give me a guess (that may or may not be correct) rather than someone who confidently tells me something they know is probably wrong.

These questions are usually very **job and technology dependent**. You can google “Technology X interview questions” and you’ll find a lot of suitable ones. I won’t enumerate all of them here, just a couple to illustrate common questions I have seen. A poster child example may be “What are indexes in SQL? When should you use them?”. Naturally these can also show up during another part of the interview. For instance, if a candidate forgot some indexes during a coding challenge I’ll usually ask them about it.

Sadly this section comes with one of my **favorite interviewing anti-patterns: Interviewers asking people about things that they just learned**. I’ve seen and heard about this _many_ times. Basically there was just a big problem, they noticed something has always been done wrong at the company and no one had caught it. Now they interview everyone for that knowledge they just acquired. The irony to me is, that no one at the company would have passed that interview as they all were doing it wrong forever. So, unless you think everyone at your company, including yourself, should be fired please don’t do this.

**Example Questions**

* What’s a join in SQL?
* What are database indexes? Why don’t you just index all fields?
* How can you manage state in React?
* What makes your web page accessible?
* What is CORS?
* What is XSS?
* What does MVC stand for? How does it help & why is it necessary?
* If Assembly is so efficient why don’t we write all programs in it?
* What is DNS? How does it work?
* What happens when you initiate an HTTP request?
* What is multithreading?
* What is a GenServer? How do you use it? What do you need to watch out for?
* In ActiveRecord there are often 2 variants of the same function, one with ! and one without. What’s the difference? When do you use which one? Why?
* What’s an n+1 query and how do you avoid it?
* What are your favorite new features of $new-prog-lang-version ?
* Tell me about a function in the standard library of $prog-lang that you really like but maybe not everybody knows about?
* What is DDD?

## Leadership Experience

Leadership - at any level comes with its own kind of challenges. Generally speaking, the more senior the position you’re applying for is, the more you’ll have to answer questions of this nature. I’ve lumped technical leadership (Staff+ Engineering) and people leadership (Engineering Management) into one category here. While there are some questions you’ll usually only have to answer as a people manager I think they are close enough. Depending on the position, most of the interview may be spent in this section. **Hiring new leaders & managers has always been one of the most daunting tasks to me.** There’s so much upside when you get it right, but also so much downside when you get it wrong – as anyone who ever had a truly terrible manager can attest to.

Oftentimes these questions concern your ability to lead: Be it to ship projects, cause organizational change or help & grow those around you. These will usually be asked and discussed with concrete examples – so it’s best to **have a couple of projects and situations at hand that you can talk through**. You can find even more of those in the following “reflective questions” section.

Don’t let all the talk of manager roles here fool you though – **these questions may also be asked   for Senior or mid-level roles. Leadership at every level.**

**Example Questions**

* When leading a project, how do you make sure everyone is on the same page?
* What does it mean for a project to be successful? What can you do to make it successful?
* What’s the last failed project you’ve been a part of? What made it a failure? What would have been needed to make it a success?
* Have you ever mentored someone? What about? How do you mentor?
* What properties does a good hiring process have?
* Tell me about a change you initiated for your team/organization.
* On a daily basis, how do you interact with your reports? What are topics for 1o1s?
* Did you have to give negative feedback? What happened? How did you try to help improve the situation?
* How do you onboard someone new onto the team?
* Tell me about a situation you were pulled into to help out and fix a situation.
* How do you handle promotions?

## Reflective Questions

Essentially **interviews are a big exercise in reflection** : About your employment journey, the decisions and experiences you’ve made along the way as well as the technical knowledge you acquired. Nowhere is this more apparent than when explicit reflective questions are asked. The poster children of this are “What are your strengths?” and “What are your weaknesses?”. I implore you to be as genuine as you can be while answering them. If you just repeat some of the default answers websites give out, good interviewers will sniff that out. Of course the one for weaknesses is commonly “Oh, I’m too perfectionistic.” - aka say a weakness, that actually isn’t one. To me, it’s a bothersome balance as being too perfectionistic is _actually_ one of my weaknesses. It’s something I try to pull myself out of, to get more done without much loss of quality. Instead of painstakingly cataloging everything in detail, maybe a higher level overview that I can do in 20% of the time is actually better. Why do I tell you this? **As with basically all of the advice here, there’s always a chance it doesn’t apply.** So, if one of those “standard” answers is your actual honest answer, then go for it but also put in the work to make your interviewers believe it.

For many of these you may ask: “Why are people asking this? Do they actually expect me to tell them my weakness?” and the answer to that is: Interviewers want to see that **you understand what your limitations are.** That’s an important part of self-reflection. **We all have weaknesses, pretending we’re perfect either means we’re delusional, lying or have 0 self-reflection** – none of which bodes well for a future colleague. I wanna hammer this home, instead of pretending a negative thing doesn’t exist, **acknowledge it and highlight how you’re dealing with it.**

As a further example: “Tell me of a conflict you had at work”. First off, it can usually be rephrased to a “disagreement” – culturally, conflict seems to have wildly different connotations around the world. Saying “Oh, I never had any conflict/disagreement” is probably the worst answer. We all have conflicts. Be it about the direction of the company, a project or just code style – it happens. **Tell a real story**. This is why preparing for interviews can be beneficial – coming up with a story in the heat of the moment can be tough. I’ve created a mind map mapping many common reflective questions to a variety of experiences I’ve made. This helps me recall them during interviews.

Lastly, also filter the stories you tell somewhat. Preferably your story shouldn’t end with you leaving the company out of frustration. There’s only so much time in an interview, recounting a highly complex and nuanced situation may usually not be in your best interest: There are too many chances for the interviewers not to understand it completely or have doubts about how it unfurled. Hence, something simpler without being simplistic works – at best with a “happy end”. That said, one of my favorite stories to tell is how I left a company after a burlesque dancing incident and related concerns around sexism. It ends with me leaving the company after trying to improve the situation. I like to tell the story, as I hope that it sends a strong signal that I stand by my values and if there are similar problems present at the company I probably wouldn’t want to work there.

**Example Questions**

* What are your strengths?
* What are your weaknesses?
* Tell me about a mistake you made. How will you avoid making the mistake in the future?
* What was a big success for you?
* What would your ... say about you – positive & negative? (... being anything from colleagues, to manager, to CEO or even mother/father)
* Tell me about a conflict you had at work?
  * What happened?
  * How did you resolve it?
* Tell me about a time you changed your perspective on something important to you.
* What could you have done better at your last job?
* What processes would you like to improve at your last job?
* Why are you a programmer and not a product manager? Why are you a Team Lead instead of a Staff engineer?
* What is something you want to get better at?

## Your Questions in the end

Many companies these days **reserve time for your questions in the interview** , highlighting that interviewing is a 2-way process. Generally speaking, these should not be part of the interview evaluation. They should be there for you to genuinely figure out if it’s a place that **you want to work at**. This is also in the interest of the company, after all hiring someone just for them to quit again just months later is a gigantic waste of resources for the company. That said, it _is_ _still part of the interview_. If the interviewers had already gotten the impression that you’re only interested in the technical side and not product or people, only asking about their tech stack and specific libraries they use will reinforce that image.

You don’t have to ask questions, however it _can_ show a lack of interest in the company if you don’t ask a question. Hence, I’d recommend you to ask questions around topics that interest you. You have direct access right now, **use it**! What would impact your decision to work there? Ask about it! Usually this includes questions surrounding the way of work, culture and the tech stack.

Here are some topics you can ask about, given they haven’t been answered before or aren’t part of easily available public documentation:

* What do they like about company X? What do they dislike?
* Details about the tech stack
* What does a day in the life of a $your-position look like?
* What’s the biggest challenge facing the company right now?
* How many meetings do you have in a given week?
* $specific-question-about-company-business-model
* What helps someone be successful at company x?
* What do you wish you knew before you started working here?"

Now, if you face the opposite problem - you have too many questions, but not enough time to ask them - what should you do? Well, now you’re the interviewer, so moderate time well. Let them know you have a lot of questions and ask for short answers. Also, don’t be too afraid to interrupt them when they’re going off on a tangent. Ultimately, usually you have the possibility to ask your recruiter more questions or ask them during the next interview!

## Bonus-Tip: Reflection

Well, thanks for making it so far – it’s been a long blog post. I’ve thought for a long time about what it may be that usually makes me perform well in interviews. And I think I identified something! It’s this right here. No, not you reading this blog post. Me, writing it. I do a fair amount of writing about work related topics, I give talks and I talk with a lot of people about work. What I really do is **take time to reflect**. **Having discussed a topic or situation before – no matter if in a blog post or with friends over a beer – makes you better at talking about the same situation in an interview**. To be clear, it’s not about publishing any of this and what may come with it. I’m talking about **the process of reflection via writing & talking** – even if it never got published. It may be worth writing down some of these key points, lest you forget them (again, I have a mind map for this).

To illustrate this point, the easiest interview I probably ever had was a “Tech Deep Dive”. I was supposed to come prepared to talk about a complex technical topic for an hour. I talked about the design and implementation of my benchmarking library [benchee](https://github.com/bencheeorg/benchee). I didn’t even prepare for it. I didn’t need to, at this point I had given multiple talks about benchee – I could talk about it and all its design tradeoffs in my sleep. The interview was a breeze. It’s an extreme example and I realize not everyone will be this lucky but I hope it helps illustrate the point.

Another **great time to reflect is right after the interview**! How do you think the interview went? Were your answers on point? Did you go off track or get to the point too slowly? Was there a question you struggled to answer? How could you improve your answer the next time around? All this helps you get better throughout the process of interviewing!

## Closing

One of my other, but related, weaknesses is keeping it short as I always feel the urge to cover _everything_ – can you tell? ;) I hope this was helpful to you, despite or exactly because of it. Interviewing is tough. Running into a specific question that you know you should have an answer for but can’t come up with on the spot can feel devastating. Hence, I hope the catalog of example questions in this post will help you avoid this situation going forward. Of course, it’s also not fully comprehensive – I get surprised with questions in an interview every now and then still. Also, remember it’s not necessarily your fault. Sometimes interviews just _suck_ and failing them is more on the interviewers or the process than it is on you. Stay calm and keep going.

**You got this!**

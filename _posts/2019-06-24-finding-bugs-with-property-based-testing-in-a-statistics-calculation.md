---
layout: post
title: Finding Bugs with Property Based Testing in a Statistics Calculation
description: None
date: 2019-06-24 16:53:16 -0000
last_modified_at: 2019-06-24 16:53:16 -0000
publish: true
pin: false
image:
  path: /assets/uploads/2019/06/selection_054.png
categories: []
tags:
- edge cases
- Elixir
- percentiles
- property based testing
- statistics
- stream_data
- testing
---
I always loved the idea of [Property Based Testing](https://propertesting.com/book_foundations_of_property_based_testing.html), it was the most mind blowing idea I encountered while learning clojure many years back. However, I always found it hard to apply in practice. I barely encountered the "easy" case where an operation was reversible (if I encode a term and then decode it again it should be equal to the original term, for instance). And the properties I came up always seemed to _loose_ to catch any bugs. So, I thought well let's give it another shot. I got all these [statistics functions in benchee/statistex](https://github.com/bencheeorg/benchee/blob/075bf0af731ab4e506a121e5d686e9994fea928c/lib/statistex.ex) \- data should be easy to generate for them. Let's give it a shot, we'll surely not find a bug... or will we?

## The first property based tests

If nothing else, I wanted to make sure no matter what numbers you throw at my statistics module it won't blow up. To implement it I used [stream_data](https://github.com/whatyouhide/stream_data): 

Source: [https://gist.github.com/PragTob/092da503ae227d00977cccf50e3a2bbf](https://gist.github.com/PragTob/092da503ae227d00977cccf50e3a2bbf)

**File: `statistex_test.exs`**
```elixir
check all samples <- list_of(float(), min_length: 1) do
  stats = statistics(samples)

  assert stats.sample_size >= 1
  assert stats.minimum <= stats.maximum

  assert stats.minimum <= stats.average
  assert stats.average <= stats.maximum

  assert stats.minimum <= stats.median
  assert stats.median <= stats.maximum

  assert stats.median == stats.percentiles[50]

  assert stats.standard_deviation >= 0
  assert stats.standard_deviation_ratio >= 0

  # property that mode occurs in the sample omitted for brevity
end
```

 This is what I came up with - our samples are any non empty list of floats and there are a bunch of checks that make sure the values are somewhere between minimum and maximum or bigger than 0. No way the tests are failing...

## Wait, the tests are failing?!
  
     Failed with generated values (after 2 successful runs):
    
    * Clause: samples <- list_of(float(), min_length: 1) Generated: [-9.0, -1.0] Assertion with >= failed
    code: assert stats.standard_deviation_ratio() >= 0
    left: -1.131370849898476
    right: 0

Honestly, I was shocked. On closer inspection, the standard deviation ratio was negative when I said it should always be positive. As the generated sample only contains negative numbers the average is negative as well. As the ratio is calculated by dividing the standard deviation by the average it turned out to be negative. Usually I only work with positive samples, hence it never occurred before. The ratio should still always be positive so an `abs/1` call fixed it.

## Another property

Thinking more I came up with another property: 

Source: [https://gist.github.com/PragTob/a803ce4acfee5ce2b35f784eb4ef656d](https://gist.github.com/PragTob/a803ce4acfee5ce2b35f784eb4ef656d)

**File: `percentiles_prop.exs`**
```elixir
check all samples <- list_of(float(), min_length: 1) do
  percies = percentiles(samples, [25, 50, 75, 90, 99])

  assert percies[25] <= percies[50]
  assert percies[50] <= percies[75]
  assert percies[75] <= percies[90]
  assert percies[90] <= percies[99]
end
```

 It's much like the first properties, just making sure the percentile values are in order as they should there is absolutely no possibility that this will fail, absolutely none, well tested code... no chance it will fail ... **IT FAILED AGAIN?!?!?!**
  
     Failed with generated values (after 4 successful runs):
    
    * Clause: samples <- list_of(float(), min_length: 1)
    Generated: [1.0, 33.0]
    
    Assertion with <= failed
    code: assert percies[25] <= percies[50]
    left: 25.0
    right: 17.0

Wait, the 25th percentile is bigger than the 50th percentile? No way that's ok. A lot of digging, googling and reading our [original source for implementing percentile interpolation](https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm) later I figured out the problem. Basically interpolation for small sample sizes is hard and also uncommon. We missed a clause/case stated in the source, that points out that for a too small percentile and sample size the value is to be set to the minimum.

> Note that any _p_ ≤ 1/(_N_ +1) will simply be set to the minimum value.

Our p was 0.25 (25th percentile) and 0.25 <= 1/3. Implementing this clause (through guard clauses) fixed the test. You can check out the full implementation and bug fixes in the [PR](https://github.com/bencheeorg/benchee/pull/302).

## Learnings

The generation part was super easy in the case shown. However, what's impressive to me is that **although the properties were very loosely defined they still uncovered 2 bugs**. And that's in code that both me and many of you have been running for quite a while in benchee. Sure, they are very specific edge cases but that's what **property based testing is good at: Finding edge cases!** If you have other ideas for properties to check, I'm happy to listen and learn. And give property based testing a shot yourselves even with very loose properties - you might be surprised what you find.  

---
layout: post
permalink: https://pragtob.wordpress.com/2023/12/14/psa-double-check-benchee-benchmarks-made-with-elixir-versions-1-14-0-1-16-0-rc-0/
title: 'PSA: Double Check Benchee Benchmarks made with Elixir Versions 1.14.0 - 1.16.0-rc.0'
description: None
date: 2023-12-14 09:24:44 -0000
last_modified_at: 2023-12-14 09:24:44 -0000
publish: true
pin: false
categories:
- Elixir
- open source
tags:
- benchee
- fix
- optimization
- psa
---
Not too fun news here but huge thanks to [Jean Klingler](https://github.com/sabiwara) for [reporting it](https://github.com/bencheeorg/benchee/issues/406).

There is a known issue affecting elixir versions from 1.14.0 to 1.16.0-rc.0: Optimizations (SSA and bool passes, [see the original change](https://github.com/elixir-lang/elixir/pull/11420)) had been disabled affecting the performance of functions defined directly in the top level (i.e. outside of any module). The issue was fixed by re-enabling the optimization in [1.16.0-rc.1](https://github.com/elixir-lang/elixir/blob/v1.16/CHANGELOG.md#v1160-rc1-2023-12-12) ([commit with the fix](https://github.com/elixir-lang/elixir/commit/aabe46536e021da88de39bc5c82c90d97b0604ec#diff-1f4ed234972cb699fe6dc400f3bbf57f72919ef587ba6b1a43441c8b784b0cfb)). The issue is best show-cased by the following benchmark where we'd expect ~equal results:
  
    list = Enum.to_list(1..10_000)
    
    defmodule Compiled do
      def comprehension(list) do
        for x <- list, rem(x, 2) == 1, do: x + 1
      end
    end
    
    Benchee.run(%{
      "module (optimized)" => fn -> Compiled.comprehension(list) end,
      "top_level (non-optimized)" => fn -> for x <- list, rem(x, 2) == 1, do: x + 1 end
    })

The benchmark yields roughly these results on an affected elixir version, which is a stark contrast:
  
    Comparison:
    module (optimized)              18.24 K
    top_level (non-optimized)       11.91 K - 1.53x slower +29.14 μs
  
So, how do you fix it/make sure a benchmark you ran is not affected? All of these work:

* benchmark on an unaffected/fixed version of elixir (<= 1.13.4 or >= 1.16.0-rc.1)
* put the code you want to benchmark into a module (just like it is done in `Compiled` in the example above)
* you can also invoke `Benchee` from within a module, such as:

  defmodule Compiled do
    def comprehension(list) do
      for x <- list, rem(x, 2) == 1, do: x + 1
    end
  end
  
  defmodule MyBenchmark do
    def run do
      list = Enum.to_list(1..10_000)
  
      Benchee.run(%{
        "module (optimized)" => fn -> Compiled.comprehension(list) end,
        "top_level (non-optimized)" => fn -> for x <- list, rem(x, 2) == 1, do: x + 1 end
      })
    end
  end
  
  MyBenchmark.run()
  
Also note that even if all your examples are top level functions you should still follow these tips (on affected elixir versions), as the missing optimization might affect them differently. Further note, that even though your examples use top level functions they _may_ not be affected, as the specific disabled optimization may not impact them. Better safe than sorry though :)

## The Fun with Optimizations

A natural question here is _"why would anyone disable optimizations?"_ , which is fair. The thing with many optimizations is - they don't come for free! They might be better in the majority of the cases, but there is often still that part where they are slower. Think of the JVM and its great JIT - it gives you a great performance after a warmup period but during warmup it's usually slower than without a JIT (as it needs to perform the additional JIT work). If you want to read more on warmup times I have an [extensive blog post covering the topic](https://pragtob.wordpress.com/2017/08/29/careful-what-you-measure-2-1-times-slower-to-4-2-times-faster-mjit-versus-truffle-ruby/).

So, what was the goal here? As the [original PR](https://github.com/elixir-lang/elixir/pull/11420) states:

> Module bodies, especially in tests, tend to be long, which affects the performance of passe such as beam_ssa_opt and beam_bool. This commit disables those passes during module definition. As an example, this makes loading Elixir's test suite 7-8% faster.
>
> José Valim

Which naturally is a valid use case and a good performance gain. The unintended side effect here was, that it also affected "top level functions"/functions outside of any module which in 99.99% of cases doesn't matter and can be ignored. Let me reiterate this, this should not have affected any of your applications.

The problem here is that benchee was affected - as for ease of use we usually forego the definition of modules (while it's completely possible). And well, optimizations not being in effect when used with a benchmarking library is quite the problem :| 😭 Hence, this blog post along with a [notice in the README](https://github.com/bencheeorg/benchee#known-issues) to raise awareness.

So, if you ran benchmarks on affected elixir versions I recommend checking the above scenario and redoing the benchmarks with the above fixes applied.

On the positive side, I'm happy how quickly we got around to the issue after it was discovered, Jean opened the issue only 4 days after it was fixed in elixir and a day after it was released as part of the 1.16.0-rc.1. So, huge shout out and thank you again!

And for even more positive news: does this now mean our tests load slower again just so benchee can function without module definitons? No! At least as best as I understand the [fix](https://github.com/elixir-lang/elixir/commit/aabe46536e021da88de39bc5c82c90d97b0604ec#diff-1f4ed234972cb699fe6dc400f3bbf57f72919ef587ba6b1a43441c8b784b0cfb), it increases the _precision_ by disabling the compiler optimizations only in module bodies.

Happy benchmarking everyone!

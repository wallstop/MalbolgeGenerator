MalbolgeGenerator
=================

A Malbolge program generator written in python. Contains an assortment of useful malbolge methods

To generate a Malbolge program that prints out a string, simply import and call findString(your_string_here)

```powershel
λ» python
Python 3.11.2 (tags/v3.11.2:878ead1, Feb  7 2023, 16:38:35) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import MalbolgeInterpreter as m
>>> m.findString("Hello")
Hello
Source code: bCBA@?>=<;:9876543210/.-,+*)('&%$#"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@"!~}|4zy16v4-2rq).',+$j('g}C#cy?`v<z:xqYunsUTpihgOkMLbafedcba`Y^WVU=SXW9UT6LKPINMF.-,+A@?>&<A@?8765YF
'ioooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo*****p**po*opo**popoop*oo*p<o*p<*p<o<op*opo**oppp*o**ppooooooopoppp*poo*oo*ppopoop****pppp*pooopppp<v'
>>>
```

# where are the robots
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Exploitation, picoCTF 2019

Description: 
Can you find the robots?
https://jupiter.challenges.picoctf.org/problem/60915/ Or 
http://jupiter.challenges.picoctf.org:60915

Hints: 
1. What part of the website could tell you where the creator doesn't want you to look?
```
## Overview
### It asked where our robot was
![alt text](/CTF/picoCTF/Static/Images/where_are_the_robots/image.png)
## Solution
**Step1:** Exploit  
* Access /robots.txt  
=> Web returned `/8028f.html` => Access it to get the flag
## Flag
`picoCTF{ca1cu1at1ng_Mach1n3s_8028f}`
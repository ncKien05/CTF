# Unminify
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2024, obfuscation, browser_webshell_solvable

Description:  
I don't like scrolling down to read the code of my website, so I've squished it. As a bonus, my pages load faster!

Hints: 
1. Try CTRL+U / ⌘+U in your browser to view the page source. You can also add 'view-source:' before the URL, or try curl <URL> in your shell.
2. Minification reduces the size of code, but does not change its functionality. 
3. What tools do developers use when working on a website? Many text editors and browsers include formatting.
```
## Overview
![alt text](/picoCTF/Static/Images/Unminify/image.png)  
### Web tells us the flag has been passed, and we have to find it
## Solution
Read source code can get flag immediately (Use `Ctr+U`)
## Flag
`picoCTF{pr3tty_c0d3_622b2c88}`

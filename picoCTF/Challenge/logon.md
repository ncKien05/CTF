# logon
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2019

Description: 
The factory is hiding things from all of its users. Can you login as Joe and find what they've been looking at? 
https://jupiter.challenges.picoctf.org/problem/15796/ (link) Or 
http://jupiter.challenges.picoctf.org:15796

Hints: 
1. Hmm it doesn't seem to check anyone's password, except for Joe's?
```
## Overview
### As soon as we access the website, we can see a login form
![alt text](/CTF/picoCTF/Static/Images/logon/image1.png)  

* Try logging in with  
    * Username : test  
    * Password : test  

![alt text](/CTF/picoCTF/Static/Images/logon/image2.png)  

* As you can see, the website allows us to log in with any username and password, but it does not give us flags  
* Based on the Description section, try logging in with  
    * Username : Joe  
    * Password : test 

![alt text](/CTF/picoCTF/Static/Images/logon/image3.png)  
* It doesn't allow me to log in
## Solution
**Step1:** Exploit  
![alt text](/CTF/picoCTF/Static/Images/logon/image4.png)  
* Can see the cookie created when we log in successfully  
* In the cookie there is an admin parameter, which seems to be what is used to authenticate what roll we are logging in with  
* Currently admin is equal to `False`, try changing it to `True` and reload the web
## Flag
`picoCTF{th3_c0nsp1r4cy_l1v3s_6edb3f5f}`
# Cookies
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2021

Description: Who doesn't love cookies? Try to figure out the best one.
http://mercury.picoctf.net:64944/

Hints: none
```
## Overview
![alt text](/picoCTF/Static/Images/Cookies/image3.png)  
The website allows us to enter cookies into a box (can be similar to a placeholder).  
  
![alt text](/picoCTF/Static/Images/Cookies/image4.png)
## Solution
**Step1:** Use burpsuite to catch requests  
![alt text](/picoCTF/Static/Images/Cookies/image5.png)  
  
In request /check, you can see that the cookie is assigned a name parameter => mining point  
![alt text](/picoCTF/Static/Images/Cookies/image6.png)
**Step2:** Exploit  
Use intruder to bruteforce the name parameter  
![alt text](/picoCTF/Static/Images/Cookies/image7.png)  
## Flag
`picoCTF{3v3ry1_l0v3s_c00k135_cc9110ba}`

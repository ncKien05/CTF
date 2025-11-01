# Who are you?
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2021

Description:  
Let me in. Let me iiiiiiinnnnnnnnnnnnnnnnnnnn (http://mercury.picoctf.net:52362/)

Hints: 
It ain't much, but it's an RFC (https://tools.ietf.org/html/rfc2616)
```
## Overview
![alt text](/picoCTF/Static/Images/Who_are_you/image1.png)  
## Solution
**Step1:** Exploit  
Use burpsuite to catch requests  

![alt text](/picoCTF/Static/Images/Who_are_you/image2.png)  
* I changed the User-Agent header  

![alt text](/picoCTF/Static/Images/Who_are_you/image3.png)  
* I have added header Referer  

![alt text](/picoCTF/Static/Images/Who_are_you/image4.png)  
* I added Date header  

![alt text](/picoCTF/Static/Images/Who_are_you/image5.png)
* I have added header DNT  

![alt text](/picoCTF/Static/Images/Who_are_you/image6.png)
* I have added header X-Forwarded-For  

* And finally we will add the header `Accept-Language: sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7`
## Flag
`picoCTF{http_h34d3rs_v3ry_c0Ol_much_w0w_0c0db339}`
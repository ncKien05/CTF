# SQLiLite
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2022, sql

Description:
Can you login to this website?  

Hints: 
1. admin is the user you want to login as.
```
## Overview
![alt text](/picoCTF/Static/Images/SQLite/image1.png)  
* I tried logging in with:
    * Username: test
    * Password : test

![alt text](/picoCTF/Static/Images/SQLite/image2.png)
* And it always returns me the sqlite query (-_-)
## Solution
**Step1:** Exploit  
* Based on hint, it forces us to log in with Username admin  
* Try logging in with: 
    * Username : admin
    * Password : `' or 1=1 -- -`

![alt text](/picoCTF/Static/Images/SQLite/image3.png)  
* See source to get flags
## Flag
`picoCTF{L00k5_l1k3_y0u_solv3d_it_9b0a4e21}`

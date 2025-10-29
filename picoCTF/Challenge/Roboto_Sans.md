# Roboto Sans
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2022

Description:  
The flag is somewhere on this web application not necessarily on the website. Find it.

Hints: None
```
## Overview
![alt text](/CTF/picoCTF/Static/Images/Roboto_Sans/image1.png)  
* A health website  
## Solution
**Step1:** Recon  
* The post name is a suggestion, let's try accessing `robots.txt` to see what's there  
![alt text](/CTF/picoCTF/Static/Images/Roboto_Sans/image2.png)  
* As you can see, these are some base64 encoded snippets, try decoding them.  
    * ZmxhZzEudHh0 => flag1.txt  
    * anMvbXlmaW  =>  js/myfi  
    * anMvbXlmaWxlLnR4dA==  =>  js/myfile.txt  
* Now try accessing these links  
* It can be seen that both 1 and 2 are noise.  
* access `js/myfile.txt` to get the flag  
## Flag
`picoCTF{Who_D03sN7_L1k5_90B0T5_22ce1f22}`
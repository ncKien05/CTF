# findme
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF2023

Description:  
Help us test the form by submiting the username as test and password as test!

Hints: 
1. any redirections?
```
## Overview
![alt text](/picoCTF/Static/Images/findme/image1.png)  
* Login with:  
    * Username: test  
    * Password : test!  

![alt text](/picoCTF/Static/Images/findme/image2.png)  

## Solution
**Step 1:** Exploit  
* Use burpsuite to catch requests  

![alt text](/picoCTF/Static/Images/findme/image3.png)  
* We can see some quite interesting requests  

![alt text](/picoCTF/Static/Images/findme/image4.png)  
=> `cGljb0NURntwcm94aWVzX2Fs`
![alt text](/picoCTF/Static/Images/findme/image5.png)  
=> `bF90aGVfd2F5X2QxYzBiMTEyfQ==`
* Decode to get the flag
## Flag
'picoCTF{proxies_all_the_way_d1c0b112}'

# Get aHEAD
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2021

Description: Find the flag being held on this server to get ahead of the competition http://mercury.picoctf.net:53554/

Hints: 
1. Maybe you have more than 2 choices
2. Check out tools like Burpsuite to modify your requests and look at the responses
```
## Overview
###  A website that is quite painful to the eyes
![alt text](/picoCTF/Static/Images/Get_aHEad/image1.png)  
* When we click choose, the website will change color according to our choice
## Solution
**Step1:** Recon    
* Use burpsuite to catch requests  
![alt text](/picoCTF/Static/Images/Get_aHEad/image2.png)
![alt text](/picoCTF/Static/Images/Get_aHEad/image3.png)  
* We see that if you choose red, the website will use GET request to send, but if you choose blue, it will use POST request  

**Step2:** Exploit  
* The topic suggests we change GET to HEAD  
* Turn on intruder on burpsuite and select red  
* After catching the request, change GET to HEAD to get the flag
## Flag
`picoCTF{r3j3ct_th3_du4l1ty_2e5ba39f}`

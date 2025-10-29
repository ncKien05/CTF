# Cookie Monster Secret Recipe
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)

## Challenge information
```text
Tags : Web Exploitation, picoCTF 2025, browser_webshell_solvable

Description: 
Cookie Monster has hidden his top-secret cookie recipe somewhere on his website. 
As an aspiring cookie detective, your mission is to uncover this delectable secret. 
Can you outsmart Cookie Monster and find the hidden recipe?

Hints:
1. Sometimes, the most important information is hidden in plain sight. Have you checked all parts of the webpage?
2. Cookies aren't just for eating - they're also used in web technologies!
3.Web browsers often have tools that can help you inspect various aspects of a webpage, including things you can't see directly.
```
## Overview
When accessing the website, a login form appeared  
![alt text](/picoCTF/Static/Images/Cookies/image1.png)  
  
Try logging in with any username and password  
It can be seen that the web has blocked our access request  
![alt text](/picoCTF/Static/Images/Cookies/image2.png)  
=> We only need cookies to login
## Solution
**Step1:** Find cookie  
* Right-click on the web, select inspect, then go to application (On google)  
* In the Cookies section, we can see something quite interesting (%3D decrypt => '=')  
`secret_recipe: cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzJDODA0MEVGfQ%3D%3D`  
* After trying to decode it with base64 I got the flag
## Flag
`picoCTF{c00k1e_m0nster_l0ves_c00kies_2C8040EF}`

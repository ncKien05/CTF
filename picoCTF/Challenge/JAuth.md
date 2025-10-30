# JAuth
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoGym Exclusive

Description:  
Most web application developers use third party components without testing their security. Some of the past affected companies are:
Equifax (a US credit bureau organization) - breach due to unpatched Apache Struts web framework CVE-2017-5638
Mossack Fonesca (Panama Papers law firm) breach - unpatched version of Drupal CMS used
VerticalScope (internet media company) - outdated version of vBulletin forum software used
Can you identify the components and exploit the vulnerable one?
The website is running here. Can you become an admin?
You can login as test with the password Test123! to get started.
Hints: 
1. Use the web browser tools to check out the JWT cookie.
2. The JWT should always have two (2) . separators.
```
## Overview
![alt text](/picoCTF/Static/Images/JAuth/image1.png))
* A web login  
## Solution
**Step1:** Exploit  
* Use burpsuite to capture requests  
![alt text](/picoCTF/Static/Images/JAuth/image2.png)  
* As you can see, burpsuite has been able to crawl the web using JWT to authenticate accounts.  
![alt text](/picoCTF/Static/Images/JAuth/image3.png)  
* Web uses HS256 for signing  
* Now we will try to change the role to admin, but the web will force us to sign again, at this point try to change `HS256` to `none`, then delete the code after the second dot  
![alt text](/picoCTF/Static/Images/JAuth/image4.png)  
## Flag
`picoCTF{succ3ss_@u7h3nt1c@710n_bc6d9041}`
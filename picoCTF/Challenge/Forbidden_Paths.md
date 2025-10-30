# Forbidden Paths
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2022

Description: 
Can you get the flag?
We know that the website files live in /usr/share/nginx/html/ and the flag is at /flag.txt but the website is filtering absolute file paths. Can you get past the filter to read the flag?

Hints: None
```
## Overview  
![alt text](/picoCTF/Static/Images/Forbidden_Paths/image1.png)  
## Solution
**Step1:** Exploit  
* The web allows us to read files on the system, but we cannot use absolute paths.  
* We can use `../` to point back to the file  
* In the introduction, we know that website files live in `/usr/share/nginx/html/`, now we will use `../../../../` to point back to root, then point to the `flag.txt` file and read it.  
## Flag
`picoCTF{7h3_p47h_70_5ucc355_e5a6fcbc}`
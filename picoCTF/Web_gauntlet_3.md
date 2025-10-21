# Web Gauntlet 3
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
   
## Challenge information
```text
Tags: Web Exploitation, picoCTF 2021

Description:
Last time, I promise! Only 25 characters this time. Log in as admin Site: http://mercury.picoctf.net:32946/
Filter: http://mercury.picoctf.net:32946/filter.php

Hints:
1. Each filter is separated by a space. Spaces are not filtered.
2. There is only 1 round this time, when you beat it the flag will be in filter.php.
3. Sqlite
```

## Overview
Similar to other web-gauntlet challenges, we also have a login form  
The challenge's requirement is to force us to log in as admin  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/b1e7b3bb-fa01-4bb9-afca-2c16dba4b265" />  
  
The /filter.php page tells us that some are automatically blacklisted  
Use burpsuite to see some missing characters  
`Filters: or and true false union like = > < ; -- /* */ admin<br/>`  
## Solution
**Step1:** Recon  
* We will try to do it the way in [Web_gauntlet_2](https://github.com/ncKien05/CTF/blob/main/picoCTF/Web_Gauntlet_2.md)  
* Here you can see that the website does not allow us to enter more than 25 characters  
  <img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/cd7c4218-b5ff-4080-b649-712776daf1c7" />

**Step2:** Bypass username
* The website blocks `admin` so I cannot enter directly, we can enter via string concatenation  
  <img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/b52f69a9-0e85-4b1e-b4b9-cfff56a53733" />

**Step3:** Bypass password
* There are many bypass methods that have been filtered, but it is not impossible
* I will use an operator that operates quite similar to LIKE => `GLOB`
* I will transmit:  
    * Username : ad’||’min  
    * Password : ' GLOB '*  
## Flag
Visit /filter.php to get the flag  
`picoCTF{k3ep_1t_sh0rt_ef4a5b40aa736f5016b4554fecb568d0}`

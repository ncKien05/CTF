# Web Gauntlet
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
- [References](#references)
## Challenge information
```text
Tags: Web Exploitation, picoCTF 2020 Mini-Competition

Description: Can you beat the filters? Log in as admin
http://shape-facility.picoctf.net:62185/
http://shape-facility.picoctf.net:62185/filter.php

Hints:
1. You are not allowed to login with valid credentials.
2. Write down the injections you use in case you lose your progress.
3. For some filters it may be hard to see the characters, always (always) look at the raw hex in the response.
4. Sqlite
5. If your cookie keeps getting reset, try using a private browser window
```
## Overview
* Visit the website and you will find a login page  
* The challenge's requirement is to force us to log in with the username admin  
* Pass 5 round to receive the flag  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/c2f08aeb-cbd8-4d7c-acd4-79d22a193797" />  
  
## Solution
**Step1:** Recon  
* I first tried to login with  
    * Username: `admin`  
    * Password: `admin`  
* The following SQL statement was printed: `SELECT * FROM users WHERE username='admin' AND password='admin123'`  
   => So it can be guessed that we can bypass login through SQL Injection  
* Hint also gives us information about the website using Database Sqlite
  
**Step2:** Round 1 / 5    
* First we'll see what `/filter.php` has: `Round1: or`    
  => So I guess any `OR`-statements are filtered out.  
* I used the comment `--` to effectivly comment out the rest of the `SELECT`-statement.  
* Logging in with  
    * Username: `admin' -- -`  
    * Password: `123`  

Web returned the message `Congrats! On to round 2`.  

**Step3:** Round 2 / 5  
* Page `/filter.php` returns: `Round2: or and like = --`  
  => We cannot use -- comments any more. Neither OR, AND, LIKE, =.
* Let's use a `/*comment*/`
* Logging in with  
    * Username: `admin'/*`  
    * Password: `123`

Web returned the message `Congrats! On to round 3`.

**Step4:** Round 3 / 5  
* Re-checking `/filter.php` showed: `Round3: or and = like > < --`  
  => It's impossible to see in a regular browser (use hex-output in Burp instead), but the space character is also included in the list of filters.  
* The above expression also works here but let's choose another one, one with the `;` character that ends SQL-statements.
* Logging in with  
    * Username: `admin';`  
    * Password: `123`

Web returned the message `Congrats! On to round 3`.  
**Step5:** Round 4 / 5  
* Page `/filter.php` returns: `Round4: or and = like > < -- admin`
* We cannot use the string `admin` any more. But we can use SQL's string concatenation method
* Logging in with  
    * Username: `ad'||'min';`  
    * Password: `123`

Web returned the message `Congrats! On to round 4`.  
**Step6:** Round 5 / 5  
* Re-checking `http://jupiter.challenges.picoctf.org:9683/filter.php` showed: `Round5: or and = like > < -- union admin`  
  As before the space character is also included in the list of filters.
* We can re-use the same credentials as in round 4 to get the message: `Congrats! You won! Check out filter.php`

## Flag
Check /filter.php to get the flag  
`picoCTF{y0u_m4d3_1t_79a0ddc6}`
## References
[Sqlite](https://www.sqlite.org/docs.html)  
[SQL Injection](https://portswigger.net/web-security/sql-injection)

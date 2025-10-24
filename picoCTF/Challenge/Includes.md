# Includes
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2022, inspector

Description: Can you get the flag?

Hints: Is there more code than what the inspector initially shows?
```
## Overview
![alt text](/CTF/picoCTF/Static/Images/Includes/image.png)
* Web show gives us a text, i tried clicking say hello and the web alerted out a text `This code is in a separate file!`
## Solution
* Based on the hint the web just alerted us  
=> `Ctr+U` to view source :)  
* I can see the web is importing style.css and script.js, let's see how it looks  
```CSS
body {
  background-color: lightblue;
}

/*  picoCTF{1nclu51v17y_1of2_  */
```
```Javascript
function greetings()
{
  alert("This code is in a separate file!");
}

//  f7w_2of2_6edef411}
```
## Flag
`picoCTF{1nclu51v17y_1of2_f7w_2of2_6edef411}`
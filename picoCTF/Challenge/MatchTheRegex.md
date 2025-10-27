# MatchTheRegex
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2023

Description:  
How about trying to match a regular expression

Hints:
1. Access the webpage and try to match the regular expression associated with the text field 
```
## Overview
![alt text](/CTF/picoCTF/Static/Images/MatchTheRegex/image.png)  
## Solution
**Step1:** Exploit  
* In soure there is a rather strange piece of js  
```Javascript
	function send_request() {
		let val = document.getElementById("name").value;
		// ^p.....F!?
		fetch(`/flag?input=${val}`)
			.then(res => res.text())
			.then(res => {
				const res_json = JSON.parse(res);
				alert(res_json.flag)
				return false;
			})
		return false;
	}
```
* We can enter the line `^p.....F!?` to get the flag  
## Flag
`picoCTF{succ3ssfully_matchtheregex_2375af79}`
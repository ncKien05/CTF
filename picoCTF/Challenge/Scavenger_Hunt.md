# Scavenger Hunt
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2021

Description: There is some interesting information hidden around this site: http://mercury.picoctf.net:27393/
Can you find it?

Hints: 
1. You should have enough hints to find the files, don't run a brute forcer.
```
## Overview
### Just some boring HTML
![alt text](/CTF/picoCTF/Static/Images/Scavenger_Hunt/image1.png)
![alt text](/CTF/picoCTF/Static/Images/Scavenger_Hunt/image2.png)  
## Solution
**Step1:** Analysis  
* The What tag of the web suggests to us what the web uses to code, which can be exploited from here  

**Step2:** Exploit  
* This is the HTML snippet  
```HTML
<!doctype html>
<html>
  <head>
    <title>Scavenger Hunt</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans|Roboto" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="mycss.css">
    <script type="application/javascript" src="myjs.js"></script>
  </head>

  <body>
    <div class="container">
      <header>
		<h1>Just some boring HTML</h1>
      </header>

      <button class="tablink" onclick="openTab('tabintro', this, '#222')" id="defaultOpen">How</button>
      <button class="tablink" onclick="openTab('tababout', this, '#222')">What</button>

      <div id="tabintro" class="tabcontent">
		<h3>How</h3>
		<p>How do you like my website?</p>
      </div>

      <div id="tababout" class="tabcontent">
		<h3>What</h3>
		<p>I used these to make this site: <br/>
		  HTML <br/>
		  CSS <br/>
		  JS (JavaScript)
		</p>
	<!-- Here's the first part of the flag: picoCTF{t -->
      </div>

    </div>

  </body>
</html>
```
=> `picoCTF{t`
* This is the CSS snippet
```CSS
div.container {
    width: 100%;
}

header {
    background-color: black;
    padding: 1em;
    color: white;
    clear: left;
    text-align: center;
}

body {
    font-family: Roboto;
}

h1 {
    color: white;
}

p {
    font-family: "Open Sans";
}

.tablink {
    background-color: #555;
    color: white;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    font-size: 17px;
    width: 50%;
}

.tablink:hover {
    background-color: #777;
}

.tabcontent {
    color: #111;
    display: none;
    padding: 50px;
    text-align: center;
}

#tabintro { background-color: #ccc; }
#tababout { background-color: #ccc; }

/* CSS makes the page look nice, and yes, it also has part of the flag. Here's part 2: h4ts_4_l0 */
```
=> `h4ts_4_l0`
* This is the JS snippet  
```Javascript
function openTab(tabName,elmnt,color) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
	tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
	tablinks[i].style.backgroundColor = "";
    }
    document.getElementById(tabName).style.display = "block";
    if(elmnt.style != null) {
	elmnt.style.backgroundColor = color;
    }
}

window.onload = function() {
    openTab('tabintro', this, '#222');
}

/* How can I keep Google from indexing my website? */
```
=> Coming here, you don't know what to do, right? :))

* If you want to prevent Google from indexing, you can use a robots.txt file => Try accessing it  
* Then the web gives us one more fact `I think this is an apache server... can you Access the next flag?`  
* You can try accessing the configuration file on Apache(.htacess)    
* Then the web gives us one more fact `I love making websites on my Mac, I can Store a lot of information there.`  
* .DS_Store is a file macOS automatically creates in folders to store display settings   
* Some programmers accidentally upload the .DS_Store file to a Git repository or server. The .DS_Store file then becomes part of the website and anyone can download it => Try accessing it
## Flag
`picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k_d375c750}`
# Search source
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
- [Reference](#reference)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2022

Description:  
The developer of this website mistakenly left an important artifact in the website source, can you find it?

Hints: 
1. How could you mirror the website on your local machine so you could use more powerful tools for searching?
```
## Overview
![alt text](/picoCTF/Static/Images/Search_source/image1.png)  
* A yoga website  
* This is source page
  
![alt text](/picoCTF/Static/Images/Search_source/image2.png)  
## Solution
**Step1:** Exploit  
* Use `wget -r [link_to_page]` to download recursive  
* Use `grep -ri "pico" path/to/folder` to find flag
## Flag
`picoCTF{1nsp3ti0n_0f_w3bpag3s_8de925a7}`
## Reference
[Recursive](https://www.gnu.org/software/wget/manual/wget.html#Recursive-Download)

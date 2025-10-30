1. Access the challenge

   <img width="1918" height="1044" alt="image" src="https://github.com/user-attachments/assets/0cfeea1c-1419-474b-a3ee-54dfe9e27181" />
* After logging in, we understand the challenge wants us to access /admin

  <img width="1218" height="318" alt="image" src="https://github.com/user-attachments/assets/d888e934-616b-4b0b-b042-3ad2f452ea35" />
* When accessing /admin, we are denied due to lack of permission.

  <img width="1776" height="698" alt="image" src="https://github.com/user-attachments/assets/4745959f-1a2a-4d3f-ad32-8c912de70339" />
* Since the current role of the session is user, we probably need to change the role back to admin, and re-sign the jwt properly.

  <img width="1525" height="937" alt="image" src="https://github.com/user-attachments/assets/b684ddf2-f002-48f5-b155-03db97469844" />
* The application uses the RS256=RSA + SHA256 algorithm to sign, which means it uses public key encryption.

2. Identify the gap
Attacking JWT we have test cases like:
* Application does not verify signature  
* Application does not verify algorithm  
* Header parameter injection  
* Algorithm Confusion  
Forcing us to test every test case, and if this JWT has a problem, it will fall into one of the above test cases  
For this article, the vulnerability will be in the Algorithm Confusion test case

3. Find the public key
For the Algorithm Confusion exploit, we need to find the public key located on the server. To find the public key, we have 2 ways  
* Method 1: Use tools such as dirsearch, gobuster, .. to search by wordlist  
* Method 2: From 2 valid JWTs, calculate the public key  

<img width="1121" height="557" alt="image" src="https://github.com/user-attachments/assets/50b60e69-6f55-4a73-9749-ee79f0c097b7" />  
In method 1 we find the public key at `/.well-known/jwks.json`  

<img width="1541" height="556" alt="image" src="https://github.com/user-attachments/assets/8ff916bb-0007-43d0-bda3-58784df515fa" />  
4. From the collected public key, we convert it to PEM format according to the x509 algorithm format.  

<img width="1917" height="1055" alt="image" src="https://github.com/user-attachments/assets/5e28f844-42c3-4ca0-8f24-5a1cd9c4f294" />  
* Then the tool will automatically format for us.

<img width="1900" height="1019" alt="image" src="https://github.com/user-attachments/assets/60e8fd38-4e9f-4a43-b649-14711ea8aa18" />  

5. From the reformatted PEM public key, we proceed to create a symmetric key.  
* Encode base64 PEM public key

  <img width="1920" height="519" alt="image" src="https://github.com/user-attachments/assets/8aa39811-135d-48f4-a739-b49e11cffd56" />
  Copy the base64 encoded string
* Next, create a symmetric key following these steps:

  <img width="1920" height="1058" alt="image" src="https://github.com/user-attachments/assets/e3b37bd4-d4fc-4762-a1b4-2dde20be790d" />

6. Re-sign JWT with symmetric key
   
   <img width="1533" height="899" alt="image" src="https://github.com/user-attachments/assets/18fd2b6f-8d66-455a-96d0-5e0c1c694d8e" />
* After completing the above 6 steps, click send request

<img width="1531" height="983" alt="image" src="https://github.com/user-attachments/assets/f68bad39-7109-43f9-991b-e13940691f33" />  

FROM THE [SOURCE](https://nguyengiangnam.notion.site/WU-PTITCTF-2025-260091b6851e807babfdcce2bba84411)











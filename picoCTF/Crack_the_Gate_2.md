# Overview
When entering the website, a login page appears  
<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/4669b9a0-657d-4a6b-b9c8-3d43654a55b7" />  
**Hint 1:** What IP does the server think you’re coming from?  
**Hint 2:** Read more about [X-forwarded-For](https://www.typeerror.org/docs/http/headers/x-forwarded-for)  
**Hint 3:** You can rotate fake IPs to bypass rate limits.  

The challenge is to provide us with an email and a list of passwords  
Email: ctf-player@picoctf.org  
Password: [Download here](https://challenge-files.picoctf.net/c_amiable_citadel/f7976d25bf2051cdee03f24a92791f4116c6eaf4ab5d7542462535051265613c/passwords.txt)  
It seems like the web forces us to find the correct password in this list  
Now I will try to log in with a few passwords  
<img width="500" height="350" alt="Screenshot 2025-10-20 221437" src="https://github.com/user-attachments/assets/336a8eff-041b-42f2-9802-4f057143d161" />  
If you enter the wrong password twice, you will have to wait 20 minutes, which is terrible  
It seems like the IP is what helps the web realize we're trying to bruteforce  

# Writeup
**B1:** I will use burpsuite to catch the request  
<img width="500" height="350" alt="Screenshot 2025-10-20 221831" src="https://github.com/user-attachments/assets/a64f87f8-c6f8-49a4-bfe1-d7efc9aeb1f2" />  
**B2:** As mentioned above, I will try spoofing my IP to see how it goes  
<img width="500" height="350" alt="Screenshot 2025-10-20 222157" src="https://github.com/user-attachments/assets/6783bc61-5378-4dee-a3cc-db7ed3cf47cf" />  
This was truly successful  
**B3:** Now I will use Intruder to bruteforce the password  
<img width="500" height="350" alt="Screenshot 2025-10-20 222453" src="https://github.com/user-attachments/assets/d1751e99-4922-4a02-b5a8-3cf5c1cea7d3" />  

Flag will be returned  
<img width="500" height="350" alt="Screenshot 2025-10-20 222929" src="https://github.com/user-attachments/assets/10f85845-1d16-413d-9ba9-e1c9c7b19ce2" />


1. After registering and logging in, we are redirected to the dashboard interface.
   
   <img width="1919" height="1143" alt="image" src="https://github.com/user-attachments/assets/0ca0a98a-8d38-426f-8fd2-bcb51b45bf8d" />

2. Proceed to upload 1 file

   <img width="1920" height="1148" alt="image" src="https://github.com/user-attachments/assets/cbf2d218-9faa-49f1-965b-bee0e43cb691" />
After uploading, we can download the file just uploaded, click to download the file  
`NOTE: Please perform all functions to understand the application before Pentest`  

3. After downloading the file, go back to the proxy history on burpsuite and review it.

   <img width="1920" height="1059" alt="image" src="https://github.com/user-attachments/assets/5ed31861-ff47-44c6-932e-59d1f95e4fb4" />

We see here that there are 2 locations that can be chosen to start testing  
* Looking at location number 1, we think of the Path traversal vulnerability  
* Looking at location number 2, we think of the File upload vulnerability  
* Looking at the response, we know that the application server is Flask

When starting, we will choose the most accessible path, of the 2 locations, location 1 is the easiest to start  

4. Conduct Path traversal at location 1

   <img width="1473" height="684" alt="image" src="https://github.com/user-attachments/assets/169db382-6f40-4ad7-98a0-b19cc5576b71" />  
  
We see that the filename parameter takes a file name and returns the file's contents.  
The question is: What if the file passed in is a file on the system? Will the application return the file's contents?  

5. Read the file `/etc/passwd`

   <img width="1453" height="1007" alt="image" src="https://github.com/user-attachments/assets/15ca2e3b-6511-4909-9f57-0f049e7e13fd" />

⇒ The assumption is true, the application can read files on the system. We can read any file if that file has read permission for the user running the web server  
The question is: How do we know where the Flag is to read it?  
To answer this question, we need to reconfigure the environment the server is running through reading files such as: command line history, Cronjob, SSH key, automatic script, environment variables  

6. Perform system reset by reading environment variables
`/proc/self/environ` is a **virtual file** in the `procfs` system, containing the **environment variables** of the **current process** (i.e. the process reading this file).

- `/proc/self` is a **symlink** pointing to the `/proc/<PID>` directory of the **current process**.

- `/proc/self/environ` is the equivalent of the `$ENV` variable of that process.

⇒ This file can be sensitive as it can contain information such as paths, local settings, and sometimes passwords or API tokens if they are stored in environment variables 

<img width="1457" height="904" alt="image" src="https://github.com/user-attachments/assets/fde7326f-11c0-44d2-89b5-7407963675dc" />   
⇒ We get the path to the file containing the Flag  





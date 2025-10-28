# SQL Direct
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2022, sql 

Description: 
Connect to this PostgreSQL server and find the flag!

Hints: 
1. What does a SQL database contain?
```
## Overview
* Start the challenge to get the server login code, for example:
    * psql -h saturn.picoctf.net -p 58461 -U postgres pico
    * Password is postgres

![alt text](/CTF/picoCTF/Static/Images/SQL_Direct/image1.png)
## Solution
* Because we already know it uses the postgres database, we will skip the recon step  
**Step1 :** Exploit  
* First we will define version(), use: `SELECT version();`  
=> Know the challenge of using PostgreSQL 15.2 refer [here](https://www.postgresql.org/docs/release/15.2/)
* use `SELECT table_name FROM information_schema.tables WHERE table_name ILIKE 'fl%';` to find the flags table  
* Read the flags table to get flags  
## Flag
'picoCTF{L3arN_S0m3_5qL_t0d4Y_73b0678f}'
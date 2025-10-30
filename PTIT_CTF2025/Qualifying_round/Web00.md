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
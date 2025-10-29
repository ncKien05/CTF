# Java Code Analysis!?!
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
- [Reference](#reference)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2023

Description:  
BookShelf Pico, my premium online book-reading service.
I believe that my website is super secure. I challenge you to prove me wrong by reading the 'Flag' book!

Hints:
1. Maybe try to find the JWT Signing Key ("secret key") in the source code? Maybe it's hardcoded somewhere? Or maybe try to crack it?
2. The 'role' and 'userId' fields in the JWT can be of interest to you!
3. The 'controllers', 'services' and 'security' java packages in the given source code might need your attention. We've provided a README.md file that contains some documentation.
4.  Upgrade your 'role' with the new (cracked) JWT. And re-login for the new role to get reflected in browser's localStorage.
```
## Overview
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image1.png)  
* I tried logging in with any email and password, it returned `login failed`  
* I created an account with:  
    * Username : hacker
    * Mail: hacker@gmail.com
    * Password: Hacker@1  

* I created an account successfully and it logged me in  

![alt text](/picoCTF/Static/Images/Java_Code_Analys/image2.png)

* This is my profile
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image3.png)  

* I can upload my avatar or change my password, it sounds like a file upload vulnerability, but we don't exploit it here.
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image4.png)  

* I see that there is a book outside the home that is a flag. After accessing it, it requires me to have admin rights to view it. This will be the main exploitation point of this article (login with admin).
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image5.png)  

* Read the source provided for better understanding
## Solution
**Step1:** Recon  
* I used burpsuite to catch requests when I logged in  
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image6.png)  
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image7.png)  
* As you can see, this is a JWT vulnerability, we can exploit it to log in with admin rights  
* This is the jwt code initialized by the web

```
Headers = {
  "typ": "JWT",
  "alg": "HS256"
}

Payload = {
  "role": "Free",
  "iss": "bookshelf",
  "exp": 1762172905,
  "iat": 1761568105,
  "userId": 6,
  "email": "hacker@gmail.com"
}

Signature = "KgSMr-IgBCERM85wFwvSaAbXoXHuRBZqwShjk1OO5b4"
```
* As you can see, the jwt code uses HS256 (a symmetric key) to sign  

```SQL
INSERT INTO roles VALUES ('Free', 1);
INSERT INTO roles VALUES ('Basic', 2);
INSERT INTO roles VALUES ('Premium', 3);
INSERT INTO roles VALUES ('Admin', 4);
```
* There are 4 roles initialized as above  
* Our job is to think of a way to find the public key, then change the role to admin and re-sign the jwt  

* This is the code of the JWTService section  
```java
package io.github.nandandesai.pico.security;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;
import io.github.nandandesai.pico.security.models.JwtUserInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Calendar;
import java.util.Date;

@Service
public class JwtService {

    private final String SECRET_KEY;

    private static final String CLAIM_KEY_USER_ID = "userId";
    private static final String CLAIM_KEY_EMAIL = "email";
    private static final String CLAIM_KEY_ROLE = "role";
    private static final String ISSUER = "bookshelf";

    @Autowired
    public JwtService(SecretGenerator secretGenerator){
        this.SECRET_KEY = secretGenerator.getServerSecret();
    }

    public String createToken(Integer userId, String email, String role){
        Algorithm algorithm = Algorithm.HMAC256(SECRET_KEY);

        Calendar expiration = Calendar.getInstance();
        expiration.add(Calendar.DATE, 7); //expires after 7 days

        return JWT.create()
                .withIssuer(ISSUER)
                .withIssuedAt(new Date())
                .withExpiresAt(expiration.getTime())
                .withClaim(CLAIM_KEY_USER_ID, userId)
                .withClaim(CLAIM_KEY_EMAIL, email)
                .withClaim(CLAIM_KEY_ROLE, role)
                .sign(algorithm);
    }

    public JwtUserInfo decodeToken(String token) throws JWTVerificationException {
        Algorithm algorithm = Algorithm.HMAC256(SECRET_KEY);
        JWTVerifier verifier = JWT.require(algorithm)
                .withIssuer(ISSUER)
                .build();
        DecodedJWT jwt = verifier.verify(token);
        Integer userId = jwt.getClaim(CLAIM_KEY_USER_ID).asInt();
        String email = jwt.getClaim(CLAIM_KEY_EMAIL).asString();
        String role = jwt.getClaim(CLAIM_KEY_ROLE).asString();
        return new JwtUserInfo().setEmail(email)
                .setRole(role)
                .setUserId(userId);
    }
}
```
* It can be seen that `expires after 7 days` 
=> There is no need to worry about the expiration time jwt  
```java
 public JwtService(SecretGenerator secretGenerator){
        this.SECRET_KEY = secretGenerator.getServerSecret();
    }
``` 
*   The secret key is obtained from `secretGenerator` , now let's take a look  
```java
package io.github.nandandesai.pico.security;

import io.github.nandandesai.pico.configs.UserDataPaths;
import io.github.nandandesai.pico.utils.FileOperation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.charset.Charset;

@Service
class SecretGenerator {
    private Logger logger = LoggerFactory.getLogger(SecretGenerator.class);
    private static final String SERVER_SECRET_FILENAME = "server_secret.txt";

    @Autowired
    private UserDataPaths userDataPaths;

    private String generateRandomString(int len) {
        // not so random
        return "1234";
    }

    String getServerSecret() {
        try {
            String secret = new String(FileOperation.readFile(userDataPaths.getCurrentJarPath(), SERVER_SECRET_FILENAME), Charset.defaultCharset());
            logger.info("Server secret successfully read from the filesystem. Using the same for this runtime.");
            return secret;
        }catch (IOException e){
            logger.info(SERVER_SECRET_FILENAME+" file doesn't exists or something went wrong in reading that file. Generating a new secret for the server.");
            String newSecret = generateRandomString(32);
            try {
                FileOperation.writeFile(userDataPaths.getCurrentJarPath(), SERVER_SECRET_FILENAME, newSecret.getBytes());
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            logger.info("Newly generated secret is now written to the filesystem for persistence.");
            return newSecret;
        }
    }
}
```
* From the code above, we can simply understand `secretkey=1234`  

**Step2:** Exploit  
* Create a jwt code with role admin, userID equal to 2 (I tried 1 but it didn't work) and re-sign the code with secretkey =1234  
`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiQWRtaW4iLCJpc3MiOiJib29rc2hlbGYiLCJleHAiOjE3NjIxNzU2MTIsImlhdCI6MTc2MTU3MDgxMiwidXNlcklkIjoyLCJlbWFpbCI6ImhhY2tlckBnbWFpbC5jb20ifQ.ogABvx_CsEmSjXNp87OEQ5jY7qUMIkNmV3gu7SZTRWw`
* Select inspect then go to local storage and change the parameters to make them valid  
![alt text](/picoCTF/Static/Images/Java_Code_Analys/image8.png)  
## Flag
`picoCTF{w34k_jwt_n0t_g00d_6e5d7df5}`
## Reference
[JWT](https://portswigger.net/web-security/jwt)

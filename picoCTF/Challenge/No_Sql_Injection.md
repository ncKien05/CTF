# No Sql Injection
- [Challenge information](#challenge-information)
- [Overview](#overview)
- [Solution](#solution)
- [Flag](#flag)
## Challenge information
```text
Tags: Web Explotation, picoCTF 2024, browser_webshell_solvable

Description:  
Can you try to get access to this website to get the flag?
You can download the source here (https://artifacts.picoctf.net/c_atlas/38/app.tar.gz).

Hints: 
1. Not only SQL injection exist but also NonSQL injection exists
2. Make sure you look at everything the server is sending back.
```
## Overview
![alt text](/CTF/picoCTF/Static/Images/No_SQL_INJECTION/image1.png)  
## Solution
**Step1:** Recon  
```Python
const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const { MongoMemoryServer } = require("mongodb-memory-server");
const path = require("path");
const crypto = require("crypto");

const app = express();
const port = process.env.PORT | 3000;

// Middleware to parse JSON data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// User schema and model
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  password: { type: String, required: true },
  token: { type: String, required: false, default: "{{Flag}}" },
});

const User = mongoose.model("User", userSchema);

// Initialize MongoMemoryServer and connect to it
async function startServer() {
  try {
    const mongoServer = await MongoMemoryServer.create();
    const mongoUri = mongoServer.getUri();
    await mongoose.connect(mongoUri);

    // Store initial user
    const initialUser = new User({
      firstName: "pico",
      lastName: "player",
      email: "picoplayer355@picoctf.org",
      password: crypto.randomBytes(16).toString("hex").slice(0, 16),
    });
    await initialUser.save();

    // Serve the HTML form
    app.get("/", (req, res) => {
      res.sendFile(path.join(__dirname, "index.html"));
    });

    // Serve the admin page
    app.get("/admin", (req, res) => {
      res.sendFile(path.join(__dirname, "admin.html"));
    });

    // Handle login form submission with JSON
    app.post("/login", async (req, res) => {
      const { email, password } = req.body;

      try {
        const user = await User.findOne({
          email:
            email.startsWith("{") && email.endsWith("}")
              ? JSON.parse(email)
              : email,
          password:
            password.startsWith("{") && password.endsWith("}")
              ? JSON.parse(password)
              : password,
        });

        if (user) {
          res.json({
            success: true,
            email: user.email,
            token: user.token,
            firstName: user.firstName,
            lastName: user.lastName,
          });
        } else {
          res.json({ success: false });
        }
      } catch (err) {
        res.status(500).json({ success: false, error: err.message });
      }
    });

    app.listen(port, () => {
    });
  } catch (err) {
    console.error(err);
  }
}

startServer().catch((err) => console.error(err));
```
* I see a few exploits in the server.py code of the web  
    * First, we can use the email `picoplayer355@picoctf.org` to log in  
    * There is a piece of code that when we look at it we can immediately see that this is a NoSQL Injection vulnerability  
```Python
const user = await User.findOne({
          email:
            email.startsWith("{") && email.endsWith("}")
              ? JSON.parse(email) // <--- VUL
              : email,
          password:
            password.startsWith("{") && password.endsWith("}")
              ? JSON.parse(password) // <--- VUL
              : password,
        });
```
**Step2:** Exploit  
* After identifying the vulnerability, everything becomes simple  
* Try logging in with  
    * email : picoplayer355@picoctf.org
    * password: {"$ne": null}
* We can now log in as admin  

![alt text](/CTF/picoCTF/Static/Images/No_SQL_INJECTION/image2.png)  
* But in the page there is no flag we need, let's repeat what we just did and use burpsuite to catch the request  

![alt text](/CTF/picoCTF/Static/Images/No_SQL_INJECTION/image3.png)  
## Flag
`picoCTF{jBhD2y7XoNzPv_1YxS9Ew5qL0uI6pasql_injection_25ba4de1}`
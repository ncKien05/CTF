# Overview
Upon entering the website, we are immediately greeted by a very confusing piece of shortened code:   
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/a32b80ef-0ac8-421a-8aa3-737eb5715c5f " />  
It seems it's asking us to enter the appropriate value in the input box for the expression to return True.  
Complete 4 stages to get the flag.  
# Writeup
**Stage 1:** `(![]+[]) [+[]] + ([][[]]+[]) [+!+[]] + ({}+[]) [+!+[]+!+[]] == input`  
That's a **JavaScript obfuscation** => The simplest way is to use console log to decode.  
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/7baf56ef-d071-4a06-b87f-23f6eb88e2cd" />  

**Stage 2:** `typeof a == 'number' && a !== NaN && (a - 1 < a) == false`  
Analysis:  
* `typeof a == 'number'` => a is of type number  
* `a !== NaN` => a is not equal to NaN
* `(a - 1 < a) == false` => (a-1<a) must be false  
=> The expression will return True when a = `NaN, Infinity, -Infinity`
  
**Stage 3:** `Object.is(0, a) == false && Math. abs(1/a) > 1`  
Analysis:  
* `Object.is(0, a) == false` => a={0,-0}  
* `1/a > 1` => a ∈ {0; 1} or a = -0  
=> The expression will return True when a = -0.  
  
**Stage 4:** `[] == input && ! [[]] == input`  
* `[] == ''` → true  
* `[] == 0` is also true (because '' → 0 when type-converted)  
* `[] == false` → also true (because both → 0)  

* `[[]]` is an array containing an empty array: `[[]]`  
* `[[]]` when coerced to boolean → true (because objects are always truthy)  
* `![[]]` → false  
Combine both conditions => `input=''` (You don't need to enter anything in the input box)  
  
After completing 4 stages, the flag will be returned.  
<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/63fc8409-e95d-47e4-9dab-b6e36551de6f" />  

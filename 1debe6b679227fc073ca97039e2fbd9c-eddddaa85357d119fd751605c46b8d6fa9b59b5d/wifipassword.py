import subprocess

def get_wifi_details():
    print("="*60)
    print(f"{'ชื่อ Wi-Fi (SSID)':<25} | {'ระบบความปลอดภัย':<15} | {'รหัสผ่าน (Password)'}")
    print("="*60)
    
    # ดึงรายชื่อ Wi-Fi ทั้งหมด
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
        profiles = [i.split(":")[1][1:-1] for i in data.split('\n') if "All User Profile" in i]
    except Exception as e:
        print("เกิดข้อผิดพลาดในการดึงข้อมูล:", e)
        return

    # ลูปดึงรายละเอียดทีละชื่อ
    for profile in profiles:
        try:
            # ดึงข้อมูล profile แบบเจาะลึก
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace")
            
            # หารหัสผ่าน
            password_line = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
            password = password_line[0] if password_line else "ไม่มีรหัส (เปิดสาธารณะ)"
            
            # หาประเภทความปลอดภัย (Authentication)
            auth_line = [b.split(":")[1][1:-1] for b in results.split('\n') if "Authentication" in b]
            auth_type = auth_line[0] if auth_line else "Unknown"

            # พิมพ์ผลลัพธ์ออกมา
            print(f"{profile:<25} | {auth_type:<15} | 🔑 {password}")
            
        except Exception:
            print(f"{profile:<25} | {'Error':<15} | ❌ ไม่สามารถดึงข้อมูลได้")

    print("="*60)

# สั่งรันโปรแกรม
if __name__ == "__main__":
    get_wifi_details()
    input("\nกด Enter เพื่อปิดหน้าต่าง...")
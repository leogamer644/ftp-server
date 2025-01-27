import ftplib
from colorama import Fore, Style
import os

# Colors variables
green = Fore.GREEN
reset = Style.RESET_ALL

def test_anonymous_access(server_ip):
    try:
        ftp = ftplib.FTP()
        ftp.connect(server_ip, 21)
        ftp.login()  # Login as anonymous
        print(f'{green}[*] Anonymous login successful.{reset}')
        
        # List directory contents
        ftp.retrlines('LIST')
        print("Directory listing successful.")
        
        # Try to upload a file (should fail)
        try:
            with open('testfile.txt', 'w') as f:
                f.write('This is a test file.')
            with open('testfile.txt', 'rb') as f:
                ftp.storlines('STOR testfile.txt', f)
            print("Error: Anonymous user should not be able to upload files.")
        except ftplib.error_perm:
            print("Anonymous upload not allowed as expected.")
        
        ftp.quit()
    except Exception as e:
        print(f"Error during anonymous access test: {e}")
    finally:
        if os.path.exists('testfile.txt'):
            os.remove('testfile.txt')

def test_user_access(server_ip, username, password, chrooted):
    try:
        ftp = ftplib.FTP_TLS(LOCAL_USERS_SERVER_IP)
        ftp.login(username, password)
        ftp.prot_p()
        print(f"{green}[*] Login successful for user {username}.{reset}")
        
        # List directory contents
        ftp.retrlines('LIST')
        print("Directory listing successful.")
        
        # Upload a file
        with open('testfile.txt', 'w') as f:
            f.write('This is a test file.')
        with open('testfile.txt', 'rb') as f:
            ftp.storlines('STOR testfile.txt', f)
        print("File upload successful.")
        
        # Download the file
        with open('downloaded_testfile.txt', 'wb') as f:
            ftp.retrbinary('RETR testfile.txt', f.write)
        print("File download successful.")
        
        # Check chroot status
        ftp.cwd('..')
        if chrooted:
            print(f"{username} is chrooted as expected.")
        else:
            print(f"{username} is not chrooted as expected.")
        
        ftp.quit()
    except Exception as e:
        print(f"Error during user access test for {username}: {e}")
    finally:
        if os.path.exists('testfile.txt'):
            os.remove('testfile.txt')
        if os.path.exists('downloaded_testfile.txt'):
            os.remove('downloaded_testfile.txt')

# Configuración del servidor FTP
SERVER_IP = 'your.ftp.server.ip'
ANONYMOUS_SERVER_IP = '192.168.57.20'  # IP del servidor FTP anónimo
LOCAL_USERS_SERVER_IP = '192.168.57.30'  # IP del servidor FTP de usuarios locales

# Pruebas para acceso anónimo
print("Testing anonymous FTP access...")
test_anonymous_access(ANONYMOUS_SERVER_IP)

# Pruebas para acceso de usuarios locales
print("Testing local user FTP access...")
test_user_access(LOCAL_USERS_SERVER_IP, 'charles', '1234', chrooted=True)
test_user_access(LOCAL_USERS_SERVER_IP, 'laura', '1234', chrooted=False)
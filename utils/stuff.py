import io
import os
import re
import sys
import time
import yaml
import datetime
import requests
import user_agent
from pystyle import *
import concurrent.futures
import utils.human_nuke as human_nuke
import utils.interface as interface

def get_theme():
    with open('color.txt', 'r') as f:
        colord = f.read().lower()
    colorx = getattr(Colors, colord)
    return colorx

def get_info():
    try:
        with open('config.yml', 'r') as f:
            config = yaml.safe_load(f)
        try:
            return config['discord']['token']
        except:
            # tell them their shi invalid and recreate it for them
            clear()
            vanguard_print("!", "Invalid config, recreating...\n")
            time.sleep(3)
            data = {'discord': {'token': 'real'}}
            with open('config.yml', 'w') as file:
                yaml.dump(data, file)
            vanguard_print("!", "Recreated config, please fill it out.")
            input("\n")
            sys.exit()
    except FileNotFoundError:
        clear()
        vanguard_print("!", "Config not found, creating...\n")
        time.sleep(3)
        data = {'discord': {'token': 'real'}}
        with open('config.yml', 'w') as file:
            yaml.dump(data, file)
        vanguard_print("!", "Created config, please fill it out.")
        input("\n")
        sys.exit()

def validate_token(token):
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if r.status_code == 200:
        return True
    else:
        return False

def proxy():
    temp = "data\\proxies.txt"
    #if the file size is empty
    if os.stat(temp).st_size == 0:
        return
    proxies = open(temp).read().split('\n')
    proxy = proxies[0]

    with open(temp, 'r+') as fp:
        #read all lines
        lines = fp.readlines()
        #get the first line
        fp.seek(0)
        #remove the proxy
        fp.truncate()
        fp.writelines(lines[1:])
    return ({'http://': f'http://{proxy}', 'https://': f'https://{proxy}'})

def get_username(token):
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if r.status_code == 200:
        return f"{r.json()['username']}#{r.json()['discriminator']}"
    else:
        return False

def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n'*120)
    return

def vanguard_print(symbol, text):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    Write.Print("[", color=get_theme(), interval=0.00), Write.Print(time, color=Colors.reset, interval=0.00), Write.Print("]", color=get_theme(), interval=0.00), Write.Print("(", color=get_theme(), interval=0.00), Write.Print(symbol, color=Colors.reset, interval=0.00), Write.Print(")", color=get_theme(), interval=0.00), Write.Print(" ", color=get_theme(), interval=0.00), Write.Print(text, color=Colors.reset, interval=0.00)

def choice_handler(choice):
    choices = ['na', 'df', 'ds', 'da', 'dc', 'ls', 'ss', 'dd', 'md', 'fm', 'gi', 'pc', 'mr', 'ws', 'cfn', 'vc', 'ct', 'help', 'exit']
    if choice in choices:
        return True
    else:
        return False

def choice_executor(choice):
    token = get_info()
    success_codes = [200, 204, 201, 202]
    if choice == "help":
        interface.menu()
    elif choice == "df":
        vanguard_print("#", "Starting to delete friends...")
        print("\n")
        human_nuke.delete_friends(token)
    elif choice == "ds":
        vanguard_print("#", "Starting to delete servers...")
        print("\n")
        human_nuke.delete_guilds(token)
    elif choice == "ls":
        vanguard_print("#", "Starting to leave servers...")
        print("\n")
        human_nuke.leave_guilds(token)
    elif choice == "ss":
        server = str(Write.Input("Name of server to spam (press enter for random): ", color=get_theme(), interval=0.00))
        icon = str(Write.Input("URL of icon to use (press enter for nothing): ", color=get_theme(), interval=0.00))
        vanguard_print("#", "Starting to spam servers...\n")
        Write.Print("Press ", color=get_theme(), interval=0.00), Write.Print("CTRL+C", color=Colors.reset, interval=0.00), Write.Print(" to stop.\n", color=get_theme(), interval=0.00)
        print("\n")
        while True:
            try:
                human_nuke.spam_guilds(token, server, icon)
            except KeyboardInterrupt:
                print("\n")
                vanguard_print("!", "Stopped spamming servers.")
                break
    elif choice == "dd":
        vanguard_print("#", "Starting to delete direct messages...")
        print("\n")
        human_nuke.delete_dms(token)
    elif choice == "md":
        choice = Write.Input("Attack friend list or dm list? (f/d): ", color=get_theme(), interval=0.00)
        if choice.lower() not in ['f', 'd']:
            vanguard_print("!", "Invalid choice.")
            time.sleep(2)
            interface.theme()
        message = str(Write.Input("Message to send: ", color=get_theme(), interval=0.00))
        if not message:
            vanguard_print("!", "Invalid message.")
            time.sleep(2)
            interface.theme()
        vanguard_print("#", "Starting to mass dm...")
        print("\n")
        human_nuke.mass_dm(token, message, choice)
    elif choice == "fm":
        vanguard_print("#", "Starting frenzy mode...")
        print("\n")
        Write.Print("Press ", color=get_theme(), interval=0.00), Write.Print("CTRL+C", color=Colors.reset, interval=0.00), Write.Print(" to stop.\n", color=get_theme(), interval=0.00)
        print("\n")
        while True:
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    executor.submit(human_nuke.frenzy_mode, token)
            except KeyboardInterrupt:
                vanguard_print("!", "Stopped frenzy mode.")
                break
    elif choice == "gi":
        vanguard_print("#", "Starting to get info...")
        print("\n")
        human_nuke.get_information(token)
    elif choice == "da":
        vanguard_print("#", "Starting to deauthorize apps...")
        print("\n")
        human_nuke.deauth_apps(token)
    elif choice == "dc":
        vanguard_print("#", "Starting to disconnect connections...")
        print("\n")
        human_nuke.disconnect_connections(token)
    elif choice == "pc":
        # show a small menu for hypesquad changer, status, bio, etc
        vanguard_print("#", "Starting to change profile...")
        print("\n")
        Write.Print("1. Bio Changer\n", color=get_theme(), interval=0.00)
        Write.Print("2. Status Changer\n", color=get_theme(), interval=0.00)
        Write.Print("3. Hypesquad Changer\n\n", color=get_theme(), interval=0.00)
        choice = Write.Input("Enter your choice: ", color=get_theme(), interval=0.00)
        print("\n")
        if choice not in ['1', '2', '3']:
            vanguard_print("!", "Invalid choice.")
            time.sleep(2)
            interface.theme()
        if choice == '1':
            human_nuke.change_bio(token)
        elif choice == '2':
            human_nuke.change_status(token)
        elif choice == '3':
            human_nuke.change_hypesquad(token)
    elif choice == "mr":
        vanguard_print("#", "Starting to mass report...")
        print("\n")
        human_nuke.mass_report(token)
    elif choice == "ws":
        vanguard_print("#", "Starting webhook spammer...")
        print("\n")
        human_nuke.webhook_spammer()
    elif choice == "cfn":
        vanguard_print("#", "Starting to change friend nicknames...")
        print("\n")
        human_nuke.friend_nickname_changer(token)
    elif choice == "vc":
        interface.credits()
    elif choice == "ct":
        interface.change_theme()
    elif choice == "exit":
        os._exit(0)
    
    time.sleep(2)
    interface.theme()
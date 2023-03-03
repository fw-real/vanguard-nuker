import os
import time
import random
import utils.stuff as stuff
from pystyle import *
from colorama import Fore

def banner():
    stuff.clear()
    banner = """
    
┬  ┬┌─┐┌┐┌┌─┐┬ ┬┌─┐┬─┐┌┬┐
└┐┌┘├─┤││││ ┬│ │├─┤├┬┘ ││
 └┘ ┴ ┴┘└┘└─┘└─┘┴ ┴┴└──┴┘
    """
    Write.Print(Center.XCenter(banner), color=stuff.get_theme(), interval=0)
    print("\n")
    Write.Print(Center.XCenter('Type "help" for a list of commands.'), color=stuff.get_theme(), interval=0)
    Write.Print(Center.XCenter('\nYou are using the discord edition of vanguard nuker.'), color=stuff.get_theme(), interval=0)
    print("\n\n")

def menu():
    comp_name = os.environ["COMPUTERNAME"]
    user_name = os.environ["USERNAME"]
    banner()
    Write.Print(Center.XCenter(Box.DoubleCube('1.  Nuke Account [na]             2.  Delete Friends [df]           3.  Delete Servers [ds]\n\n4.  Leave servers [ls]            5.  Spam Servers [ss]             6.  Delete DMs [dd]\n\n7.  Mass DM [md]                  8.  Frenzy Mode [fm]              9.  Get Information [gi]\n\n10. Deauthorize Apps [da]         11. Profile Changer [pc]          12. Disconnect Connections [dc]\n\n13. Mass Report [mr]              14. Webhook Spammer [ws]          15. Change Friend Nicknames [cfn]\n\n16. Get Friend Invite [gfi]       17. View Credits [vc]             18. Change Theme [ct]\n\n19. Exit Nuker [exit]')), color=stuff.get_theme(), interval=0)
    print("\n\n")
    choice = input(f"{Fore.LIGHTGREEN_EX}{user_name}@{comp_name}{Fore.RESET}:{Fore.LIGHTBLUE_EX}/vanguard-nuker{Fore.RESET}$ ")
    if not stuff.choice_handler(choice.lower()):
        stuff.vanguard_print('!', 'Invalid Choice.')
        time.sleep(1)
        theme()
    else:
        stuff.choice_executor(choice.lower())
    

def theme():
    comp_name = os.environ["COMPUTERNAME"]
    user_name = os.environ["USERNAME"]
    banner()
    choice = input(f"{Fore.LIGHTGREEN_EX}{user_name}@{comp_name}{Fore.RESET}:{Fore.LIGHTBLUE_EX}/vanguard-nuker{Fore.RESET}$ ")
    if not stuff.choice_handler(choice.lower()):
        stuff.vanguard_print('!', 'Invalid Choice.')
        time.sleep(1)
        theme()
    else:
        stuff.choice_executor(choice.lower())

def credits():
    comp_name = os.environ["COMPUTERNAME"]
    user_name = os.environ["USERNAME"]
    banner()
    Write.Print(Box.Lines('Vanguard Nuker is created by "nostorian"'), color=stuff.get_theme(), interval=0)
    Write.Print(Center.XCenter(Box.DoubleCube('1. My Discord [mdc]       2. My Github [mg]\n\n3. My Telegram [mt]       4. My PayPal [mp]\n\n5. Go Back [gb]           6. Exit Nuker [en]')), color=stuff.get_theme(), interval=0)
    print("\n\n")
    choice = input(f"{Fore.LIGHTGREEN_EX}{user_name}@{comp_name}{Fore.RESET}:{Fore.LIGHTBLUE_EX}/vanguard-nuker{Fore.RESET}$ ")
    credits_choices = ['mdc', 'mg', 'mt', 'mp', 'gb', 'en']
    if not stuff.choice_handler(choice.lower()) and choice.lower() not in credits_choices:
        stuff.vanguard_print('!', 'Invalid Choice.')
        time.sleep(1)
        credits()
    if stuff.choice_handler(choice.lower()):
        stuff.choice_executor(choice.lower())
    if choice.lower() == 'mdc':
        stuff.vanguard_print('#', 'My Discord: nostorian#9339')
        time.sleep(8)
        credits()
    elif choice.lower() == 'mg':
        stuff.vanguard_print('#', 'My Github: https://github.com/nostorian')
        time.sleep(8)
        credits()
    elif choice.lower() == 'mt':
        stuff.vanguard_print('#', 'My Telegram: https://t.me/nostorian\n')
        stuff.vanguard_print('!', "If t.me link doesn't work, my username is @nostorian")
        time.sleep(8)
        credits()
    elif choice.lower() == 'mp':
        stuff.vanguard_print('#', 'My Paypal: https://paypal.me/nostorian')
        time.sleep(8)
        credits()
    elif choice.lower() == 'gb':
        theme()
    elif choice.lower() == 'en':
        os._exit(1)

def change_theme():
    comp_name = os.environ["COMPUTERNAME"]
    user_name = os.environ["USERNAME"]
    banner()
    Write.Print(Center.XCenter(Box.DoubleCube('1. Default [d]        2. Custom [c]\n3. Random [r]         4. Back [b]')), color=stuff.get_theme(), interval=0)
    print("\n\n")
    choice = input(f"{Fore.LIGHTGREEN_EX}{user_name}@{comp_name}{Fore.RESET}:{Fore.LIGHTBLUE_EX}/vanguard-nuker{Fore.RESET}$ ")
    theme_choices = ['d', 'c', 'r', 'b']
    if not stuff.choice_handler(choice.lower()) and choice not in theme_choices:
        stuff.vanguard_print('!', 'Invalid Choice.')
        time.sleep(1)
        change_theme()
    if stuff.choice_handler(choice.lower()):
        stuff.choice_executor(choice.lower())
    if choice.lower() == 'd':
        with open("color.txt", "w") as f:
            f.write("cyan")
        time.sleep(1)
        change_theme()
    elif choice.lower() == 'c':
        stuff.clear()
        banner()
        # colors = [red, green, blue, white, black, gray, yellow, purple, cyan, orange, pink, turquoise, light_gray, dark_gray, light_red, light_green, light_blue, dark_red, dark_green, dark_blue] in rows of 4
        Write.Print(Center.XCenter(Box.DoubleCube('1.  Red [r]             2.  Green [g]             3.  Blue [b]             4.  White [w]\n\n5.  Black [k]           6.  Gray [y]              7.  Yellow [o]           8.  Purple [p]\n\n9.  Turquoise [t]       10. Orange [a]            11. Pink [i]             12. Light Gray [l]\n\n13. Dark Gray [d]       14. Light Red [e]         15. Light Green [f]      16. Light Blue [h]\n\n17. Dark Red [j]        18. Dark Green [m]        19. Dark Blue [n]        20. Go Back [gb]')), color=stuff.get_theme(), interval=0)
        print("\n\n")
        choice = input(f"{Fore.LIGHTGREEN_EX}{user_name}@{comp_name}{Fore.RESET}:{Fore.LIGHTBLUE_EX}/vanguard-nuker{Fore.RESET}$ ")
        color_choices = {'r': 'red', 'g': 'green', 'b': 'blue', 'w': 'white', 'k': 'black', 'y': 'gray', 'o': 'yellow', 'p': 'purple', 'a': 'orange', 'i': 'pink', 't': 'turquoise', 'l': 'light_gray', 'd': 'dark_gray', 'e': 'light_red', 'f': 'light_green', 'h': 'light_blue', 'j': 'dark_red', 'm': 'dark_green', 'n': 'dark_blue', 'gb': 'gb'}
        if choice not in color_choices:
            stuff.vanguard_print('!', 'Invalid Choice.')
            time.sleep(1)
            change_theme()
        if choice != "gb":
            with open("color.txt", "w") as f:
                f.write(color_choices[choice])
            stuff.vanguard_print('#', f"Theme set to {color_choices[choice]}.")
            time.sleep(1)
            change_theme()
        else:
            change_theme()
    elif choice.lower() == 'r':
        color_choices = {'r': 'red', 'g': 'green', 'b': 'blue', 'w': 'white', 'k': 'black', 'y': 'gray', 'o': 'yellow', 'p': 'purple', 'c': 'cyan', 'a': 'orange', 'i': 'pink', 't': 'turquoise', 'l': 'light_gray', 'd': 'dark_gray', 'e': 'light_red', 'f': 'light_green', 'h': 'light_blue', 'j': 'dark_red', 'm': 'dark_green', 'n': 'dark_blue', 'gb': 'gb'}
        color = random.choice(list(color_choices.values()))
        with open("color.txt", "w") as f:
            f.write(color)
        stuff.vanguard_print('#', f"Theme set to {color}.")
        time.sleep(1)
        change_theme()
    elif choice.lower() == 'b':
        theme()
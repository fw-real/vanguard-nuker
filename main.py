import os
import time
import sys
import ctypes
from pystyle import *
import utils.stuff as stuff
import utils.interface as interface


ctypes.windll.kernel32.SetConsoleTitleW('Vanguard Nuker | Discord Edition')


def main():
    stuff.clear()
    Write.Print(Center.XCenter("""

 ▌ ▐· ▄▄▄·  ▐ ▄  ▄▄ • ▄• ▄▌ ▄▄▄· ▄▄▄  ·▄▄▄▄       ▐ ▄ ▄• ▄▌▄ •▄ ▄▄▄ .▄▄▄  
▪█·█▌▐█ ▀█ •█▌▐█▐█ ▀ ▪█▪██▌▐█ ▀█ ▀▄ █·██▪ ██     •█▌▐██▪██▌█▌▄▌▪▀▄.▀·▀▄ █·
▐█▐█•▄█▀▀█ ▐█▐▐▌▄█ ▀█▄█▌▐█▌▄█▀▀█ ▐▀▀▄ ▐█· ▐█▌    ▐█▐▐▌█▌▐█▌▐▀▀▄·▐▀▀▪▄▐▀▀▄ 
 ███ ▐█ ▪▐▌██▐█▌▐█▄▪▐█▐█▄█▌▐█ ▪▐▌▐█•█▌██. ██     ██▐█▌▐█▄█▌▐█.█▌▐█▄▄▌▐█•█▌
. ▀   ▀  ▀ ▀▀ █▪·▀▀▀▀  ▀▀▀  ▀  ▀ .▀  ▀▀▀▀▀▀•     ▀▀ █▪ ▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀

    """), color=stuff.get_theme(), interval=0)
    # check if proxies.txt is empty
    if os.stat("data\\proxies.txt").st_size == 0:
        Write.Print(Center.XCenter('\n\nHang tight while we load the program...'), color=stuff.get_theme(), interval=0)
        Write.Print(Center.XCenter('\nProxies are not found, ratelimits may occur.'), color=stuff.get_theme(), interval=0)
    else:
        Write.Print(Center.XCenter('\n\nHang tight while we load the program...'), color=stuff.get_theme(), interval=0)
    time.sleep(5)
    token = stuff.get_info()
    stuff.clear()
    if not stuff.validate_token(token):
        stuff.clear()
        stuff.vanguard_print('!', 'Invalid Credentials.')
        input("\n")
        sys.exit()
    else:
        real = stuff.get_username(token)
        if not real:
            pass
        else:
            ctypes.windll.kernel32.SetConsoleTitleW(f'Vanguard Nuker | {real}')
        interface.theme()

if __name__ == '__main__':
    main()
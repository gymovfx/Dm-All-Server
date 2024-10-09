# Script made by _gymo
# https://github.com/gymovfx
# https://github.com/gymovfx/Dm-All-Server

import os
import shutil
import webbrowser
import requests
import time
import datetime

ROUGE = '\033[31m'
VERT = '\033[32m'
RESET = '\033[0m'

ascii_art = '''
                    ▄████▓██   ██▓ ███▄ ▄███▓ ▒█████     ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
                   ██▒ ▀█▒▒██  ██▒▓██▒▀█▀ ██▒▒██▒  ██▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
                  ▒██░▄▄▄░ ▒██ ██░▓██    ▓██░▒██░  ██▒   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
                  ░▓█  ██▓ ░ ▐██▓░▒██    ▒██ ▒██   ██░   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
                  ░▒▓███▀▒ ░ ██▒▓░▒██▒   ░██▒░ ████▓▒░     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
                   ░▒   ▒   ██▒▒▒ ░ ▒░   ░  ░░ ▒░▒░▒░      ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
                    ░   ░ ▓██ ░▒░ ░  ░      ░  ░ ▒ ▒░        ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
                  ░ ░   ░ ▒ ▒ ░░  ░      ░   ░ ░ ░ ▒       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
                        ░ ░ ░            ░       ░ ░                  ░ ░      ░ ░      ░  ░      ░  
                          ░ ░
'''

def centrer_texte(texte):
    terminal_size = shutil.get_terminal_size()
    texte_lines = texte.splitlines()
    centered_texte = '\n'.join(line.center(terminal_size.columns) for line in texte_lines)
    return centered_texte

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_menu():
    menu = f'''



                 [{ROUGE}01{RESET}]{ROUGE} ->{RESET} Dm-All
                 [{ROUGE}02{RESET}]{ROUGE} ->{RESET} Credits
    '''
    print(centrer_texte(menu))

def credits_visites():
    return os.path.exists('credits_visited.txt')

def marquer_credits_visites():
    with open('credits_visited.txt', 'w') as f:
        f.write('1')

def verifier_token(token, proxies=None):
    headers = {
        'Authorization': f'Bot {token}'
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers, proxies=proxies)
    return response.status_code == 200

def verifier_bot_dans_guild(token, guild_id, proxies=None):
    headers = {
        'Authorization': f'Bot {token}'
    }
    response = requests.get('https://discord.com/api/v10/users/@me/guilds', headers=headers, proxies=proxies)
    
    if response.status_code == 200:
        guilds = response.json()
        guild_id_str = str(guild_id)  
        
        for guild in guilds:
            if guild['id'] == guild_id_str:
                return True
    else:
        print(f"Erreur de réponse: {response.status_code} - {response.text}")
        
    return False


def obtenir_heure_actuelle():
    now = datetime.datetime.now()
    return f"{ROUGE}[{RESET}{now.strftime('%H:%M:%S')}{ROUGE}]{RESET}"


def formater_token(token):
    if len(token) > 38:
        return f"{token[:38]}****"
    else:
        return token


def obtenir_membres_guilde(token, guild_id, proxies=None):
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
    }
    
    membres = []
    after = None
    
    while True:
        params = {'limit': 1000}  
        if after:
            params['after'] = after
        
        response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/members', headers=headers, params=params, proxies=proxies)
        
        if response.status_code == 200:
            data = response.json()
            membres.extend(data)
            if len(data) < 1000:  
                break
            after = data[-1]['user']['id']  
        else:
            print(f"Erreur de réponse: {response.status_code} - {response.text}")
            break
    
    return membres


def envoyer_dm(token, user_id, message, ping, proxies=None):
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'recipient_id': user_id
    }
    

    response = requests.post(f'https://discord.com/api/v10/users/@me/channels', headers=headers, json=payload, proxies=proxies)
    
    if response.status_code == 200:
        channel_id = response.json()['id']
        if ping:
            
            payload_message = {
                'content': f"{message} <@{user_id}>"
            }
        else:
            payload_message = {
                'content': message
            }
        response_message = requests.post(f'https://discord.com/api/v10/channels/{channel_id}/messages', headers=headers, json=payload_message, proxies=proxies)
        return response_message.status_code
    return None


def lire_proxies(fichier='proxy.txt'):
    proxies = []
    if os.path.exists(fichier):
        with open(fichier, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(f"http://{proxy}")
    return proxies

def main():
    visite_credits = credits_visites()
    proxies_list = lire_proxies()  
    proxy_index = 0
    
    while True:
        clear_screen()
        centered_art = centrer_texte(ascii_art)
        print(f"{ROUGE}{centered_art}{RESET}")
        
        afficher_menu()
        
        choix = input("\nChoise : ")
        
        if choix == "01":
            while True:
             
                clear_screen()
                centered_art = centrer_texte(ascii_art)
                print(f"{ROUGE}{centered_art}{RESET}")
                
           
                token = input(f"\n[{ROUGE}+{RESET}]{ROUGE} ->{RESET} Token Bot : ")
                
                proxies = {'http': proxies_list[proxy_index]} if proxies_list else None  
                
                if verifier_token(token, proxies):
               
                    token_affiche = formater_token(token)
                    heure_actuelle = obtenir_heure_actuelle()  
                    print(f"\n{heure_actuelle} [{VERT}VALID{RESET}] Token{VERT} -> {RESET}{token_affiche}")
                    time.sleep(2)
                    clear_screen()
                    centered_art = centrer_texte(ascii_art)
                    print(f"{ROUGE}{centered_art}{RESET}")
                    
                    while True:
                  
                        guild_id = input(f"\n[{ROUGE}+{RESET}]{ROUGE} ->{RESET} Guild ID : ")
                        
                        guild_id_int = int(guild_id)  
                        
                        if verifier_bot_dans_guild(token, guild_id_int, proxies):
                            print(f"\n{obtenir_heure_actuelle()} [{VERT}VALID{RESET}] Guild ID {VERT} -> {RESET}{guild_id}")
                            time.sleep(2)
                            clear_screen()
                            centered_art = centrer_texte(ascii_art)
                            print(f"{ROUGE}{centered_art}{RESET}")
                            
                        
                            message = input(f"\n[{ROUGE}+{RESET}]{ROUGE} ->{RESET} Message à envoyer : ")
                            time.sleep(2)
                            clear_screen()
                            centered_art = centrer_texte(ascii_art)
                            print(f"{ROUGE}{centered_art}{RESET}")
                            
                        
                            ping_reponse = input(f"\n[{ROUGE}+{RESET}]{ROUGE} ->{RESET} Voulez-vous ping la personne ? : ")
                            ping = ping_reponse.lower() == 'y'  
                            time.sleep(2)
                            clear_screen()
                            centered_art = centrer_texte(ascii_art)
                            print(f"{ROUGE}{centered_art}{RESET}")
                            
                      
                            cooldown = int(input(f"\n[{ROUGE}+{RESET}]{ROUGE} ->{RESET} Cooldown : "))
                            
                         
                            clear_screen()
                            centered_art = centrer_texte(ascii_art)
                            print(f"{ROUGE}{centered_art}{RESET}")
                            
                           
                            membres = obtenir_membres_guilde(token, guild_id_int, proxies)
                            for membre in membres:
                                user_id = membre['user']['id']
                                status_code = envoyer_dm(token, user_id, message, ping, proxies)
                                
                                if status_code == 200:
                                    print(f"{obtenir_heure_actuelle()} [{VERT}SUCCESS{RESET}]  {ROUGE}->{RESET} Sent {message} to User ID {user_id} {VERT}[200]{RESET}")
                                else:
                                    print(f"{obtenir_heure_actuelle()} [{ROUGE}ERROR{RESET}]  {ROUGE}->{RESET} Failed to send DM to User ID {user_id} {ROUGE}[403]{RESET}")
                                
                                time.sleep(cooldown) 
                                
                               
                                proxy_index = (proxy_index + 1) % len(proxies_list) if proxies_list else 0
                        
                            print(f"\nTous les messages ont été envoyés.")
                            break  
                        
                        else:
                            print(f"\n{obtenir_heure_actuelle()} [{ROUGE}INVALID{RESET}] Guild ID {ROUGE} -> {RESET}{guild_id}")
                        
                        time.sleep(2)  
                        clear_screen()  
                        
                        
                        centered_art = centrer_texte(ascii_art)
                        print(f"{ROUGE}{centered_art}{RESET}")
                        afficher_menu()
                        break 
                    
                else:
                  
                    heure_actuelle = obtenir_heure_actuelle() 
                    token_affiche = formater_token(token)  
                    print(f"\n{heure_actuelle} [{ROUGE}INVALID{RESET}] Token{ROUGE} -> {RESET}{token_affiche}")
                    time.sleep(2)  
                    clear_screen()  
                    
                    
                    centered_art = centrer_texte(ascii_art)
                    print(f"{ROUGE}{centered_art}{RESET}")
                    afficher_menu()
                    
        elif choix == "02":
            if not visite_credits:
                webbrowser.open("https://github.com/gymovfx")
                marquer_credits_visites()  
                visite_credits = True  
                
        else:
            print("\nOption invalide. Veuillez réessayer.")
            input("\nAppuyez sur une touche pour réessayer...")

if __name__ == "__main__":
    main()

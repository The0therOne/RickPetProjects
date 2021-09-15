import requests
from bs4 import BeautifulSoup
import webbrowser
import os

INTERACTIVE_MAP_URL = 'https://genshin-impact-map.appsample.com/#/'
URL = 'https://www.pockettactics.com/genshin-impact/codes'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.159 Safari/537.36',
           'accept': '*/*',
           }


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html, codes='a'):
    soup = BeautifulSoup(html, 'html.parser')
    active_codes = soup.find('h2', string='Genshin Impact codes').find_next_sibling('ul').find_all('li')
    expired_codes = soup.find('p', string='Expired Genshin Impact codes:').find_next_sibling('ul').find_all('li')

    promocodes = []

    if codes == 'a':
        for item in active_codes:
            splitted_item = item.text.replace(u'\xa0', u' ').split(' ', maxsplit=2)

            promocodes.append({
                'promocode': splitted_item[0],
                'reward': splitted_item[2],
            })
    elif codes == 'e':
        for item in expired_codes:
            splitted_item = item.text.replace(u'\xa0', u' ').split(' ', maxsplit=2)

            promocodes.append({
                'promocode': splitted_item[0],
                'reward': splitted_item[2],
            })
    else:
        print('[-]Something wrong! Check you answer! A (for active) or E (for expired)')

    return promocodes


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        what_parse = input('[?]Active or Expired codes? (A/E): ')

        promocodes = get_content(html.text, what_parse.lower())
        for promocode in promocodes:
            print('--------------------------------------------------------------')
            print(f"PROMOCODE: {promocode['promocode']}\nREWARD: {promocode['reward']}")
    else:
        print('[-]Error!')


def show_builds():
    char_builds = {
        "1": ['Albedo', 'https://genshin.gg/characters/Albedo'],
        "2": ['Amber', 'https://genshin.gg/characters/Amber'],
        "3": ['Barbara', 'https://genshin.gg/characters/Barbara'],
        "4": ['Beidou', 'https://genshin.gg/characters/Beidou'],
        "5": ['Bennett', 'https://genshin.gg/characters/Bennett'],
        "6": ['Chongyun', 'https://genshin.gg/characters/Chongyun'],
        "7": ['Diluc', 'https://genshin.gg/characters/Diluc'],
        "8": ['Diona', 'https://genshin.gg/characters/Diona'],
        "9": ['Eula', 'https://genshin.gg/characters/Eula'],
        "10": ['Fischl', 'https://genshin.gg/characters/Fischl'],
        "11": ['Ganyu', 'https://genshin.gg/characters/Ganyu'],
        "12": ['Hu Tao', 'https://genshin.gg/characters/HuTao'],
        "13": ['Jean', 'https://genshin.gg/characters/Jean'],
        "14": ['Kazuha', 'https://genshin.gg/characters/Kazuha'],
        "15": ['Kaeya', 'https://genshin.gg/characters/Kaeya'],
        "16": ['Ayaka', 'https://genshin.gg/characters/Ayaka'],
        "17": ['Keqing', 'https://genshin.gg/characters/Keqing'],
        "18": ['Klee', 'https://genshin.gg/characters/Klee'],
        "19": ['Lisa', 'https://genshin.gg/characters/Lisa'],
        "20": ['Mona', 'https://genshin.gg/characters/Mona'],
        "21": ['Ningguang', 'https://genshin.gg/characters/Ningguang'],
        "22": ['Noelle', 'https://genshin.gg/characters/Noelle'],
        "23": ['Qiqi', 'https://genshin.gg/characters/Qiqi'],
        "24": ['Razor', 'https://genshin.gg/characters/Razor'],
        "25": ['Rosaria', 'https://genshin.gg/characters/Rosaria'],
        "26": ['Sayu', 'https://genshin.gg/characters/Sayu'],
        "27": ['Sucrose', 'https://genshin.gg/characters/Sucrose'],
        "28": ['Tartaglia', 'https://genshin.gg/characters/Tartaglia'],
        "29": ['Traveler(Anemo)', 'https://genshin.gg/characters/Traveler(Anemo)'],
        "30": ['Traveler(Electro)', 'https://genshin.gg/characters/Traveler(Electro)'],
        "31": ['Traveler(Geo)', 'https://genshin.gg/characters/Traveler(Geo)'],
        "32": ['Venti', 'https://genshin.gg/characters/Venti'],
        "33": ['Xiangling', 'https://genshin.gg/characters/Xiangling'],
        "34": ['Xiao', 'https://genshin.gg/characters/Xiao'],
        "35": ['Xingqiu', 'https://genshin.gg/characters/Xingqiu'],
        "36": ['Xinyan', 'https://genshin.gg/characters/Xinyan'],
        "37": ['Yanfei', 'https://genshin.gg/characters/Yanfei'],
        "38": ['Yoimiya', 'https://genshin.gg/characters/Yoimiya'],
        "39": ['Zhongli', 'https://genshin.gg/characters/Zhongli'],
    }

    options = char_builds.keys()
    while True:
        count = 1
        for entry in options:
            print(f"{entry}) {char_builds[entry][0]}")
            count += 1
        print("Type 'quit' for exit!")

        choose = input("Character: ")
        if choose in options:
            os.system('cls')
            webbrowser.open(char_builds[choose][1])
        elif choose == 'quit':
            os.system('cls')
            break
        else:
            print("[-]Wrong name! Try again!")
            os.system('cls')
            continue


def how_to_redeem():
    print("""\t    1) Reach Adventure Level 10
            2) Log into your account on the official website
            3) Go to the Redeem Codes section
            4) Select your regional server
            5) Enter your character's name
            6) Enter the promocode
            7) Your reward will await you in-game\n""")
    input('[!]Press ENTER to continue...')


# def show_culus_map():
#     culus_map = {
#         "1": ["Mondstadt (Anemo)", ""],
#         "2": ["Liyue (Geo)", ""],
#         "3": ["Inazuma (Electro)", ""],
#         "4": ["Dragonspine (Crimson Agate)", "https://static.gosunoob.com/img/1/2020/12/Crimson-Agate-map-location-genshin-impact-1024x808.jpg"],
#     }
#     choose_loc = input("Which region?\nMondstadt")


def main_menu():
    menu = {
        "1": "Show promocodes",
        "2": "Open website with codes",
        "3": "How to redeem codes?",
        "4": "Show builds",
        "5": "Open interactive map",
        "6": "Quit",
    }
    options = menu.keys()

    while True:
        print("""-----------------------------------------------
        Genshin Multitool by Ricrawl
-----------------------------------------------""")

        for entry in options:
            print(f"{entry}) {menu[entry]}")

        choose = input("Option: ")

        if choose == '1':
            os.system('cls')
            parse()
            input('\n[!]Press ENTER to continue...')
            continue
        elif choose == '2':
            webbrowser.open(URL)
            os.system('cls')
            input('[!]Press ENTER to continue...')
            os.system('cls')
            continue
        elif choose == '3':
            how_to_redeem()
            os.system('cls')
            continue
        elif choose == '4':
            os.system('cls')
            show_builds()
            continue
        elif choose == '5':
            webbrowser.open(INTERACTIVE_MAP_URL)
            os.system('cls')
            input('[!]Press ENTER to continue...')
            os.system('cls')
        elif choose == '6':
            break
        else:
            print('[-]Wrong option!')
            input('[!]Press ENTER to continue...')
            os.system('cls')
            continue


if __name__ == '__main__':
    main_menu()

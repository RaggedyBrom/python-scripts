import sys
import requests
import bs4
import subprocess

systems = ['dnd_next',
           'wod',
           'barbariansoflemuria',
           'cthulhu',
           'l5r',
           'ryuutama',
           'savageworlds',
           'dungeonworld',
           'bladesinthedark',
           'sotdl',
           'warhammer'
           ]

def ribbon_finder(system):

    ribbon_listings = []
    page_num = 0
    url_front = 'https://app.roll20.net/lfg/search//?page='
    url_back = ('&days=&dayhours=&frequency=&timeofday=&timeofday_seconds=&langua'
               'ge=English&avpref=voiceonly&gametype=Any&newplayer=true&yesmatur'
               'econtent=true&nopaytoplay=true&playingstructured=' + system +
               '&sortby=relevance&for_event=&roll20con=')
    
    while page_num < 10 and len(ribbon_listings) < 30:
    
        # import and parse the current page
        print('Parsing page ' + str(page_num))  
        url = url_front + str(page_num) + url_back
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        listings = soup.select('.lfglisting')

        # iterate over the listings on the page
        for i in range(len(listings)):
            if 'ribbon_purple' in str(listings[i]) and len(ribbon_listings) < 30:
                print('Found a ribbon!')
                link_tag = listings[i].select('.thumb a')
                link = 'https://app.roll20.net' + link_tag[0].get('href')
                ribbon_listings.append(link)

        page_num += 1

    # open all the listings with ribbons that were found
    print('Opening links...')
    for link in ribbon_listings:
        subprocess.call([r'C:\Program Files\Mozilla Firefox\Firefox.exe',
        '-new-tab', link])
    
    print('Done. Found ' + str(len(ribbon_listings)) + ' listing(s).\n')

# Main program loop
while True:
    for index, system in enumerate(systems):
        print(str(index).ljust(3 - len(str(index))) + ' -  ' + system)
    choice = input('\nEnter the index of your chosen system,\n'
                   'enter "all" to parse all systems EXCEPT D&D 5e,\n'
                   'or press "q" to exit: ')

    if choice == 'q':
        sys.exit()
    elif choice == 'all':
        for index in range(1, len(systems)):
            ribbon_finder(systems[index])
    else:
        try:
            index = int(choice)
            ribbon_finder(systems[index])
        except ValueError:
            continue
        except IndexError:
            continue

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
import urllib

print(""" \a
  ____  _____ ____  _  __    _ __   __   ____ ___ _   _    _    _   _  
 | __ )| ____|  _ \| |/ /   / \ \ \ / / / ___|_ _| | | |  / \  | \ | | 
 |  _ \|  _| | |_) | ' /   / _ \ \ V / | |    | || |_| | / _ \ |  \| | 
 | |_) | |___|  _ <| . \  / ___ \ | |  | |___ | ||  _  |/ ___ \| |\  | 
 |____/|_____|_| \_\_|\_\/_/   \_\ _|   \____|___|_| |_/_/   \_\_| \_| 
                                                                       
            """)




print("\n \n *** GOOGLE ARAMASINI EXCEL TABLO OLARAK KAYDEDICI ***\nbilgi:fazla denedikten sonra engelleniyorsa vpn kullanabilirsiniz.\nbilgi:'utf-8' degerler giriniz.\n")
girdi = 0
while True:
    girdi = int(input("kelime(ler) aratacaksan '1',\ngoogle url'si gireceksen '0'\n ISLEM: "))
    if (girdi == 1):
        x = list(map(str, input("Google'da aranacak keywords: ").split()))
        birlesim=""
        for i in x:
            birlesim=birlesim+str(i)+" "  
        uzunluk=int(len(birlesim))
        kwords=birlesim[:uzunluk-1]     
        query = kwords
        query = urllib.parse.quote_plus(query)
        number_result = 100  # her bir sayfada gösterilecek sonuç sayısı
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)

        break
    elif (girdi == 0):
        girdi_link = str(input("Link:"))
        google_url = girdi_link
        kwords=input('dosyanin ismi:')
        break
    else:
        print("gecersiz islem.")

ua = UserAgent()
response = requests.get(google_url, {"User-Agent": ua.random})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})

links = []
titles = []
descriptions = []
for r in result_div:
    # Her bir öğenin mevcut olup olmadığını kontrol eder, aksi takdirde istisna oluşturur
    try:
        link = r.find('a', href=True)
        title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
        description = r.find('div', attrs={'class': 's3v9rd'}).get_text()

        # Eklemeden önce her şeyin mevcut olduğundan emin olmak için kontroller
        if link != '' and title != '' and description != '':
            links.append(link['href'])
            titles.append(title)
            descriptions.append(description)
    # Bir öğe yoksa sonraki döngü
    except:
        continue
import re

to_remove = []
clean_links = []
for i, l in enumerate(links):
    clean = re.search('\/url\?q\=(.*)\&sa', l)

    # Yukarıdaki modele uymayan her şeyi kaldırır.
    if clean is None:
        to_remove.append(i)
        continue
    clean_links.append(clean.group(1))

# İlgili başlıkları ve açıklamaları kaldırır
for x in to_remove:
    del titles[x]
    del descriptions[x]

df_1 = pd.DataFrame({"BASLIK": titles[:], "LINK": clean_links[:], "ACIKLAMA": descriptions[:]})

# df_toplam=pd.concat([df_toplam,df_2],axis=0) diğer sayfaları da çekip birleştirmek için

# df_1

df_1.to_csv(str(kwords + '.csv'), index=False)

input("\nIslem Basariyla Tamamlandi!")
sys.exit(0)


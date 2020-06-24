# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 20:54:03 2018

@author: Yohan Reyes
"""

# =============================================================================
# %% Settings
# =============================================================================

scrape_ = 'PCH'

###############################################################################
#%% Libs
###############################################################################

import os
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime

###############################################################################
#%% Defs
###############################################################################

def downloadPage(path,url,verbose):
    if os.getcwd() != path:
        os.chdir(path)
        
    page = requests.get(url)
    assert str(page.status_code)[0] == '2' 
    if verbose:
        print(page)

    return page


def parserPage(soup, pr, no_pr):
    # offers = soup.find_all(class_='tileV2 regular mapView')
    offers = soup.find_all(class_='tileV2 REAdTileV2 regular mapView')
    
    offer_temp = []
    
    for offer in offers:
        
        offer_temp = []
        
        temp = offer
        price = temp.find(class_="ad-price")
        
        urgent_ = temp.find_all(class_="label-text")
        urgent = "Normal"
        for urgent__ in urgent_:
            if urgent__ != None:
                txt = urgent__.get_text()
                if txt == "Urgente":
                    urgent = "Urgente"
            else:
                 urgent = "Normal"
        
        offer_temp.append(urgent)
        contract = temp.find(class_="value make-offer")
        if contract != None:
            contract = contract.get_text()
        else:
            contract = "None"
        offer_temp.append(contract)
        
        beds = temp.find(class_="chiplets-inline-block re-bedroom")
        if beds != None:
            beds = str(beds.get_text())
        else:
            beds = "None"
        offer_temp.append(beds)
        
        baths = temp.find(class_="chiplets-inline-block re-bathroom")
        if baths != None:
            baths = str(baths.get_text())
        else:
            baths = "None"
        offer_temp.append(baths)
        
        cars = temp.find(class_="chiplets-inline-block car-parking")
        if cars != None:
            cars = str(cars.get_text())
        else:
            cars = "None"
        offer_temp.append(cars)
        
        location = temp.find(class_="tile-location one-liner")
        if location != None:
            location = location.get_text()
        else:
            location = "None"
        offer_temp.append(location)
        
        desc_more = temp.find(class_="expanded-description")
        if desc_more !=None:
            desc_more = desc_more.get_text()
            desc_more = list(desc_more)
        offer_temp.append(desc_more)
        
        link = temp.find(class_="href-link tile-title-text")
        link = str(link)
        link = link.replace('<a class="href-link tile-title-text"','')
        link = link.replace('<a class="href-link tile-title-text"','')
        link = link.replace('href=', '')
        s = link.find('/a')
        e = link.find(' target')-1
        link = link[s:e]
        offer_temp.append(link)
        
        if price != None:
            price = price.get_text()
            price = price.replace('$', '')
            price = price.replace(' ', '')
            price = price.replace(',', '')
            price = price.replace('\n', '')
            try:
                price = float(price)
            except:
                price = None
            # pr.append(price)
            offer_temp.append(price)
            
            # offers_pr.append(temp)
            desc = temp.find(class_="tile-desc one-liner")
            desc = list(desc)[0]
            desc = desc.get_text()
            offer_temp.append(desc)
            offer_temp = np.reshape(offer_temp,[1,-1])
            offer_temp = pd.DataFrame(offer_temp, columns = ['Urgent','Contract','rooms','baths','cars','location','More','link','price','more'])
            pr = pd.concat([pr,offer_temp],axis = 0, ignore_index = True)
            offer_temp = []
            
        else:
            desc = temp.find(class_="tile-desc one-liner")
            desc = list(desc)[0]
            offer_temp.append(desc)
            offer_temp = np.reshape(offer_temp,[1,-1])
            offer_temp = pd.DataFrame(offer_temp, columns = ['Urgent','Contract','rooms','baths','cars','location','More','link','more'])
            no_pr = pd.concat([no_pr,offer_temp],axis = 0, ignore_index = True)
            offer_temp = []
            
    return pr, no_pr
    
def linksParser(link_temp):
    link_temp = temp.find(class_="href-link tile-title-text")
    link_temp = str(link_temp)
    link_temp = link_temp.replace('<a class="href-link tile-title-text"','')
    link_temp = link_temp.replace('<a class="href-link tile-title-text"','')    
    link_temp = link_temp.replace('href=', '')
    s = link_temp.find('/a')
    e = link_temp.find(' target')-1
    return link_temp[s:e]


###############################################################################
#%% Page download and parse
###############################################################################



downloads_path = "D:\\Spiders\\Download"
os.chdir(downloads_path)

if scrape_ == 'PCH':
    url0 = "https://www.vivanuncios.com.mx/s-renta-inmuebles/pachuca-de-soto/v1c1098l10488p1"
    url = "https://www.vivanuncios.com.mx/s-renta-inmuebles/pachuca-de-soto/v1c1098l10488p"
#    url1 = "https://www.inmuebles24.com/casas-en-renta-en-pachuca.html"
#    url2 = "https://casas.trovit.com.mx/renta-casa-pachuca-soto"
#    url3 = "https://www.segundamano.mx/anuncios/hidalgo/pachuca-de-soto/renta-inmuebles"
#    url4 = 'https://facebook.com/login'
elif scrape_ == 'GDL':
    url0 = 'https://www.vivanuncios.com.mx/s-renta-inmuebles/guadalajara-y-zona-metro/v1c1098l10567p1'
    url = 'https://www.vivanuncios.com.mx/s-renta-inmuebles/guadalajara-y-zona-metro/v1c1098l10567p'

page = downloadPage(downloads_path,url0,True)

soup = BeautifulSoup(page.content, 'html.parser')

#%%

# print(soup.prettify())


# lst = list(soup.children)
# items = [type(item) for item in list(soup.children)]

###############################################################################
#%% Code
###############################################################################

pr = pd.DataFrame(columns = ['Urgent','Contract','rooms','baths','cars','location','More','link','price','more'])
no_pr = pd.DataFrame(columns = ['Urgent','Contract','rooms','baths','cars','location','More','link','more'])

pr = pd.DataFrame()
no_pr = pd.DataFrame()

pr, no_pr = parserPage(soup, pr, no_pr)

pagination = soup.find_all(class_="pag-box")
pagination = pagination[-1]
pagination = str(pagination)[38:97]
pagination_number = int(pagination[-2:])

for i0 in range(2,pagination_number+1):
    url_tmp = url+str(i0)
    
    page = downloadPage(downloads_path,url_tmp,True)
    soup = BeautifulSoup(page.content, 'html.parser')
    pr, no_pr = parserPage(soup, pr, no_pr)

pr["price"] = pd.to_numeric(pr["price"])
pr_ = pr.sort_values('price')
pr_ = pr_.reset_index(drop = True)

# =============================================================================
# %% Filter
# =============================================================================

pr__ = pr_.loc[pr_["price"]<10000]
pr__ = pr__.reset_index(drop = True)

pr__ = pr__.loc[pr_["price"]>1000]
pr__ = pr__.reset_index(drop = True)



###############################################################################
#%% save
###############################################################################
now = str(datetime.now())
now = now[:-7]
now = now.replace(':', '-')
if scrape_ == 'PCH':
    name = 'housesPCH' + now + '.csv'
elif scrape_ == 'GDL':
    name = 'housesGDL' + now + '.csv'

pr__.to_csv(name, index = False)



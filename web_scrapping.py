import requests
import pandas as pd
from bs4 import BeautifulSoup
r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",\
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content
soup=BeautifulSoup(c,'html.parser')
# soup.prettify()
all = soup.find_all("div",{"class":'propertyRow'})



features_el = soup.find_all("span",{"class":"featureGroup"})
# features = {None}

# for feature in features_el:
#     features.add(feature.text.replace(':\xa0',''))
l=[]
    
for item in all:
    details_dict = {}
    details_dict["price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n",'').replace(" ",'')
    details_dict["Address"]=item.find_all("span",{"class","propAddressCollapse"})[0].text
    details_dict["Locality"]=item.find_all("span",{"class","propAddressCollapse"})[0].text
    try:
        details_dict["Bed"]=item.find("span",{"class","infoBed"}).find("b").text
    except:
        details_dict["Bed"]=None
        
    try:
        details_dict["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text
    except:
        details_dict["Area"]=None
    try:
        details_dict["Full Baths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
    except:
        details_dict["Full Baths"]=None
    try:
        details_dict["Half Baths"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text
    except:
        details_dict["Half Baths"]=None
    for column_group in item.find_all("div",{"class":"columnGroup"}):
        for feature_group,feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):   
            if "Lot Size" in feature_group.text:
                details_dict["Lot Size"]=feature_name.text
            else:
                details_dict["Lot Size"]=None
                
    l.append(details_dict)    
    

    
    

df = pd.DataFrame(l)

df.to_csv("Output.csv")
f = open("Output.txt",'a')
print(df,file=f)

f.close()
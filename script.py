import csv
import codecs
import folium
import geopandas as gpd
import pandas as pd
from geopy.geocoders import Nominatim
from collections import defaultdict
import matplotlib.pyplot as plt
import contextily as ctx

path = 'Registre_d_Entitats_Esportives (1).csv'

def printOptions():
    print("1. Table with the names of provinces and the number of entities\n")
    print("2. Table with the modalities and the number of entities\n")
    print("3. Modalities of the 'COMARCA' chosen\n")
    print("4. Map of the entity that you choose\n")
    print("5. Map with the entities of a postal code\n")
    print("6. Color map of entities per 'comarca'. The TOP10 'comarcas'\n")
    print("7. Color map of entities per 'comarca'. The DOWN10 'comarcas'\n")
    print("8. Color map of entities per 'comarca'. Without BArcelonés\n")
    print("9. Color map of entities per 'comarca'.\n")
    print("10. Histograma of entities per Comarca\n")



def function1():
    file = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(file)
    b=0
    l=0
    g=0
    t=0
    for row in reader:
        cp = row['CP'] 
        if (cp[0:2] == '08'):
            b +=1
        elif (cp[0:2] == '25'):
            l +=1
        elif (cp[0:2] == '17'):
            g +=1
        elif (cp[0:2] == '43'):
            t +=1
    
    print("PROVINCES      ENTITIES")
    print("-------------------------")
    print("BARCELONA:      ",b)
    print("GIRONA:         ",g)
    print("LLEIDA:         ",l)
    print("TARRAGONA:      ",t)
    #In this case, the number of rows are the same as the  number of entities
            
    
def function2():
    file = codecs.open(path, encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(file)
    total = defaultdict(int)
    for row in reader:
        mod = row['MODALITATS']
        sep = mod.split(', ')
        for i in range(len(sep)):
            total[sep[i]] +=1 
    
    #Order  TOP DOWN
    order = defaultdict(int)
    for i in range(len(total)):
        aux = 0
        for m, cont in total.items():
            if(aux < cont and cont != 0):
                f_count = cont
                f_mod = m
                aux = cont
        order[f_mod]= f_count
        total[f_mod]=0

    for letra, cuenta in order.items():
        print(letra, cuenta)
     
def function3():
    file = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(file)
    
    print("Select one option: \n")
    print("1.Barcelona\n2.Girona\n3.Lleida\n4.Tarragona")
    option = input()
    if int(option) == 1:
        cp = '08'
    elif int(option) == 2:
        cp = '17'
    elif int(option) == 3:
        cp = '25'
    elif int(option) == 4:
        cp = '43'
    else:
        print("WRONG VALUE. THE PROGRAM ENDS")
        quit()
    
    print("Select one option: \n")
    list = []
    cont = 1
    for row in reader:
        if row['CP'][0:2] == cp:
            if(row['COMARCA'] not in list):
                list.append(row['COMARCA'])
                print(cont,". ",row['COMARCA'])
                cont += 1
    option2 = input()
    c = list[int(option2)-1] 
    
    file = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(file)
    
    total = defaultdict(int)
    for row1 in reader:
        if row1['COMARCA'] == c:
            mod = row1['MODALITATS']
            sep = mod.split(', ')
            for i in range(len(sep)):
                total[sep[i]] +=1

    for moda, valor in total.items():
        print(moda, valor)
    print("\n")

def function4():
    file = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(file)
  
    list_com = []
    cont = 1
    for row in reader:
        if(row['COMARCA'] not in list_com):
            list_com.append(row['COMARCA'])
            print(cont,". ",row['COMARCA'])
            cont += 1
    option = input()
    c = list_com[int(option)-1] 

    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)

    list_mun = []
    cont = 1
    for row in reader:
        if(row['COMARCA']==c):
            if(row['MUNICIPI'] not in list_mun):
                list_mun.append(row['MUNICIPI'])
                print(cont,". ",row['MUNICIPI'])
                cont += 1
    option2 = input()
    m = list_mun[int(option2)-1] 
    print(m)

    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)

    entidades = []
    cont = 1
    for row in reader:
        if(row['MUNICIPI']==m):
            if(row['NOM_ENTITAT'] not in entidades):
                entidades.append(row['NOM_ENTITAT'])
                print(cont,". ",row['NOM_ENTITAT'])
                cont += 1
    option2 = input()
    e = entidades[int(option2)-1] 

    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)
    
    for row in reader:
        if(row['NOM_ENTITAT']==e):
            dir = row['ADREÇA']

    #2-5-3
    l = dir.capitalize()+", "+m+", Spain"

    geo = Nominatim(user_agent="agent")
    loc = geo.geocode(l)
    mapa = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=15)
    folium.Marker([loc.latitude, loc.longitude], tooltip= l).add_to(mapa)
    mapa.save('mapa4.html') 




def function5():
    file = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(file)

    print("Enter a postal code\n")
    cp = input()

    list_dir = []
    for row in reader:
        if(row['CP']==cp):
            l = row['ADREÇA'].capitalize()+", "+row['MUNICIPI']+", Spain"
            if(l not in list_dir):
                list_dir.append(l)
    
    aux = list_dir[0]
    geo = Nominatim(user_agent="agent")
    loc_i = geo.geocode(aux)
    mapa = folium.Map(location=[loc_i.latitude, loc_i.longitude], zoom_start=14)
    
    for l in range(len(list_dir)):
        try:
            loc = geo.geocode(list_dir[l])
            folium.Marker([loc.latitude, loc.longitude], tooltip= l).add_to(mapa)
        except Exception: 
            print(Exception)
            
    #08301
    mapa.save('mapa5.html') 





def function6():
    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)
    
    comarcas = defaultdict(int)
    for row in reader:
        comarcas[row['COMARCA']] += 1
    
    top = defaultdict(int)
    for i in range(10):
        aux =0
        aux_t = defaultdict(int)
        for c, v in comarcas.items():
            if v >= aux:
                if v == aux:
                    aux_t[c]=v
                else:
                    aux = v
                    aux_t = defaultdict(int)
                    aux_t[c]=v
        for cj, vj in aux_t.items():
            comarcas[cj] = 0
            top[cj] = vj
        
    with open('TOP.csv', 'w') as file_top:
        filenames = ['NOMCOMAR', 'NUM_ENTITATS']
        write = csv.DictWriter(file_top, fieldnames=filenames)

        write.writeheader()
        for name, num in top.items():
            write.writerow({'NOMCOMAR':name, 'NUM_ENTITATS':num})
            
    file_path = 'TOP.csv'
    df = pd.read_csv(file_path)
    #we read the file
    shp_path = "./shp/divisions-administratives-v2r0-comarques-1000000-20210701.shp"
    #We use utf-8 encoding to recognize accents and special characters in the shp file such as the letters "ñ"
    sf = gpd.read_file(shp_path,encoding = 'utf-8')
    #We make a merge of the GEO DataFrame and our data source, for this to work it is important that our sources have a column in common.

    merged = pd.merge(df, sf)
    merged = gpd.GeoDataFrame(merged)
    merged = merged.to_crs(epsg=3857)

    fig, ax = plt.subplots(1, figsize=(16, 16))

    ax.axis('off')

    ax.set_title('CATALUNYA',fontdict={'fontsize': '24', 'fontweight': '3'})
                
    #We use the pandas plot function to select the column we want to plot and the formatting characteristics on the map.

    fig=merged.plot(column='NUM_ENTITATS', cmap='Set2', alpha=0.8,zorder=1,edgecolor='green',linewidth=0.1, ax = ax,legend=True)              
    ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.Mapnik)

    plt.show()


def function7():
    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)
    
    comarcas = defaultdict(int)
    for row in reader:
        comarcas[row['COMARCA']] += 1
    
    
    down = defaultdict(int)
    for i in range(10):
        aux =10000
        aux_t = defaultdict(int)
        for c, v in comarcas.items():
            if v < aux:
                aux = v
                aux_t = defaultdict(int)
                aux_t[c]=v
        for cj, vj in aux_t.items():
            comarcas[cj] = 10000
            down[cj] = vj
        
    with open('LOW.csv', 'w') as file_top:
        filenames = ['NOMCOMAR', 'NUM_ENTITATS']
        write = csv.DictWriter(file_top, fieldnames=filenames)

        write.writeheader()
        for name, num in down.items():
            write.writerow({'NOMCOMAR':name, 'NUM_ENTITATS':num})
        
    file_path = 'LOW.csv'
    df = pd.read_csv(file_path)
    shp_path = "./shp/divisions-administratives-v2r0-comarques-1000000-20210701.shp"
    sf = gpd.read_file(shp_path,encoding = 'utf-8')

    merged = pd.merge(df, sf)
    merged = gpd.GeoDataFrame(merged)
    merged = merged.to_crs(epsg=3857)

    fig, ax = plt.subplots(1, figsize=(16, 16))

    ax.axis('off')

    ax.set_title('CATALUNYA',fontdict={'fontsize': '24', 'fontweight': '3'})

    fig=merged.plot(column='NUM_ENTITATS', cmap='Set2', alpha=0.8,zorder=1,edgecolor='green',linewidth=0.1, ax = ax,legend=True)              
    ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.Mapnik)
    plt.show()



def function8():
    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)

    comarcas = defaultdict(int)
    for row in reader:
        if(row['COMARCA']!='Barcelonès'):
            comarcas[row['COMARCA']] += 1
    
    with open('NOBAR.csv', 'w') as file_top:
        filenames = ['NOMCOMAR', 'NUM_ENTITATS']
        write = csv.DictWriter(file_top, fieldnames=filenames)

        write.writeheader()
        for name, num in comarcas.items():
            write.writerow({'NOMCOMAR':name, 'NUM_ENTITATS':num})
    
    file_path = 'NOBAR.csv'
    df = pd.read_csv(file_path)
    shp_path = "./shp/divisions-administratives-v2r0-comarques-1000000-20210701.shp"
    sf = gpd.read_file(shp_path,encoding = 'utf-8')

    merged = pd.merge(df, sf)
    merged = gpd.GeoDataFrame(merged)
    merged = merged.to_crs(epsg=3857)

    fig, ax = plt.subplots(1, figsize=(16, 16))

    ax.axis('off')

    ax.set_title('CATALUNYA',fontdict={'fontsize': '24', 'fontweight': '3'})

    fig=merged.plot(column='NUM_ENTITATS', cmap='plasma_r', alpha=0.8,zorder=1,edgecolor='green',linewidth=0.1, ax = ax,legend=True)              
    ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.Mapnik)

    plt.show()

    
def function9():
    read = codecs.open(path, 'r', encoding='utf-8', errors='backslashreplace')
    reader = csv.DictReader(read)
    
    comarcas = defaultdict(int)
    for row in reader:
        comarcas[row['COMARCA']] += 1
    
        
    with open('ALL.csv', 'w') as file_top:
        filenames = ['NOMCOMAR', 'NUM_ENTITATS']
        write = csv.DictWriter(file_top, fieldnames=filenames)

        write.writeheader()
        for name, num in comarcas.items():
            write.writerow({'NOMCOMAR':name, 'NUM_ENTITATS':num})
        
    file_path = 'ALL.csv'
    df = pd.read_csv(file_path)
    shp_path = "./shp/divisions-administratives-v2r0-comarques-1000000-20210701.shp"
    sf = gpd.read_file(shp_path,encoding = 'utf-8')

    merged = pd.merge(df, sf)
    merged = gpd.GeoDataFrame(merged)
    merged = merged.to_crs(epsg=3857)

    fig, ax = plt.subplots(1, figsize=(16, 16))

    ax.axis('off')

    ax.set_title('CATALUNYA',fontdict={'fontsize': '24', 'fontweight': '3'})

    fig=merged.plot(column='NUM_ENTITATS', cmap='inferno_r', alpha=0.8,zorder=1,edgecolor='green',linewidth=0.1, ax = ax,legend=True)              
    ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.Mapnik)

    plt.show()




def function10():
    file_path = 'ALL.csv'
    df = pd.read_csv(file_path)

    ff=pd.DataFrame(df,columns=["NOMCOMAR","NUM_ENTITATS"])

    ff.plot(x="NOMCOMAR",y="NUM_ENTITATS",kind="bar",stacked=True,figsize=(10,10))
    plt.legend(loc="lower left",bbox_to_anchor=(0.8,1.0))
    plt.show() 


#main    
next = True
while (next):
    print("List of options: \n--------------\n ")
    printOptions()
    option = int(input())
    while(option<1 or option>10):
        print("Incorrect option, the correct values are [1-10].\n")
        option = int(input())

    print("\n")
    print("Your choice is the option", option, ":\n")
    if option == 1:
        function1()
    elif option == 2:
        function2()
    elif option == 3:
        function3()
    elif option == 4:
        function4()
    elif option == 5:
        function5()
    elif option == 6:
        function6()
    elif option == 7:
        function7()
    elif option == 8:
        function8()
    elif option == 9:
        function9()
    elif option == 10:
        function10()
    
    print("\n")
    print("Do you want to run another option? [y, n]")
    o = input()
    if o.lower() != 'y':
        next = False
   
print("The program has ended\n")


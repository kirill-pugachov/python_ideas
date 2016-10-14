# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:25:56 2016

@author: Кирилл
"""

#Забираем drug_id
#Забираем аптеки по drug_id
#Делаем связку adress_id цена на препарат price 
#Определяем медиану цены на препарат
#От медианы определяем отклонение в 50%
#По минимальной и максимальной цене определяем масштаб оси Y
#По кол-ву аптек определяем масштаб оси Х
#Рисуем график в осях adress_id (X) price(Y)
#Проводим на графике медиану и линии +/- 50%

import urllib.request
import json
#import codecs
#import time
import tkinter as tk
import statistics



#Объявляем переменные 69314 12077 92625 197577 79895 127389 127390 7168 365087
drug_id=7167
geo_lat=50.391203
geo_lng=30.375645
quant=3000
quest_url1='http://apigeo.morion.ua/m/1/prop/nearest/'
canvas_width = 850
canvas_height = 650
path_to_save ='C:/Python/Service/Wrong_data_income_from_points_1.txt'

#функции
def Average_price(parsed_json):
    Sum=0
    for item in parsed_json:
        Sum+=item['p']
    return round(Sum/len(parsed_json), 2)

def Average_price_less(parsed_json):
    return round(Average_price(parsed_json)/2, 2)
         
def Average_price_more(parsed_json):
    return round(Average_price(parsed_json)*1.5, 2)

def Number_of_drugstores(parsed_json):
    return len(parsed_json)
    
def Max_price(parsed_json):
    Max_price=0
    for item in parsed_json:
        if Max_price < item['p']:
            Max_price=item['p']
    return round(Max_price, 2)
    
def Min_price(parsed_json):
    Min_price=10000000
    for item in parsed_json:
        if item['p'] <= 0:
            continue
        else:
            if Min_price > item['p']:
                Min_price=item['p']
                #print(Min_price, item['p'])
    return round(Min_price, 2)

def Mediana(parsed_json):
    A=len(parsed_json)
    sorted_parsed_json=Sorted_list(parsed_json)
    if A%2==0:
        Mediana=(sorted_parsed_json[A//2]['p']+sorted_parsed_json[A//2+1]['p'])/2
    else:
        Mediana=sorted_parsed_json[A//2+1]['p']
    return round(Mediana, 2)

def Stand_dev(parsed_json):
    Data_list=[]
    for item in parsed_json:
        Data_list.append(item['p'])
        #print(item['p'])
    #print (Data_list)
    return round(statistics.stdev(Data_list),2)
    
def Lek_forma_name(drug_id):
    full_url='http://api.geoapteka.com.ua/get_item/'+str(drug_id)
    req = urllib.request.Request(full_url)
    with urllib.request.urlopen(req) as response:
        parsed_json = json.loads(response.read().decode("utf-8-sig"))
    Lek_forma_name=parsed_json['name']+' '+parsed_json['form']+' '+parsed_json['dose']+' '+parsed_json['numb']+' '+'штук'+' '+parsed_json['make']
        
    return Lek_forma_name
    
    
    
def Sorted_list(parsed_json):
    for I in reversed(range(len(parsed_json))):
        for J in range(1, I+1):
            if parsed_json[J-1]['p']>parsed_json[J]['p']:
                #print (J, parsed_json[J-1]['p'], parsed_json[J]['p'])
                parsed_json[J], parsed_json[J-1] = parsed_json[J-1], parsed_json[J]
                #print (J, parsed_json[J-1]['p'], parsed_json[J]['p'])
        Sorted_list=parsed_json
    return Sorted_list

def Scale_count_heigt(canvas_height, parsed_json):
    Scale = (canvas_height-15)/Average_price_more(parsed_json)
    return Scale
    
def Scale_count_width(canvas_width, parsed_json):
    Scale = (canvas_width)/len(parsed_json)
    return Scale
    
def Get_result(parsed_json):
    Data_list=[]
    High_price = Average_price(parsed_json) + Stand_dev(parsed_json)*3
    Low_price = Average_price(parsed_json) - Stand_dev(parsed_json)*3
    
    for item in parsed_json:
        if item['p'] > High_price or item['p'] < Low_price:
            Data_list.append(item)
    print ('Кол-во аптек с неправильными данными =', len(Data_list))

    for I in Data_list:
        result = open (path_to_save, 'a')
        result.write (I['i']+';'+str(I['p'])+';'+str(I['q'])+';'+I['l']+';'+str(I['g'])+'\n')
        result.close ()

def Update(drug_id, root):
    drug_id=New_drug_id.get()
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bd='1', bg='pale goldenrod')
    canvas.pack()   
    canvas.delete("all")
    #читаем по запросу данные
    full_url=quest_url1+str(drug_id)+'/'+str(geo_lat)+','+str(geo_lng)+'/'+str(quant)
    #print (full_url) 
    req = urllib.request.Request(full_url)
    with urllib.request.urlopen(req) as response:
        parsed_json = json.loads(response.read().decode("utf-8-sig"))
    
    print (Sorted_list(parsed_json))
    print ('Максимальная цена =', Max_price(parsed_json))        
    print ('Минимальная цена =', Min_price(parsed_json))
    print ('Медиана цены =', Mediana(parsed_json))    
    print ('Средняя цена =', Average_price(parsed_json))
    print ('Средняя цена -50% =', Average_price_less(parsed_json))
    print ('Средняя цена +50% =', Average_price_more(parsed_json))
    print ('Кол-во аптек =', Number_of_drugstores(parsed_json))
    print ('Среднее квадратичное отклонение =', Stand_dev(parsed_json))
    print ('Имя препарата =', Lek_forma_name(drug_id))
    
 
    
    I=0
    while I < len(parsed_json):
        canvas.create_line(I*Scale_count_width(canvas_width, parsed_json), canvas_height, I*Scale_count_width(canvas_width, parsed_json), canvas_height-parsed_json[I]['p']*Scale_count_heigt(canvas_height, parsed_json), fill="springgreen2")
        I+=1

    canvas.create_line(0, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)-Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, canvas_width, canvas_height- Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) -Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, fill='cyan', dash=(7,1,1,1), width='3')
    canvas.create_text(195, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)+15-Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, text='Плюс утроенное среднее квадратичное отклонение цены + '+str(round(Stand_dev(parsed_json)*3, 2))+' грн')    
    
    canvas.create_line(0, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)+Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, canvas_width, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) + Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, fill='cyan', dash=(7,1,1,1), width='3')
    canvas.create_text(195, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) + 15 + Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, text='Минус утроенное среднее квадратичное отклонение цены - '+str(round(Stand_dev(parsed_json)*3, 2))+' грн')    
    
    
    canvas.create_line(0, canvas_height-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="indigo")
    canvas.create_text(175, canvas_height+15-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Медиана цены в Украине составляет - '+str(Mediana(parsed_json))+' грн')    
    canvas.create_line(0, canvas_height-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="red")
    canvas.create_text(175, canvas_height+15-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине -50% составляет - '+str(Average_price_less(parsed_json))+' грн')
    canvas.create_line(0, canvas_height-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="red")
    canvas.create_text(175, canvas_height+15-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине +50% составляет - '+str(Average_price_more(parsed_json))+' грн')
    canvas.create_line(0, canvas_height-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="green", width='3')    
    canvas.create_text(175, canvas_height-15-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине '+str(Average_price(parsed_json))+' грн')
    canvas.create_text(175, canvas_height-15, text='Кол-во аптек с препаратом '+str(Number_of_drugstores(parsed_json))+' точек')    
        
    
#читаем по запросу данные
full_url=quest_url1+str(drug_id)+'/'+str(geo_lat)+','+str(geo_lng)+'/'+str(quant)
#print (full_url) 
req = urllib.request.Request(full_url)
with urllib.request.urlopen(req) as response:
    parsed_json = json.loads(response.read().decode("utf-8-sig"))

print (Sorted_list(parsed_json))
print ('Максимальная цена =', Max_price(parsed_json))        
print ('Минимальная цена =', Min_price(parsed_json))
print ('Медиана цены =', Mediana(parsed_json))    
print ('Средняя цена =', Average_price(parsed_json))
print ('Средняя цена -50% =', Average_price_less(parsed_json))
print ('Средняя цена +50% =', Average_price_more(parsed_json))
print ('Кол-во аптек =', Number_of_drugstores(parsed_json))
print ('Среднее квадратичное отклонение =', Stand_dev(parsed_json))
print ('Имя препарата =', Lek_forma_name(drug_id))

#tkinter._test()

root = tk.Tk()
root.title('Цены на препарат' + ' ' + str(drug_id)+' '+Lek_forma_name(drug_id))
root.geometry('950x750+50+50')
root.resizable(False, False)

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bd='1', bg='pale goldenrod')
canvas.pack()

Frame_for_buttons = tk.Frame(root, width=canvas_width+25, height=canvas_height-25, bd='1', bg='grey')
Frame_for_buttons.pack(side='left', expand=True)

New_drug_id = tk.Entry(Frame_for_buttons, bd =5)
New_drug_id.insert(0, str(drug_id))
#New_drug_id.bind('<Button-1>', Update(drug_id, root))
New_drug_id.pack(padx=10, pady=10, side='left')

But_update=tk.Button(Frame_for_buttons, text='Обновить график', command=root.destroy)
But_update.pack(padx=5, pady=10, side='left')

But_get_result=tk.Button(Frame_for_buttons, text='Сохранить результат', command=Get_result(parsed_json))
But_get_result.pack(padx=5, pady=10, side='left')

But_close=tk.Button(Frame_for_buttons, text='Выйти', command=root.destroy)
But_close.pack(padx=10, pady=10, side='left')


I=0
while I < len(parsed_json):
    canvas.create_line(I*Scale_count_width(canvas_width, parsed_json), canvas_height, I*Scale_count_width(canvas_width, parsed_json), canvas_height-parsed_json[I]['p']*Scale_count_heigt(canvas_height, parsed_json), fill="springgreen2")
    I+=1

canvas.create_line(0, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)-Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, canvas_width, canvas_height- Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) -Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, fill='cyan', dash=(7,1,1,1), width='3')
canvas.create_text(195, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)+15-Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, text='Плюс утроенное среднее квадратичное отклонение цены + '+str(round(Stand_dev(parsed_json)*3, 2))+' грн')    

canvas.create_line(0, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)+Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, canvas_width, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) + Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, fill='cyan', dash=(7,1,1,1), width='3')
canvas.create_text(195, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) + 15 + Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, text='Минус утроенное среднее квадратичное отклонение цены - '+str(round(Stand_dev(parsed_json)*3, 2))+' грн')    


canvas.create_line(0, canvas_height-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="indigo")
canvas.create_text(175, canvas_height+15-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Медиана цены в Украине составляет - '+str(Mediana(parsed_json))+' грн')    
canvas.create_line(0, canvas_height-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="red")
canvas.create_text(175, canvas_height+15-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине -50% составляет - '+str(Average_price_less(parsed_json))+' грн')
canvas.create_line(0, canvas_height-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="red")
canvas.create_text(175, canvas_height+15-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине +50% составляет - '+str(Average_price_more(parsed_json))+' грн')
canvas.create_line(0, canvas_height-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="green", width='3')    
canvas.create_text(175, canvas_height-15-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине '+str(Average_price(parsed_json))+' грн')
canvas.create_text(175, canvas_height-15, text='Кол-во аптек с препаратом '+str(Number_of_drugstores(parsed_json))+' точек')    

canvas.mainloop()


##читаем по запросу данные
#full_url=quest_url1+str(drug_id)+'/'+str(geo_lat)+','+str(geo_lng)+'/'+str(quant)
##print (full_url) 
#req = urllib.request.Request(full_url)
#with urllib.request.urlopen(req) as response:
#    parsed_json = json.loads(response.read().decode("utf-8-sig"))
#
#print (Sorted_list(parsed_json))
#print ('Максимальная цена =', Max_price(parsed_json))        
#print ('Минимальная цена =', Min_price(parsed_json))
#print ('Медиана цены =', Mediana(parsed_json))    
#print ('Средняя цена =', Average_price(parsed_json))
#print ('Средняя цена -50% =', Average_price_less(parsed_json))
#print ('Средняя цена +50% =', Average_price_more(parsed_json))
#print ('Кол-во аптек =', Number_of_drugstores(parsed_json))
#print ('Среднее квадратичное отклонение =', Stand_dev(parsed_json))
#print ('Имя препарата =', Lek_forma_name(drug_id))
#
##tkinter._test()
#
#root = tk.Tk()
#root.title('Цены на препарат' + ' ' + str(drug_id)+' '+Lek_forma_name(drug_id))
#root.geometry('950x750+50+50')
#root.resizable(False, False)
#
#canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bd='1', bg='pale goldenrod')
#canvas.pack()
#
#Frame_for_buttons = tk.Frame(root, width=canvas_width+25, height=canvas_height-25, bd='1', bg='grey')
#Frame_for_buttons.pack(side='left', expand=True)
#
#New_drug_id = tk.Entry(Frame_for_buttons, bd =5)
#New_drug_id.insert(0, str(drug_id))
#New_drug_id.bind('<Button-1>', Update)
#New_drug_id.pack(padx=10, pady=10, side='left')
#
#But_update=tk.Button(Frame_for_buttons, text='Обновить график', command=root.destroy)
#But_update.pack(padx=5, pady=10, side='left')
#
#But_get_result=tk.Button(Frame_for_buttons, text='Сохранить результат', command=Get_result(parsed_json))
#But_get_result.pack(padx=5, pady=10, side='left')
#
#But_close=tk.Button(Frame_for_buttons, text='Выйти', command=root.destroy)
#But_close.pack(padx=10, pady=10, side='left')
#
#
#I=0
#while I < len(parsed_json):
#    canvas.create_line(I*Scale_count_width(canvas_width, parsed_json), canvas_height, I*Scale_count_width(canvas_width, parsed_json), canvas_height-parsed_json[I]['p']*Scale_count_heigt(canvas_height, parsed_json), fill="springgreen2")
#    I+=1
#
#canvas.create_line(0, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)-Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, canvas_width, canvas_height- Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) -Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, fill='cyan', dash=(7,1,1,1), width='3')
#canvas.create_text(195, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)+15-Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, text='Плюс утроенное среднее квадратичное отклонение цены + '+str(round(Stand_dev(parsed_json)*3, 2))+' грн')    
#
#canvas.create_line(0, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)+Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, canvas_width, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) + Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, fill='cyan', dash=(7,1,1,1), width='3')
#canvas.create_text(195, canvas_height - Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json) + 15 + Stand_dev(parsed_json)*Scale_count_heigt(canvas_height, parsed_json)*3, text='Минус утроенное среднее квадратичное отклонение цены - '+str(round(Stand_dev(parsed_json)*3, 2))+' грн')    
#
#
#canvas.create_line(0, canvas_height-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="indigo")
#canvas.create_text(175, canvas_height+15-Mediana(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Медиана цены в Украине составляет - '+str(Mediana(parsed_json))+' грн')    
#canvas.create_line(0, canvas_height-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="red")
#canvas.create_text(175, canvas_height+15-Average_price_less(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине -50% составляет - '+str(Average_price_less(parsed_json))+' грн')
#canvas.create_line(0, canvas_height-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="red")
#canvas.create_text(175, canvas_height+15-Average_price_more(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине +50% составляет - '+str(Average_price_more(parsed_json))+' грн')
#canvas.create_line(0, canvas_height-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), canvas_width, canvas_height-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), fill="green", width='3')    
#canvas.create_text(175, canvas_height-15-Average_price(parsed_json)*Scale_count_heigt(canvas_height, parsed_json), text='Средняя цена в Украине '+str(Average_price(parsed_json))+' грн')
#canvas.create_text(175, canvas_height-15, text='Кол-во аптек с препаратом '+str(Number_of_drugstores(parsed_json))+' точек')    
#
#canvas.mainloop()
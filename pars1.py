import csv
import os
import re
from pprint import pprint

from bs4 import BeautifulSoup
import requests

def get_html (url):
    r= requests.get(url)
    return r.text

def get_soup(html):
    soup= BeautifulSoup(html,'lxml')
    return soup
def save_html_file (text,name_file):
    with open(name_file,'w',encoding='utf-8') as html_file:
        html_file.write(text)

def open_html_file(name_file):
    with open(name_file,'r',encoding='utf-8') as html_file:
        return html_file.read()


def write_rows_csv (list_of_dict_sportsmens):
    with open('table.csv','a',newline='') as f:
        header_list=list(list_of_dict_sportsmens[0].keys())
        writer=csv.DictWriter(f,fieldnames=header_list)
        writer.writeheader()
        for sportsmen_dict in list_of_dict_sportsmens:
            writer.writerow(sportsmen_dict)
def RowHandler (tag):
    eng_name,ru_name=tag.find('a').text.strip().split(' | ')
    href=tag.find('a').get('href')
    return (eng_name,ru_name,href)
def saveFile(*args):
    with open ('text.txt','a') as f:
        f.write(' '.join(*args)[:-1] )



def main():
    url ='https://allskaters.info/skaters/rus/'
    name_file='main.html'
    file_exists=os.path.exists(name_file)
    html_text= open_html_file(name_file) if file_exists else get_html(url)
    if not file_exists:save_html_file(html_text,name_file)
    soup_html= get_soup(html_text)


    table_sports =soup_html.find('table',id='tablepress-25058')


    p = re.compile("column-1")
    all_sprotsmens=  table_sports.findAll('td',class_=p)

    dictSportsems={}.fromkeys(['eng_name',
        'ru_name',
        'href',
        'region',
        'data_birthday'])
    list_of_dict_sportsmens=[]
    list_exception_sportsmens=[]

    for i,sportsmen in enumerate(all_sprotsmens[:]):
        keys_list=list(dictSportsems.keys())[:3]
        dictSportsems.update( zip(keys_list,RowHandler(sportsmen)))

        html_sportsmen=get_html(dictSportsems['href'])
        soup_html_sportsmen = get_soup(html_sportsmen)

        try:
            pattern_data=re.compile("Дата рождения:")
            data=soup_html_sportsmen.find(string=pattern_data).find_parent('span').text.split(':')[1]
            data=re.findall(r'.*\d{4}',data)
            dictSportsems.update({'data_birthday':  str(*data).strip()})
        except Exception as e:
            list_exception_sportsmens.append((i + 1, dictSportsems['ru_name'], e, 'data'))
        try:
            pattern_region = re.compile("Регион:")
            region=soup_html_sportsmen.find( string=pattern_region).find_next('a')
            region=(region.get_text())
            dictSportsems.update({'region':region})
        except Exception as e:
            list_exception_sportsmens.append((i+1,dictSportsems['ru_name'],e, 'region'))



        finally:
            print(i+1, dictSportsems['ru_name'])
            list_of_dict_sportsmens.append(dict.copy(dictSportsems))
            dictSportsems.update((key, None) for key in dictSportsems)

    print('#'*20)
    pprint(list_exception_sportsmens)
    write_rows_csv(list_of_dict_sportsmens)




if __name__=='__main__':
    main()
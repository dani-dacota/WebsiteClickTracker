#tracks clicks on personal website and youtube using rebrandly URL

from shutil import copyfile
import json
import time
import requests
import datetime

DEBUG = True


class CSVFile:
    #READS a CSV File to produce a DICT
    #WRITES to a CSV File from a LIST of TUPLES
    #BACKS-UP a CSV File
    
    def __init__(self, name = 'log.txt') -> None:
        self.filename = name

    def set_name_to(self, name: str) -> None:
        self.filename = name

    def get_filename(self) -> str:
        return self.filename
        
    def write(self, data:[tuple], sep = ',') -> None:
        self.back_up()
        if DEBUG:
            print('Writing to CSV File')
        list_of_lines = []
        for each in data:
            str_to_write = sep.join(each)
            list_of_lines.append(str_to_write)

        file = open(self.filename,"w")
        for each in list_of_lines:
            file.write(each + '\n')
        file.close()

    def read(self) -> None:
        if DEBUG:
            print('Reading From CSV File')
        dict_to_return = dict()
        file = open(self.filename,"r")
        for line in file:
            line_data = line.split(',')
            line_data[-1] = line_data[-1].strip()
            dict_to_return[line_data[0]] = line_data[1:]
        return dict_to_return

    def back_up(self) -> None:
        now = datetime.datetime.now()
        name = self.filename.split('.')
        dest_filename = name[0]+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'.'+name[1]
        if DEBUG:
            print('Copying File...')
        copyfile(self.filename, dest_filename)
        if DEBUG:
            print('Copying Completed')
        
def list_to_dict(data:list)->dict:
  #converts lists to dict
    dict_to_return = dict()
    for each in data:
        dict_to_return[each[0]] = [each[1]]
    return dict_to_return

def merge_data(new:dict, old:dict)->dict:
  #merges data from old dict to new dict
    for each in new:
        if each in old:
            new[each] = new[each] + old[each]
    for each in old:
        if each not in new:
            print(each, 'has been changed!')
    
def data_to_info(data):
  #parses the data and returns information
    list_to_return = []
    for each in data:
        list_to_return.append(( str(each['title']), str(each['clicks'])))
    return list_to_return
    

def get_result(url: str) -> dict:
  #gets response to query from rebrandly URL
    r=requests.get(url, headers={'content-type':'application/json', 'apikey': '679ab3639bf34f079cb397f22751e866'})
    if (r.status_code == requests.codes.ok):
        data = r.json()
        return data_to_info(data)

def get_current_time() -> str:
  #returns current time
    now = datetime.datetime.now()
    return (str(now.month)+ '/' + str(now.day) + '/' + str(now.year-2000) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
    

def run():
  #main function
  #reads old data from File
  #gets new data from web server 
  #combines new data with old data 
  #shows the difference between the data 
  #shows option to write new data to file 

    filename = 'log.txt'
    list_of_tuple_sorted = sorted(get_result('https://api.rebrandly.com/v1/links'),key=lambda each: -int(each[1]))
    new_data = list_to_dict(list_of_tuple_sorted)

    csv_file = CSVFile(filename)
    
    historic_data = csv_file.read()

    merge_data(new_data, historic_data)

    new_clicks = []
    list_to_write = []
    
    for each in new_data:
        if new_data[each][0] > new_data[each][1]:
            print(each, ':', new_data[each])
            new_clicks.append('')
        list_to_write.append((each,) + tuple(new_data[each]))

    if len(new_clicks) == 0:
        print ('No New Clicks')

    choice = input('Write to File? ([No] | Yes):')
    if choice in ['Yes','yes','y','Y']:
        csv_file.write(list_to_write)
    else:
        print('Writing Skipped!')
    
    input('\nEnd of Program! Press Enter...')

if __name__ == '__main__':
    run()

import csv
import os.path
import urllib.request
import urllib.parse
import json


def filterIn(data, key_value, dictionary_value):
    filteredDictionaries = []
    for entry in data:
        for entry_key, entry_value in entry.items():
            if entry_key == key_value and entry_value == dictionary_value:
                filteredDictionaries.append(entry)
    return filteredDictionaries


def filterOut(data, key_value, dictionary_value):
    pair_is_in_dictionary = False
    filteredDictionaries = []
    for entry in data:
        for entry_key, entry_value in entry.items():
            if key_value == entry_key and dictionary_value == entry_value:
                pair_is_in_dictionary = True
        if pair_is_in_dictionary == False:
            filteredDictionaries.append(entry)
        else:
            pair_is_in_dictionary = False
    return filteredDictionaries


def filterInRange(data, key_value, given_low, given_high):
    filteredDictionaries = []
    temp_store_val = 0
    for entry in data:
        for section_key, section_value in entry.items():
            if section_key == key_value:
                temp_store_val = float(section_value)
                if given_low <= temp_store_val < given_high:
                    filteredDictionaries.append(entry)
    return filteredDictionaries


def filterByMonth(data, issue_date):
    filteredDictionaries = []
    keyvalue = ''
    for entry in data:
        for section_key, section_keyvalue in entry.items():
            if section_key == 'issued':
                keyvalue = section_keyvalue
                keyvalue = keyvalue[5] +keyvalue[6]
                if (int(keyvalue) == issue_date):
                    filteredDictionaries.append(entry)
    return filteredDictionaries
        

def filterByYear(data, issue_year):
    filteredDictionaries = []
    keyvalue = ''
    for entry in data:
        for section_key, section_keyvalue in entry.items():
            if section_key == 'issued':
                keyvalue = section_keyvalue
                keyvalue = keyvalue[0] +keyvalue[1] +keyvalue[2] + keyvalue[3]
                if (int(keyvalue) == issue_year):
                    filteredDictionaries.append(entry)
    return filteredDictionaries


def makeDictionary(keys, values):
    retval = {}
    if len(keys) != len(values):
        return -1
    else:
        for i in range (len(keys)):
            retval[keys[i]] = values[i]
    return retval


def readDataFromCSVFile(name):
    first_line = []
    retval = []
    acc_dict = {}
    with open (name, newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        first_line = next(csv_reader)
        for line in csv_reader:
            for i in range (len(first_line)):
                acc_dict[first_line[i]] = line[i]
            retval.append(acc_dict)
            acc_dict = {}
    return retval


def dictionaryToListOfValues(keys, dictionary):
    retval = []
    for key in keys:
        for k, v in dictionary.items():
            if key == k:
                retval.append(v)
    return retval


def writeDataToCSVFile(name, lst_of_dict, lst_of_keys, a_bool):
    #a_bool indicates if the first row in the csv file should be written
    #to write to a CSV file, use the following:
    #csv_writer.writerow('what you want to write')
    mybool = a_bool
    acc = []
    with open (name, 'w', newline='', encoding="utf-8") as new_csv_file:
        csv_writer = csv.writer(new_csv_file)
        if mybool:
            csv_writer.writerow(lst_of_keys)
        for dic in lst_of_dict:
            for i in range(len(lst_of_keys)):
                acc.append(dic[lst_of_keys[i]])
            csv_writer.writerow(acc)
            acc = []


def convertToJSON(name, data):
    with open (name + '.json', 'w') as json_file:
        json_file.write(json.dumps(data))




def loadData(filenameRoot, howMany):
   csvFile = filenameRoot
   if not os.path.isfile(csvFile):
       params = urllib.parse.urlencode({"$limit":howMany})
       uri = "https://data.buffalony.gov/resource/9p2d-f3yt.json?%s" % params
       response = urllib.request.urlopen(uri)
       content_string = response.read().decode()
       content = json.loads(content_string)
       writeDataToCSVFile(csvFile,content,['apno','aptype','issued','value'],True)
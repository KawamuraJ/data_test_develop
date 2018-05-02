# -*- coding: utf-8 -*-
"""
Spyder Editor

Document: booj.py
Date: 5/1/2018

"""

import requests
import xml.etree.ElementTree as ET

# sort by column
import csv
import operator

url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
in_feed_file = 'feed.xml'
csv_record_write = []
out_file = 'Mls.csv'
out_file_sort = "Mls_sort.csv"

try:
    # Get xml feed
    response = requests.get(url)
   
    # Write feed to file
    with open(in_feed_file, 'wb') as file_feed:
        file_feed.write(response.content)
        
except Exception as e:
    print('Failure downloading feed into file:\n' + str(e))
    raise
    
finally:
    try:
        file_feed.close()
    
    except:
        pass

# parse xml file
tree = ET.parse(in_feed_file)  

# Find root
root = tree.getroot()

try:
    # Open file to write to
    write_out_file = open(out_file, "w")
    
    #Iterate through Listing nodes
    for x in root.findall('Listing'):
        appliance_list = []
        appliance_list_string = None
        
        rooms_list = []
        rooms_list_string = None
        
        DateListed = x[1][6].text + ','
        YearListed = int(DateListed[:4])
        Description = x[3][2].text # text[3:] 
        
        # Filter greater/equal 2016 and check for "and" in description 
        if YearListed >= 2016 and Description.find('and'):
            
            # Assign variables
            MlsId = x[1][3].text + ','
            MlsName = x[1][4].text + ','
            StreetAddress = x[0][0].text + ','
            Price = x[1][1].text + ','
            Bedrooms = x[3][3].text + ','
            Bathrooms = str(x[3][4].text).replace('None','0') + ','
            Description_CSV = str(Description[0:200]).replace(',','-') + '\n'
            
            # Iterate through appliance nodes
            for y in x.findall('RichDetails/Appliances/Appliance'):
                if y.text != '':
                    appliance_list.append( y.text )
                
            # Made these | joined so they reside in obe field in csv file
            appliance_list_string = "|".join(appliance_list) + ','
            
            # Iterate through room nodes
            for v in x.findall('RichDetails/Rooms/Room'):
                if v.text != '':
                    rooms_list.append( v.text )
                
            # Made these | joined so they reside in obe field in csv file
            rooms_list_string = "|".join(rooms_list) + ','
            
            write_out_file.write(MlsId + MlsName + DateListed + StreetAddress + Price + Bedrooms + Bathrooms + appliance_list_string + rooms_list_string + Description_CSV)

except Exception as e:
    print('Failure while iterating through xml file:\n' + str(e))
    raise
    
finally:
    try:
        # Close out file
        write_out_file.close()
    
    except:
        pass

try:
    # sort file
    sort_csv = open(out_file, 'r')
    csv_read = csv.reader(sort_csv, delimiter=',')
    sort = sorted(csv_read, key=operator.itemgetter(2))
    
    # open new soirted file
    write_out_sort_file = open(out_file_sort, "w")
    #write header
    write_out_sort_file.write('MlsId,MlsName,DateListed,StreetAddress,Price,Bedrooms,Bathrooms,Appliances,Rooms,Description\n')
    
    #Write sorted date to final product
    for sort_rec in sort:
        write_out_sort_file.write(sort_rec[0] + ',' + sort_rec[1] + ',' + sort_rec[2] + ',' + sort_rec[3] + ',' + sort_rec[4] + ',' + sort_rec[5] + ',' + sort_rec[6] + ',' + sort_rec[7] + ',' + sort_rec[8] + ',' + sort_rec[9] + '\n')

except Exception as e:
    print('Failure sorting report file:\n' + str(e))
    raise

finally:
    try:
        write_out_sort_file.close()
    except:
        pass
    
    try:
        sort_csv.close()
    except:
        pass


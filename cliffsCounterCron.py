#!/usr/bin/env python
# coding: utf-8

## Import necessary packages
import pytesseract
from PIL import Image
import re
from csv import writer
from datetime import datetime
import subprocess
import os

# Set the working directory
os.chdir('/Users/alexandercheung/Desktop/School/cliffsCounter')
print('Current directory is ', os.getcwd())
print('+++++++++++++++++++++++', '\n')

# Set URL to pull from
url = "https://occupancy.onpointtiming.com/api/view.php?id=d5d9d4fa04782a0d"
print('URL to pull from is: ', url)
print('+++++++++++++++++++++++', '\n')

## Pull image using curl on terminal and save as raw_image.png
process = subprocess.call(['curl', url, '--output', 'raw_image.png'],
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE)

# curl https://occupancy.onpointtiming.com/api/view.php\?id\=d5d9d4fa04782a0d --output raw_image.png

# Convert image to text
image_path = '/Users/alexandercheung/Desktop/School/cliffsCounter/raw_image.png'
pytesseract.pytesseract.tesseract_cmd =  r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
img_string = pytesseract.image_to_string(Image.open(image_path))
print('URL output says: ', img_string)
print('+++++++++++++++++++++++', '\n')

# Parse text and save to csv file
img_string.split('are ')

n_climbers = 139 - int(re.search('There are (.*) spots', img_string).group(1))
print('There are ', n_climbers, ' people climbing right now.')
print('+++++++++++++++++++++++', '\n')

# save date and n_climbers as list
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
day_date = now.strftime("%d")
month_date = now.strftime("%m")
hour = now.strftime("%H")
minute = now.strftime("%M")
weekday = datetime.today().weekday()
list_values = [weekday, hour, minute, n_climbers, day_date, month_date]

# Write fxn to save date and climber count
def append_list_as_row(file_name, list_of_elem):
    # open file in append mode
    with open(file_name, 'a+', newline = '') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

# Append the new row of data to existing .csv
append_list_as_row('/Users/alexandercheung/Desktop/School/cliffsCounter/occupancy-counter.csv', list_values)
print('Most recent values have been appended to occupancy-counter.csv')
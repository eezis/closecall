import os
# get the OS indendent home direction
home_dir = os.path.expanduser("~")
import sys
# print home_dir
sys.path.append(home_dir + "/code/sites/closecall")
sys.path.append(home_dir + "/sites/closecall")
sys.path.append(home_dir + "/.virtualenvs/closecall/lib/python2.7/site-packages")

import requests

URL = "http://www.autocheck.com/vehiclehistory/autocheck/en/search-by-license-plate#showSearchVin"

# client = requests.session()

# # get the CRSFTOKEN
# client.get(URL) # sets cookie

# print crsftoken

# post_data = {'plateNumber': 'AAP 5562', 'state': 'WA'}
r = requests.get(URL)
print r.status_code
# print r.text

# print r.text

# print '\n'
# print r.status_code



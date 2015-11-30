# -*- coding: utf-8 -*-

import sys
reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')
import os

# get the OS indendent home direction
home_dir = os.path.expanduser("~")
# print home_dir
sys.path.append(home_dir + "/sites/closecall")
sys.path.append(home_dir + "/code/sites/closecall")
sys.path.append(home_dir + "/.virtualenvs/closecall/lib/python2.7/site-packages")

# print sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
import django
django.setup()

from users.models import UserProfile

jdata_no_ending = ''
jdata_for_file = ''

def get_jsondata_as_string():
    """
    This should recreate all the entries already in the json.data file, the last entry
    will be comma delimited because the whole idea is to add the last entry onto it
    """
    UPS = UserProfile.objects.all()
    total = UPS.count()
    jdata ='var data = {{ "count": {},\n'.format(total)
    jdata = jdata + '  "members": [\n'

    count = 0
    for u in UPS:
        count += 1
        lat, lon = u.get_lat_lon()
        if count <= total:
            jdata = jdata + '  {{"{}": {}, "longitude": {}, "latitude": {} }},\n'.format('member', u.id, lon, lat)
        # else:
        #     jdata = jdata + '  {{"{}": {}, "longitude": {}, "latitude": {} }}\n'.format('member', u.id, lon, lat)

    # return jdata + ']}\n'
    return jdata

def add_position_to_str(new_position):
    # new_postion should be a string that looks like this
    #   {"member": 5433, "longitude": -1.437804, "latitude": 55.0400162 }
    jdata_no_ending = jdata_no_ending + new_position + ',\n'
    jdata_for_file = jdata_no_ending + new_postion + '\n ]}\n'
    # jdata_for_file now looks like this
    #{"member": 5432, "longitude": -86.2483921, "latitude": 43.2341813 },
    #{"member": 5433, "longitude": -1.437804, "latitude": 55.0400162 }
    # }]

def write_files(filename):
    # write the oriinga
    pass


F_ALL_POSITIONS = 'jdatafilepositions.txt'
def add_position_to_file(position_no_trailing_comma):
    # open the file, append the position (w)
    fh = open(F_ALL_POSITIONS, "a")
    write(position)
    fh.close()

F_FILE_TERMINATOR = 'jdatafileterminator.txt'
def create_file_end():
    fh = open(F_FILE_TERMINATOR, "w")
    write(']}')
    fh.close()

def initialize_position_datafiles():




jdata_no_ending = get_jsondata_as_string()


print get_jsondata_as_string()

print


"""
jdatafilepositions.txt (last entry has comma, it's ready to have append operation
append now position without comma
now combine the files
jdatafileterminator.txt
    ]}
now rewrite the jdatafilepositions.txt so that it has a final comma
"""

def combine_files():
    os.system("cat jdatafilepositions.txt + jdatafileterminator.txt >> data2.json")


from pyowlet.PyOwlet import PyOwlet
import sys
from pprint import pprint

if len(sys.argv) != 3:
    print('usage:  python3 test.py username password \n')
else:

    print('using username: ' + sys.argv[1] + '\n')
    print('using password: ' + sys.argv[2] + '\n')

    print('\n\n\n')

    pyowletClient = PyOwlet(sys.argv[1], sys.argv[2])
    properties = [
        'OXYGEN_LEVEL',
        'HEART_RATE',
        'BASE_STATION_ON',
        'BATT_LEVEL',
        'MOVEMENT',
        'SOCK_OFF',
        'CHARGE_STATUS',
        'BABY_NAME',
        'SOCK_CONNECTION',
    ]

    for measure in properties:
        val = pyowletClient.get_property(measure)
        print(val)
        print('\n\n\n')

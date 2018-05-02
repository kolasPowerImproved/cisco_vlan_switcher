import collections
import csv
import subprocess
import logging

from pprint import pprint
from datetime import datetime

from consts import LOGIN, PASSWORD, ENABLE_PASSWORD


def vlan_switcher(path_to_file, vlan):
    '''
    Configure vlan in needed cisco ports
    Need file with cisco's ips and their ports to configure
    All ips must be in row named 'ip'
    All ports must be in row named 'port'
    USE VERY CAREFUL !!!
    :param path_to_file: write path to csv file with cisco ips and ports co configure, must be a string value
    :param vlan: vlan number to port's configure, must be integer value
    :return:
    '''

    file = csv.DictReader(open(path_to_file))      # open csv file
    vlan = str(vlan)                               # convert and save the vlan value
    ip_list = []                                   # empty list with cisco's ips
    port_list = []                                 # empty list with ports
    data = collections.defaultdict(list)           # empty DefaultDict for ips and ports
    logging.basicConfig(filename='logs.log',       # set logging params
                        level=logging.DEBUG)
    file_error = open('bad_logs.log', 'a')         # open file to write bad logs
    file_ok = open('logs.log', 'a')                # open file to write logs
    year = datetime.now().year                     # get current year
    month = datetime.now().month                   # get current month
    day = datetime.now().day                       # get current day
    hour = datetime.now().hour                     # get current hour
    minute = datetime.now().minute                 # get current minute
    # make a string with current time with splitters
    t_date = '(' + str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ') '

    for row in file:
        ip_list.append(row['ip'])                  # write ips to ip's list from the file with row 'ip'
        port_list.append(row['port'])              # write ports to port's list from the file with row 'port'
        data[row['ip']].append(row['port'])        # save ips and ports to the default dict

    for i in data.keys():
        ports = ("{" + "} {".join(data[i]) + "}")  # convert ports numbers to the needed format
        # sting that runs the command
        command_str = 'expect vlan_switcher.exp' + " " + '"' + LOGIN + '"' + " " + '"' + PASSWORD + '"' + " " + '"' + ENABLE_PASSWORD + '"' + " " + '"' + "10.10." + i + '"' + ' "' + ports + '" ' + '"' + vlan + '"'
        proc = subprocess.Popen(
            command_str,
            shell=True,
            stdout=subprocess.PIPE)
        for line in proc.stdout:
            line = str(line.rstrip())
            pprint(line[2:len(line)])                           # pint result without chars "b'"
            file_ok.write(t_date + line[2:len(line)] + '\n')    # write logs to file
            if line == "b''":
                # write bad logs to file
                file_error.write(t_date + 'NO CONNECTION WITH DEVICE TRY TO PING IT YOURSELF' + ' (' + '10.10.' + i + ')' + '\n')
        file_ok.write('\n')
        file_error.write('\n')

    file_error.close()
    file_ok.close()


vlan_switcher('vlan.csv', 10)

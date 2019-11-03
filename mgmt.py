#!/usr/bin/python3
# -*- coding :utf-8 -*-


import subprocess
import re
reg = r'\D+.py'


def get_componentns():
    comps = []
    command = subprocess.Popen('ls ~/python/adhoc_parser/components/', shell=True, stdout=subprocess.PIPE)
    components = command.communicate()
    for i in components:
        try:
            component = i.decode('utf-8')
            comps.append(component)
        except AttributeError:
            pass
    return comps





def mgmt(name):
    command = subprocess.Popen(f'ps -aux | grep "python3 ~/python/adhoc_parser/components/{name}/{name}.py"', shell=True, stdout=subprocess.PIPE)
    data = command.communicate()
    for line in data:
        try:
            dline = line.decode('utf-8')
        except AttributeError:
            pass
    # USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    list = dline.split('\n')

    for i in list:
        if '/bin/sh -c ps' and 'grep' in i:
            pass
        else:
            final = re.findall(reg, i)
            if final != []:
                j = 'Parser: ' + (''.join(final)).replace(' ', '').replace('python', 'Parser: ') + ' RUNNING'
                print(j)

for name in get_componentns():
    mgmt(name)
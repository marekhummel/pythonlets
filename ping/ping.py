import os
import re
import subprocess
from datetime import datetime


def ping():
    p = subprocess.Popen('ping vodafone.de -n 10', stdout=subprocess.PIPE, shell=True)
    (output, _) = p.communicate()
    p.wait()
    ms = re.findall(r'(?:Minimum|Maximum|Average) = (\d+)ms', str(output), re.DOTALL)
    rrts = [int(i) for i in ms]
    nums = [str(i).rjust(3, ' ') for i in rrts]

    line = f'[{datetime.now()}]:\tMinimum = {nums[0]}ms | Maximum = {nums[1]}ms | Average = {nums[2]}ms\r\n'
    path = os.path.join(os.path.realpath(__file__), '..', 'log.txt')
    with open(path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n')

        diff = datetime.now() - datetime.strptime(content.split('\n')[0][1:27], '%Y-%m-%d %H:%M:%S.%f')
        if (diff.seconds // 3600 > 5):
            f.write('\n')

        f.write(content)


ping()

"""
Port backend for Geert Bevin's command line programs SendMIDI and ReceiveMIDI.

https://github.com/gbevin/SendMIDI
https://github.com/gbevin/ReceiveMIDI
"""
import os
import re
import subprocess
from ..messages import prototypes, new
from ..bytes import as_bytes


def _parse_syx_line(line):
    # Example: "system-exclusive hex 01 02 03 dec"

    data = [byte for byte in line.split() if len(byte) == 2]
    return new('system_exclusive', data=bytes(int(byte, 16) for byte in data))


def dashname(scorename):
    return scorename.replace('_', '-')


def scorename(dashname):
    return dashname.replace('-', '_')


_dashnames = [dashname(name) for name in prototypes]


def from_line(line):
    if 'system-exclusive' in line:
        return _parse_syx_line(line)
    else:
        for name in _dashnames:
            if name in line:
                args = [int(arg) for arg in re.findall('(\d+)', line)]
                if 'channel' in line:
                    # Move channel to last position.
                    args = args[1:] + [args[0]]
                names = list(prototypes[scorename(name)].keys())[1:]
                return new(scorename(name), **dict(zip(names, args)))
        else:
            raise ValueError(f'unknown message: {line.strip()!r}')

    
def as_line(msg):
    hex_bytes = ' '.join(f'{byte}' for byte in as_bytes(msg))
    return f'raw {hex_bytes}'


def list_inputs():
    return [n.rstrip() for n in os.popen('receivemidi list').readlines()]


def list_outputs():
    return [n.rstrip() for n in os.popen('sendmidi list').readlines()]


def open_input(name):
    return Input(name)


def open_output(name):
    return Output(name)


def create_input(name):
    return Input(name, create=True)


def create_output(name):
    return Output(name, create=True)


class Input:
    def __init__(self, name, create=False):
        if create:
            devtype = 'virt'
        else:
            devtype = 'dev'

        args = ['receivemidi', devtype, name, 'nn']
        self._proc = subprocess.Popen(args,
                                      stdout=subprocess.PIPE)

    def __iter__(self):
        while True:
            line = self._proc.stdout.readline()
            yield from_line(line.decode('ascii'))


class Output:
    def __init__(self, name, create=False):
        if create:
            devtype = 'virt'
        else:
            devtype = 'dev'

        args = ['sendmidi', devtype, name, '--']
        self._proc = subprocess.Popen(args,
                                      stdin=subprocess.PIPE)

    def send(self, msg):
        line = as_line(msg) + '\n'
        self._proc.stdin.write(line.encode('ascii'))
        self._proc.stdin.flush()


__all__ = ['list_inputs', 'list_outputs',
           'open_input', 'open_output',
           'create_input', 'create_output']

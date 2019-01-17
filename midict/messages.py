from numbers import Integral

prototypes = {prot['msgtype']: prot for prot in [
    {'msgtype': 'note_off', 'note': 0, 'velocity': 64, 'ch': 1},
    {'msgtype': 'note_on', 'note': 0, 'velocity': 64, 'ch': 1},
    {'msgtype': 'poly_pressure', 'note': 0, 'value': 0, 'ch': 1},
    {'msgtype': 'control_change', 'number': 0, 'value': 0, 'ch': 1},
    {'msgtype': 'program_change', 'number': 0, 'ch': 1},
    {'msgtype': 'channel_pressure', 'value': 0, 'ch': 1},
    {'msgtype': 'pitch_bend', 'value': 8192, 'ch': 1},
    {'msgtype': 'system_exclusive', 'data': b''},
    {'msgtype': 'time_code', 'type': 0, 'value': 0},
    {'msgtype': 'song_position', 'beats': 0},
    {'msgtype': 'song_select', 'number': 0},
    {'msgtype': 'tune_request'},
    {'msgtype': 'midi_clock'},
    {'msgtype': 'start'},
    {'msgtype': 'stop'},
    {'msgtype': 'continue'},
    {'msgtype': 'active_sensing'},
    {'msgtype': 'reset'},
]}

_max_values = {
    ('pitch_bend', 'value'): 16383,
    ('song_position', 'beats'): 16383,
    ('time_code', 'type'): 7,
    ('time_code', 'value'): 15,
}

def check_msg(msg):
    for name, value in list(msg.items())[1:]:
        if name == 'data':
            if not isinstance(value, bytes):
                raise TypeError('system exclusive data must be bytes')
            for byte in value:
                if not 0 <= byte <= 127:
                    raise ValueError('data byte must be in range 0..127')
        elif not isinstance(value, Integral):
            raise TypeError(f'{name} must be integer')
        elif name == 'ch':
            if not 1 <= value <= 16:
                raise ValueError('ch must be in range 1..16')
        else:
            max_value = _max_values.get((msg['msgtype'], name), 127)
            if not 0 <= value <= max_value:
                raise ValueError(f'{name} must be in range 0..{max_value}')


def new(prototype, **kwargs):
    if isinstance(prototype, str):
        msg = prototypes[prototype].copy()
    else:
        msg = prototype.copy()

    if 'data' in kwargs:
        kwargs['data'] = bytes(kwargs['data'])

    for name in kwargs:
        if name not in msg:
            raise NameError(name)

    msg.update(kwargs)

    check_msg(msg)
        
    return msg

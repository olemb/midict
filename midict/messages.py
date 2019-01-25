from numbers import Integral

prototypes = {msg['type']: msg for msg in [
    {'type': 'note_off', 'note': 0, 'velocity': 64, 'ch': 1},
    {'type': 'note_on', 'note': 0, 'velocity': 64, 'ch': 1},
    {'type': 'poly_pressure', 'note': 0, 'value': 0, 'ch': 1},
    {'type': 'control_change', 'number': 0, 'value': 0, 'ch': 1},
    {'type': 'program_change', 'number': 0, 'ch': 1},
    {'type': 'channel_pressure', 'value': 0, 'ch': 1},
    {'type': 'pitch_bend', 'value': 8192, 'ch': 1},
    {'type': 'system_exclusive', 'data': b''},
    {'type': 'time_code', 'frame_type': 0, 'value': 0},
    {'type': 'song_position', 'beats': 0},
    {'type': 'song_select', 'number': 0},
    {'type': 'tune_request'},
    {'type': 'midi_clock'},
    {'type': 'start'},
    {'type': 'stop'},
    {'type': 'continue'},
    {'type': 'active_sensing'},
    {'type': 'reset'},
]}

_max_values = {
    ('pitch_bend', 'value'): 16383,
    ('song_position', 'beats'): 16383,
    ('time_code', 'frame_type'): 7,
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
            max_value = _max_values.get((msg['type'], name), 127)
            if not 0 <= value <= max_value:
                raise ValueError(f'{name} must be in range 0..{max_value}')

    return msg


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

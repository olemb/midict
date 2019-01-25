from .messages import check_msg


def note_off(note, velocity=64, ch=1):
    return check_msg({'type': 'note_off', 'note': note,
                      'velocity': velocity, 'ch': ch})


def note_on(note, velocity=64, ch=1):
    return check_msg({'type': 'note_on', 'note': note,
                      'velocity': velocity, 'ch': ch})


def poly_pressure(note, value=0, ch=1):
    return check_msg({'type': 'poly_pressure', 'note': note,
                      'value': value, 'ch': ch})


def control_change(number, value, ch=1):
    return check_msg({'type': 'control_change', 'number': number,
                      'value': value, 'ch': ch})


def program_change(number, ch=1):
    return check_msg({'type': 'program_change', 'number': number, 'ch': ch})


def channel_pressure(value, ch=1):
    return check_msg({'type': 'channel_pressure', 'value': value, 'ch': ch})


def pitch_bend(value=8192, ch=1):
    return check_msg({'type': 'pitch_bend', 'value': value, 'ch': ch})


def system_exclusive(data):
    return check_msg({'type': 'system_exclusive', 'data': bytes(data)})


def time_code(frame_type, value):
    return check_msg({'type': 'time_code', 'frame_type': frame_type,
                      'value': value})


def song_position(beats):
    return check_msg({'type': 'song_position', 'beats': beats})


def song_select(number):
    return check_msg({'type': 'song_select', 'number': number})


def tune_request():
    return check_msg({'type': 'tune_request'})


def midi_clock():
    return {'type': 'midi_clock'}


def start():
    return {'type': 'start'}


def stop():
    return {'type': 'stop'}


def continue_():
    return {'type': 'continue'}


def active_sensing():
    return {'type': 'active_sensing'}


def reset():
    return {'type': 'reset'}


__all__ = [
    'note_off',
    'note_on',
    'poly_pressure',
    'control_change',
    'program_change',
    'channel_pressure',
    'pitch_bend',
    'system_exclusive',
    'time_code',
    'song_position',
    'song_select',
    'tune_request',
    'midi_clock',
    'start',
    'stop',
    'continue_',
    'active_sensing',
    'reset',
]


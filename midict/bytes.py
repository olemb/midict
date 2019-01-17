from .messages import new


encoders = {
    'note_off': lambda msg: (0x80|msg['ch']-1, msg['note'], msg['velocity']),
    'note_on': lambda msg: (0x90|msg['ch']-1, msg['note'], msg['velocity']),
    'poly_pressure': lambda msg: (0xa0|msg['ch']-1, msg['note'], msg['value']),
    'control_change': lambda msg: (0xb0|msg['ch']-1, msg['number'], msg['value']),
    'program_change': lambda msg: (0xc0|msg['ch']-1, msg['number']),
    'channel_pressure': lambda msg: (0xd0|msg['ch']-1, msg['value']),
    'pitch_bend' :lambda msg: (0xe0|msg['ch']-1, msg['value'] & 0x7f, msg['value'] >> 7),
    'system_exclusive': lambda msg: (0xf0,) + tuple(msg['data']) + (0xf7,),
    'time_code': lambda msg: (0xf1, msg['type'] << 4 | msg['value']),
    'song_position': lambda msg: (0xf2, msg['beats'] & 0x7f, msg['beats'] >> 7),
    'song_select': lambda msg: (0xf3, msg['number']),
    'tune_request': lambda msg: (0xf6,),
    'midi_clock': lambda msg: (0xf8,),
    'start': lambda msg: (0xfa,),
    'continue': lambda msg: (0xfb,),
    'stop': lambda msg: (0xfc,),
    'activeSensing': lambda msg: (0xfe,),
    'reset': lambda msg: (0xff,),
}


decoders = {
    0x80: lambda msg: new('note_off', note=msg[1], velocity=msg[2], ch=(msg[0]&15)+1),
    0x90: lambda msg: new('note_on', note=msg[1], velocity=msg[2], ch=(msg[0]&15)+1),
    0xa0: lambda msg: new('poly_pressure', note=msg[1], value=msg[2], ch=(msg[0]&15)+1),
    0xb0: lambda msg: new('control_change', number=msg[1], value=msg[2], ch=(msg[0]&15)+1),
    0xc0: lambda msg: new('program_change', number=msg[1], ch=(msg[0]&15)+1),
    0xd0: lambda msg: new('channel_pressure', value=msg[1], ch=(msg[0]&15)+1),
    0xe0: lambda msg: new('pitch_bend', value=(msg[1] | msg[2] << 7), ch=(msg[0]&15)+1),
    0xf0: lambda msg: new('system_exclusive', data=bytes(msg[1:-1])),
    0xf1: lambda msg: new('time_code', type=msg[1] >> 4, value=msg[1] & 0xf),
    0xf2: lambda msg: new('song_position', beats=(msg[1] | msg[2] << 7)),
    0xf3: lambda msg: new('song_select', number=msg[1]),
    0xf6: lambda msg: new('tune_request'),
    0xf8: lambda msg: new('midi_clock'),
    0xfa: lambda msg: new('start'),
    0xfb: lambda msg: new('continue'),
    0xfc: lambda msg: new('stop'),
    0xfe: lambda msg: new('active_sensing'),
    0xff: lambda msg: new('reset'),
}


def as_bytes(msg):
    return encoders[msg['msgtype']](msg)


def from_bytes(midi_bytes):
    status = midi_bytes[0]
    if status < 0xf0:
        # Strip away channel.
        status &= 0xf0

    return decoders[status](midi_bytes)

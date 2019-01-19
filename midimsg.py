"""
A simple MidiMsg class implemented on top of midict.
"""
import midict


class MidiMsg:
    def __init__(self, msgtype, **kwargs):
        vars(self).update(midict.new(msgtype, **kwargs))

    def __setattr__(self):
        raise ValueError('MidiMsg is immutable')

    def __repr__(self):
        items = list(vars(self).items())[1:]
        args = ', '.join(f'{name}={value!r}' for name, value in items)
        return f'MidiMsg({self.msgtype!r}, {args})'

    def __call__(self, **kwargs):
        if 'msgtype' in kwargs:
            for msgtype in self.msgtype, kwargs['msgtype']:
                if msgtype not in {'note_on', 'note_off'}:
                    raise ValueError(
                        'type change is only allowed for note_on and note_off')

        args = vars(self).copy()
        args.update(kwargs)
        return MidiMsg(**args)


if __name__ == '__main__':
    msg = MidiMsg('note_on', note=40)
    msg2 = msg(note=60, ch=2)
    print(msg)
    print(msg2)

    print(msg(msgtype='note_off'))

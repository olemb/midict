midict - Experimental Python MIDI library using dictionaries
------------------------------------------------------------

Requires Python 3.7 (but should work with CPython 3.6 as well).

This is a modified version of https://github.com/olemb/meep/ using
plain old dictionaries instead of dataclasses.

This is currently just an experiment to see how far one can go using
built in types and pure functions.

The basic API is just three functions:

.. code-block:: python

    >>> import midict
    >>> msg = midict.note_on(60)
    >>> msg
    {'type': 'note_on', 'note': 60, 'velocity': 64, 'ch': 1}

    >>> msg = midict.new('note_on', note=60)
    {'type': 'note_on', 'note': 60, 'velocity': 64, 'ch': 1}

    >>> midict.copy(msg, velocity=10, ch=2)
    {'type': 'note_on', 'note': 60, 'velocity': 10, 'ch': 2}    

    >>> midict.as_bytes(msg)
    (144, 60, 64)
    >>> midict.from_bytes((144, 60, 64))
    {'type': 'note_on', 'note': 60, 'velocity': 64, 'ch': 1}

``new()``, ``copy()`` and ``from_bytes()`` do type and value checks
and will always return a valid message (or otherwise raise the
appropriate exceptions).

The ``continue`` message has a trailing underscore to avoid collision
with the Python keyword:

.. code-block:: python

    >>> midict.continue_()
    {'type': 'continue'}


Ports
-----

A very basic (unfinished) port API is also available with the
following functions::

    list_inputs()
    open_input(name)
    create_input(name)

    list_outputs()
    open_output(name)
    create_output(name)

The open and create functions return ``Input`` and ``Output``
objects. I have not yet decided what should go into these so they are
very basic.

There are two backend modules, ``sendmidi`` and ``rtmidi``. The
``rtmidi`` module currently has no code to receive messages.


MIDI Files
----------

I have no plans to add support for MIDI files since I don't use them,
but I've added an example to https://github.com/olemb/rawmidifile/
(``midict_midifile.py``) that sketches out one possible
implementation.


Open Questions
--------------

For this library to work it's very important to settle on a naming
convention for all messages, so most of my questions are to do with naming.

* use message and attribute names and values compatible with Mido or
  SendMIDI/ReceiveMIDI? (Currently the latter.) Examples of the same message::

      {'type': 'pitch_bend': 0, 'ch': 1}        # SendMIDI/ReceiveMIDI
      {'type': 'channel': 0, 'pitchwheel': -8192}  # Mido

* I had to rename ``time_code``'s ``type`` to ``frame_type`` to avoid
  collision. Maybe there's a better name to use? Should it also have
  ``frame_value`` like in Mido?

* ``ch`` at the end of the message?

* ``ch`` or ``channel``?

* use ``bytes`` or a list of ints for sysex data? (A list of ints is
  easier to convert to and from JSON.)

* ``type`` or something else?

* ``new()`` should probably also have another name since it also
  copies messages.


Author
------

Ole Martin Bjorndalen

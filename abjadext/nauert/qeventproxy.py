import typing

import abjad

from .qevents import QEvent


class QEventProxy:
    """
    Q-event proxy.

    Maps Q-event offset with the range of its beatspan to the range 0-1.

    ..  container:: example

        >>> q_event = nauert.PitchedQEvent(130, [0, 1, 4])
        >>> nauert.QEventProxy(q_event, 0.5)
        QEventProxy(q_event=PitchedQEvent(offset=Offset((130, 1)), pitches=(NamedPitch("c'"), NamedPitch("cs'"), NamedPitch("e'")), index=None, attachments=()), offset=Offset((1, 2)))

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset", "_q_event")

    ### INITIALIZER ###

    def __init__(self, q_event: QEvent | None = None, *offsets: abjad.typings.Offset):
        if len(offsets) == 1:
            offset = abjad.Offset(offsets[0])
            assert isinstance(q_event, QEvent)
            assert 0 <= offset <= 1
        elif len(offsets) == 2:
            minimum, maximum = (
                abjad.Offset(offsets[0]),
                abjad.Offset(offsets[1]),
            )
            assert isinstance(q_event, QEvent)
            assert minimum <= q_event.offset <= maximum
            offset = (q_event.offset - minimum) / (maximum - minimum)
        elif len(offsets) == 0:
            assert q_event is None
            offset = abjad.Offset(0)
        else:
            message = "can not initialize {}: {!r}."
            message = message.format(type(self).__name__, offsets)
            raise ValueError(message)
        self._q_event = q_event
        self._offset = abjad.Offset(offset)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a q-event proxy with offset and q-event
        equal to those of this q-event proxy. Otherwise false.
        """
        if type(self) == type(argument):
            if self.offset == argument.offset:
                if self.q_event == argument.q_event:
                    return True
        return False

    def __hash__(self) -> int:
        """
        Hashes q-event proxy.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(QEventProxy, self).__hash__()

    def __repr__(self):
        """
        Gets repr.
        """
        return (
            f"{type(self).__name__}(q_event={self.q_event!r}, offset={self.offset!r})"
        )

    ### PUBLIC PROPERTIES ###

    @property
    def index(self) -> typing.Optional[int]:
        """
        Index of q-event proxy.
        """
        assert self._q_event is not None, "There is no QEvent is this proxy."
        return self._q_event.index

    @property
    def offset(self) -> abjad.Offset:
        """
        Offset of q-event proxy.
        """
        return self._offset

    @property
    def q_event(self) -> typing.Optional[QEvent]:
        """
        Q-event of q-event proxy.
        """
        return self._q_event

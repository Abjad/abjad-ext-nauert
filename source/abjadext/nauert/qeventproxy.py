import typing

import abjad

from . import qevents as _qevents


class QEventProxy:
    """
    Q-event proxy.

    Maps Q-event offset with the range of its beatspan to the range 0-1.

    ..  container:: example

        >>> q_event = nauert.PitchedQEvent(abjad.Offset(130), [0, 1, 4])
        >>> nauert.QEventProxy(q_event, abjad.Offset(0.5))
        QEventProxy(q_event=PitchedQEvent(offset=Offset((130, 1)), pitches=...)

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset", "_q_event")

    ### INITIALIZER ###

    def __init__(
        self,
        q_event: _qevents.QEvent | None = None,
        *offsets: abjad.Offset,
    ) -> None:
        assert all(isinstance(_, abjad.Offset) for _ in offsets), repr(offsets)
        if len(offsets) == 1:
            offset = abjad.Offset(offsets[0])
            assert isinstance(q_event, _qevents.QEvent)
            assert 0 <= offset <= 1
        elif len(offsets) == 2:
            minimum, maximum = (
                abjad.Offset(offsets[0]),
                abjad.Offset(offsets[1]),
            )
            assert isinstance(q_event, _qevents.QEvent)
            assert minimum <= q_event.offset <= maximum
            offset = (q_event.offset - minimum) / (maximum - minimum)
        elif len(offsets) == 0:
            assert q_event is None
            offset = abjad.Offset(0)
        else:
            message = f"can not initialize {type(self).__name__}: {offsets!r}."
            raise ValueError(message)
        self._q_event = q_event
        self._offset = abjad.Offset(offset)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a q-event proxy with offset and q-event
        equal to those of this q-event proxy. Otherwise false.
        """
        if type(self) is type(argument):
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

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        class_name = type(self).__name__
        string = f"{class_name}(q_event={self.q_event!r}, offset={self.offset!r})"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def index(self) -> typing.Optional[int]:
        """
        Gets index of q-event proxy.
        """
        assert self._q_event is not None, "There is no QEvent is this proxy."
        return self._q_event.index

    @property
    def offset(self) -> abjad.Offset:
        """
        Gets offset of q-event proxy.
        """
        return self._offset

    @property
    def q_event(self) -> typing.Optional[_qevents.QEvent]:
        """
        Gets q-event of q-event proxy.
        """
        return self._q_event

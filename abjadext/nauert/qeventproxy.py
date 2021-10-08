import typing

import abjad

from .qevents import QEvent


class QEventProxy:
    """
    Q-event proxy.

    Maps Q-event offset with the range of its beatspan to the range 0-1.

    ..  container:: example

        >>> q_event = nauert.PitchedQEvent(130, [0, 1, 4])
        >>> proxy = nauert.QEventProxy(q_event, 0.5)
        >>> string = abjad.storage(proxy)
        >>> print(string)
        nauert.QEventProxy(
            abjad.Offset((1, 2)),
            q_event=nauert.PitchedQEvent(
                offset=abjad.Offset((130, 1)),
                pitches=(
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("cs'"),
                    abjad.NamedPitch("e'"),
                    ),
                ),
            )

    Not composer-safe.

    Used internally by ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset", "_q_event")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        q_event: typing.Optional[QEvent] = None,
        *offsets: typing.Union[int, abjad.typings.IntegerPair],
    ):
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

    def __format__(self, format_specification: str = "") -> str:
        """
        Formats q-event.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.
        """
        if format_specification in ("", "storage"):
            return abjad.storage(self)
        return str(self)

    def __hash__(self) -> int:
        """
        Hashes q-event proxy.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(QEventProxy, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self) -> abjad.FormatSpecification:
        values = []
        if self.offset:
            values.append(self.offset)
        return abjad.FormatSpecification(storage_format_args_values=tuple(values))

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

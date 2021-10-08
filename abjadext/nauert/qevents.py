import abc
import numbers
import typing

import abjad


class QEvent(abc.ABC):
    """
    Abstract Q-event.

    Represents an attack point to be quantized.

    All ``QEvents`` possess a rational offset in milliseconds, and an optional
    index for disambiguating events which fall on the same offset in a
    ``QGrid``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_attachments", "_index", "_offset")

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        offset: typing.Union[numbers.Real, abjad.typings.Number, abjad.IntegerPair] = 0,
        index: typing.Optional[int] = None,
        attachments: typing.Optional[typing.Iterable] = None,
    ):
        offset = abjad.Offset(offset)
        self._offset = offset
        self._index = index
        self._attachments = tuple(attachments or ())

    ### SPECIAL METHODS ###

    def __format__(self, format_specification: str = "") -> str:
        """
        Formats object.
        """
        return abjad.storage(self)

    def __lt__(self, argument) -> bool:
        """
        Is true when `epxr` is a q-event with offset greater than that of this
        q-event. Otherwise false.
        """
        if type(self) == type(self):
            if self.offset < argument.offset:
                return True
        return False

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        result = abjad.format._inspect_signature(self)
        signature_keyword_names = result[1]
        names = list(signature_keyword_names)
        for name in ("attachments",):
            if not getattr(self, name, None) and name in names:
                names.remove(name)
        return abjad.FormatSpecification(
            repr_is_indented=False,
            storage_format_keyword_names=names,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def attachments(self) -> tuple:
        """
        The attachments of the QEvent.
        """
        return self._attachments

    @property
    def index(self) -> typing.Optional[int]:
        """
        The optional index, for sorting QEvents with identical offsets.
        """
        return self._index

    @property
    def offset(self) -> abjad.Offset:
        """
        The offset in milliseconds of the event.
        """
        return self._offset


class PitchedQEvent(QEvent):
    """
    Pitched q-event.

    Indicates the onset of a period of pitched material in a q-event sequence.

    ..  container:: example

        >>> pitches = [0, 1, 4]
        >>> q_event = nauert.PitchedQEvent(1000, pitches)
        >>> string = abjad.storage(q_event)
        >>> print(string)
        nauert.PitchedQEvent(
            offset=abjad.Offset((1000, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                abjad.NamedPitch("cs'"),
                abjad.NamedPitch("e'"),
                ),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_attachments", "_index", "_offset", "_pitches")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        offset: typing.Union[numbers.Real, abjad.typings.Number, abjad.IntegerPair] = 0,
        pitches: typing.Optional[
            typing.Iterable[typing.Union[numbers.Number, abjad.typings.Number]]
        ] = None,
        attachments: typing.Optional[typing.Iterable] = None,
        index: typing.Optional[int] = None,
    ):
        QEvent.__init__(self, offset=offset, index=index)
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        pitches = pitches or []
        self._pitches = tuple([abjad.NamedPitch(x) for x in pitches])
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a pitched q-event with offset, pitches,
        attachments and index equal to those of this pitched q-event. Otherwise
        false.
        """
        if (
            type(self) == type(argument)
            and self.offset == argument.offset
            and self.pitches == argument.pitches
            and self.attachments == argument.attachments
            and self.index == argument.index
        ):
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes pitched q-event.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(PitchedQEvent, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def attachments(self) -> tuple:
        """
        Attachments of pitched q-event.
        """
        return self._attachments

    @property
    def pitches(self) -> typing.Tuple[abjad.NamedPitch, ...]:
        """
        Pitches of pitched q-event.
        """
        return self._pitches


class SilentQEvent(QEvent):
    """
    Silent q-event.

    ..  container:: example

        >>> q_event = nauert.SilentQEvent(1000)
        >>> string = abjad.storage(q_event)
        >>> print(string)
        nauert.SilentQEvent(
            offset=abjad.Offset((1000, 1)),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_attachments",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        offset: typing.Union[numbers.Real, abjad.typings.Number, abjad.IntegerPair] = 0,
        attachments: typing.Optional[typing.Iterable] = None,
        index: typing.Optional[int] = None,
    ):
        QEvent.__init__(self, offset=offset, index=index)
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a silent q-event with offset, attachments
        and index equal to those of this silent q-event. Otherwise false.
        """
        if (
            type(self) == type(argument)
            and self._offset == argument._offset
            and self._attachments == argument._attachments
            and self._index == argument._index
        ):
            return True
        return False

    def __hash__(self) -> int:
        """Hashes silent q-event.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(SilentQEvent, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def attachments(self) -> tuple:
        """
        Gets attachments of silent q-event.
        """
        return self._attachments


class TerminalQEvent(QEvent):
    """
    Terminal q-event.

    ..  container:: example

        >>> q_event = nauert.TerminalQEvent(1000)
        >>> string = abjad.storage(q_event)
        >>> print(string)
        nauert.TerminalQEvent(
            offset=abjad.Offset((1000, 1)),
            )

    Carries no significance outside the context of a ``QEventSequence``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        offset: typing.Union[numbers.Real, abjad.typings.Number, abjad.IntegerPair] = 0,
    ):
        QEvent.__init__(self, offset=offset)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a terminal q-event with offset equal to that
        of this terminal q-event. Otherwise false.
        """
        if type(self) == type(argument) and self.offset == argument.offset:
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes terminal q-event.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(TerminalQEvent, self).__hash__()

import abc
import dataclasses
import numbers
import typing

import abjad


@dataclasses.dataclass
class QEvent(abc.ABC):
    """
    Abstract Q-event.

    Represents an attack point to be quantized.

    All ``QEvents`` possess a rational offset in milliseconds, and an optional
    index for disambiguating events which fall on the same offset in a
    ``QGrid``.
    """

    ### CLASS VARIABLES ###

    offset: typing.Union[abjad.typings.Number, abjad.Offset] = 0
    index: typing.Optional[int] = None

    ### INITIALIZER ###

    def __post_init__(self):
        self.offset = abjad.Offset(self.offset)

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


@dataclasses.dataclass
class PitchedQEvent(QEvent):
    """
    Pitched q-event.

    Indicates the onset of a period of pitched material in a q-event sequence.

    ..  container:: example

        >>> pitches = [0, 1, 4]
        >>> q_event = nauert.PitchedQEvent(1000, pitches=pitches)
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

    pitches: typing.Optional[
        typing.Iterable[typing.Union[numbers.Number, abjad.typings.Number]]
    ] = None
    attachments: typing.Optional[typing.Iterable] = None

    ### INITIALIZER ###

    def __post_init__(self):
        super().__post_init__()
        pitches = self.pitches or []
        self.pitches = tuple([abjad.NamedPitch(x) for x in pitches])
        self.attachments = tuple(self.attachments or ())


@dataclasses.dataclass
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

    attachments: typing.Optional[typing.Iterable] = None

    ### INITIALIZER ###

    def __post_init__(self):
        super().__post_init__()
        self.attachments = tuple(self.attachments or ())


@dataclasses.dataclass
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

    pass

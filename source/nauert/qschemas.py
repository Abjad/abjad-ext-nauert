import abc
import bisect
import copy

import abjad

from . import qschemaitems as _qschemaitems
from . import qtargetitems as _qtargetitems
from . import qtargets as _qtargets
from . import searchtrees as _searchtrees


class QSchema(abc.ABC):
    """
    Abstract Q-schema.

    ``QSchema`` allows for the specification of quantization settings
    diachronically, at any time-step of the quantization process.

    In practice, this provides a means for the composer to change the tempo,
    search-tree, time-signature etc., effectively creating a template into
    which quantized rhythms can be "poured", without yet knowing what those
    rhythms might be, or even how much time the ultimate result will take. Like
    Abjad indicators the settings made at any given time-step via a ``QSchema``
    instance are understood to persist until changed.

    All concrete ``QSchema`` subclasses strongly implement default values for
    all of their parameters.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items", "_lookups")

    _keyword_argument_names: tuple[str, ...] = ()

    _search_tree = _searchtrees.UnweightedSearchTree()

    _tempo = abjad.MetronomeMark()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, *arguments, **keywords):
        if 1 == len(arguments) and isinstance(arguments[0], type(self)):
            items = copy.deepcopy(arguments[0].items)
        elif 1 == len(arguments) and isinstance(arguments[0], dict):
            items = list(arguments[0].items())
            if abjad.math.all_are_pairs_of_types(items, int, dict):
                items = [(x, self.item_class(**y)) for x, y in items]
            assert abjad.math.all_are_pairs_of_types(items, int, self.item_class)
            items = dict(items)
        elif abjad.math.all_are_pairs_of_types(arguments, int, self.item_class):
            items = dict(arguments)
        elif abjad.math.all_are_pairs_of_types(arguments, int, dict):
            items = [(x, self.item_class(**y)) for x, y in arguments]
            items = dict(items)
        elif all(isinstance(x, self.item_class) for x in arguments):
            items = [(i, x) for i, x in enumerate(arguments)]
            items = dict(items)
        elif all(isinstance(x, dict) for x in arguments):
            items = [(i, self.item_class(**x)) for i, x in enumerate(arguments)]
            items = dict(items)
        else:
            raise ValueError
        if items:
            assert 0 <= min(items)
        self._items = dict(items)
        self._lookups = self._create_lookups()

    ### SPECIAL METHODS ###

    def __call__(self, duration: abjad.Duration) -> _qtargets.QTarget:
        """
        Calls QSchema on ``duration``.
        """
        assert isinstance(duration, abjad.Duration), repr(duration)
        target_items = []
        idx, current_offset = 0, abjad.Offset(0)
        duration = abjad.Duration(duration)
        while current_offset < duration:
            lookup = self[idx]
            lookup["offset_in_ms"] = current_offset
            target_item = self.target_item_class(**lookup)
            target_items.append(target_item)
            current_offset += target_item.duration_in_ms
            idx += 1
        return self.target_class(target_items)

    def __getitem__(self, argument: int) -> dict:
        """
        Gets item or slice identified by `argument`.
        """
        assert isinstance(argument, int) and 0 <= argument
        result = {}
        for field in self._lookups:
            lookup = self._lookups[field].get(argument)
            if lookup is not None:
                result[field] = lookup
            else:
                keys = sorted(self._lookups[field].keys())
                idx = bisect.bisect(keys, argument)
                if len(keys) == idx:
                    key = keys[-1]
                elif argument < keys[idx]:
                    key = keys[idx - 1]
                result[field] = self._lookups[field][key]
        return result

    ### PRIVATE METHODS ###

    def _create_lookups(self) -> dict[str, dict]:
        names = self._keyword_argument_names
        lookups = {}
        for name in names:
            lookups[name] = {0: getattr(self, name)}
            for position, item in self.items.items():
                value = getattr(item, name)
                if value is not None:
                    lookups[name][position] = value
            lookups[name] = dict(lookups[name])
        return dict(lookups)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def item_class(self):
        """
        Gets schema's item class.
        """
        raise NotImplementedError

    @property
    def items(self) -> dict[int, _qschemaitems.QSchemaItem]:
        """
        Gets items dictionary.
        """
        return self._items

    @property
    def search_tree(self) -> _searchtrees.SearchTree:
        """
        Gets default search tree.
        """
        return self._search_tree

    @abc.abstractproperty
    def target_class(self):
        """
        Gets schema's target class.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def target_item_class(self):
        """
        Gets schema's target class' item class.
        """
        raise NotImplementedError

    @property
    def tempo(self) -> abjad.MetronomeMark:
        """
        Gets default tempo.
        """
        return self._tempo


class BeatwiseQSchema(QSchema):
    r"""
    Beatwise q-schema.

    Treats beats as timestep unit.

        >>> q_schema = nauert.BeatwiseQSchema()

        Without arguments, it uses smart defaults:

    ..  container:: example

        Each time-step in a ``BeatwiseQSchema`` is composed of three settings:

            * ``beatspan``
            * ``search_tree``
            * ``tempo``

        These settings can be applied as global defaults for the schema via keyword
        arguments, which persist until overridden:

        >>> beatspan = abjad.Duration(5, 16)
        >>> search_tree = nauert.UnweightedSearchTree({7: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 54)
        >>> q_schema = nauert.BeatwiseQSchema(
        ...     beatspan=beatspan,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

    ..  container:: example

        The computed value at any non-negative time-step can be found by
        subscripting:

        >>> index = 0
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print("{}:".format(key), value)
        ...
        beatspan: 5/16
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: MetronomeMark(...)

        >>> index = 1000
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print("{}:".format(key), value)
        ...
        beatspan: 5/16
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: MetronomeMark(...)

    ..  container:: example

        Per-time-step settings can be applied in a variety of ways.

        Instantiating the schema via ``*arguments`` with a series of either
        ``BeatwiseQSchemaItem`` instances, or dictionaries which could be used to
        instantiate ``BeatwiseQSchemaItem`` instances, will apply those settings
        sequentially, starting from time-step ``0``:

        >>> a = {"beatspan": abjad.Duration(5, 32)}
        >>> b = {"beatspan": abjad.Duration(3, 16)}
        >>> c = {"beatspan": abjad.Duration(1, 8)}

        >>> q_schema = nauert.BeatwiseQSchema(a, b, c)

        >>> q_schema[0]["beatspan"]
        Duration(5, 32)

        >>> q_schema[1]["beatspan"]
        Duration(3, 16)

        >>> q_schema[2]["beatspan"]
        Duration(1, 8)

        >>> q_schema[3]["beatspan"]
        Duration(1, 8)

    ..  container:: example

        Similarly, instantiating the schema from a single dictionary, consisting
        of integer:specification pairs, or a sequence via ``*arguments`` of (integer,
        specification) pairs, allows for applying settings to  non-sequential
        time-steps:

        >>> a = {"search_tree": nauert.UnweightedSearchTree({2: None})}
        >>> b = {"search_tree": nauert.UnweightedSearchTree({3: None})}

        >>> settings = {
        ...     2: a,
        ...     4: b,
        ... }

        >>> q_schema = nauert.BeatwiseQSchema(settings)

        >>> import pprint
        >>> ust = q_schema[0]["search_tree"]
        >>> pprint.pprint(ust.definition)
        {2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
        3: {2: {2: None}, 3: None, 5: None},
        5: {2: None, 3: None},
        7: {2: None},
        11: None,
        13: None}

        >>> ust = q_schema[1]["search_tree"]
        >>> pprint.pprint(ust.definition)
        {2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
        3: {2: {2: None}, 3: None, 5: None},
        5: {2: None, 3: None},
        7: {2: None},
        11: None,
        13: None}

        >>> q_schema[2]["search_tree"]
        UnweightedSearchTree(definition={2: None})

        >>> q_schema[3]["search_tree"]
        UnweightedSearchTree(definition={2: None})

        >>> q_schema[4]["search_tree"]
        UnweightedSearchTree(definition={3: None})

        >>> q_schema[1000]["search_tree"]
        UnweightedSearchTree(definition={3: None})

    ..  container:: example

        The following is equivalent to the above schema definition:

        >>> q_schema = nauert.BeatwiseQSchema(
        ...     (2, {"search_tree": nauert.UnweightedSearchTree({2: None})}),
        ...     (4, {"search_tree": nauert.UnweightedSearchTree({3: None})}),
        ... )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_beatspan", "_items", "_lookups", "_search_tree", "_tempo")

    _keyword_argument_names = ("beatspan", "search_tree", "tempo")

    ### INITIALIZER ###

    def __init__(self, *arguments, **keywords):
        self._beatspan = abjad.Duration(keywords.get("beatspan", (1, 4)))
        search_tree = keywords.get("search_tree", _searchtrees.UnweightedSearchTree())
        assert isinstance(search_tree, _searchtrees.SearchTree)
        self._search_tree = search_tree
        tempo = keywords.get("tempo", (abjad.Duration(1, 4), 60))
        if isinstance(tempo, tuple):
            tempo = abjad.MetronomeMark(*tempo)
        self._tempo = tempo
        QSchema.__init__(self, *arguments, **keywords)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = f"{type(self).__name__}(beatspan={self.beatspan!r},"
        string += f" search_tree={self.search_tree!r}, tempo={self.tempo!r})"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self) -> abjad.Duration:
        """
        Gets default beatspan of beatwise q-schema.
        """
        return self._beatspan

    @property
    def item_class(self) -> type[_qschemaitems.BeatwiseQSchemaItem]:
        """
        Gets schema's item class.
        """
        return _qschemaitems.BeatwiseQSchemaItem

    @property
    def target_class(self) -> type[_qtargets.BeatwiseQTarget]:
        """
        Gets target class of beatwise q-schema.
        """
        return _qtargets.BeatwiseQTarget

    @property
    def target_item_class(self) -> type[_qtargetitems.QTargetBeat]:
        """
        Gets target item class of beatwise q-schema.
        """
        return _qtargetitems.QTargetBeat


class MeasurewiseQSchema(QSchema):
    r"""
    Measurewise q-schema.

    Treats measures as its timestep unit.

    >>> q_schema = nauert.MeasurewiseQSchema()

    ..  container:: example

        Without arguments, it uses smart defaults:

        >>> import pprint
        >>> pprint.pprint(q_schema.search_tree.definition)
        {2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
        3: {2: {2: None}, 3: None, 5: None},
        5: {2: None, 3: None},
        7: {2: None},
        11: None,
        13: None}

    ..  container:: example

        Each time-step in a ``MeasurewiseQSchema`` is composed of four settings:

            * ``search_tree``
            * ``tempo``
            * ``time_signature``
            * ``use_full_measure``

        These settings can be applied as global defaults for the schema via keyword
        arguments, which persist until overridden:

        >>> search_tree = nauert.UnweightedSearchTree({7: None})
        >>> time_signature = abjad.TimeSignature((3, 4))
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 54)
        >>> use_full_measure = True
        >>> q_schema = nauert.MeasurewiseQSchema(
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ...     use_full_measure=use_full_measure,
        ... )

        All of these settings are self-descriptive, except for
        ``use_full_measure``, which controls whether the measure is subdivided
        by the ``quantize`` function into beats according to its time
        signature.

        If ``use_full_measure`` is ``False``, the time-step's measure will be
        divided into units according to its time-signature.  For example, a 4/4
        measure will be divided into 4 units, each having a beatspan of 1/4.

        On the other hand, if ``use_full_measure`` is set to ``True``, the
        time-step's measure will not be subdivided into independent
        quantization units. This usually results in full-measure tuplets.

    ..  container:: example

        The computed value at any non-negative time-step can be found by
        subscripting:

        >>> index = 0
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print("{}:".format(key), value)
        ...
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: MetronomeMark(...)
        time_signature: TimeSignature(pair=(3, 4), hide=False, partial=None)
        use_full_measure: True

        >>> index = 1000
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print("{}:".format(key), value)
        ...
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: MetronomeMark(...)
        time_signature: TimeSignature(pair=(3, 4), hide=False, partial=None)
        use_full_measure: True

    ..  container:: example

        Per-time-step settings can be applied in a variety of ways.

        Instantiating the schema via ``*arguments`` with a series of either
        ``MeasurewiseQSchemaItem`` instances, or dictionaries which could be
        used to instantiate ``MeasurewiseQSchemaItem`` instances, will apply
        those settings sequentially, starting from time-step ``0``:

        >>> a = {"search_tree": nauert.UnweightedSearchTree({2: None})}
        >>> b = {"search_tree": nauert.UnweightedSearchTree({3: None})}
        >>> c = {"search_tree": nauert.UnweightedSearchTree({5: None})}

        >>> q_schema = nauert.MeasurewiseQSchema(a, b, c)

        >>> q_schema[0]["search_tree"]
        UnweightedSearchTree(definition={2: None})

        >>> q_schema[1]["search_tree"]
        UnweightedSearchTree(definition={3: None})

        >>> q_schema[2]["search_tree"]
        UnweightedSearchTree(definition={5: None})

        >>> q_schema[1000]["search_tree"]
        UnweightedSearchTree(definition={5: None})

    ..  container:: example

        Similarly, instantiating the schema from a single dictionary,
        consisting of integer:specification pairs, or a sequence via
        ``*arguments`` of (integer, specification) pairs, allows for applying
        settings to non-sequential time-steps:

        >>> a = {"time_signature": abjad.TimeSignature((7, 32))}
        >>> b = {"time_signature": abjad.TimeSignature((3, 4))}
        >>> c = {"time_signature": abjad.TimeSignature((5, 8))}

        >>> settings = {
        ...     2: a,
        ...     4: b,
        ...     6: c,
        ... }

        >>> q_schema = nauert.MeasurewiseQSchema(settings)

        >>> q_schema[0]["time_signature"]
        TimeSignature(pair=(4, 4), hide=False, partial=None)

        >>> q_schema[1]["time_signature"]
        TimeSignature(pair=(4, 4), hide=False, partial=None)

        >>> q_schema[2]["time_signature"]
        TimeSignature(pair=(7, 32), hide=False, partial=None)

        >>> q_schema[3]["time_signature"]
        TimeSignature(pair=(7, 32), hide=False, partial=None)

        >>> q_schema[4]["time_signature"]
        TimeSignature(pair=(3, 4), hide=False, partial=None)

        >>> q_schema[5]["time_signature"]
        TimeSignature(pair=(3, 4), hide=False, partial=None)

        >>> q_schema[6]["time_signature"]
        TimeSignature(pair=(5, 8), hide=False, partial=None)

        >>> q_schema[1000]["time_signature"]
        TimeSignature(pair=(5, 8), hide=False, partial=None)

    ..  container:: example

        The following is equivalent to the above schema definition:

        >>> q_schema = nauert.MeasurewiseQSchema(
        ...     (2, {"time_signature": abjad.TimeSignature((7, 32))}),
        ...     (4, {"time_signature": abjad.TimeSignature((3, 4))}),
        ...     (6, {"time_signature": abjad.TimeSignature((5, 8))}),
        ... )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_items",
        "_lookups",
        "_search_tree",
        "_tempo",
        "_time_signature",
        "_use_full_measure",
    )

    _keyword_argument_names = (
        "search_tree",
        "tempo",
        "time_signature",
        "use_full_measure",
    )

    ### INITIALIZER ###

    def __init__(self, *arguments, **keywords):
        search_tree = keywords.get("search_tree", _searchtrees.UnweightedSearchTree())
        assert isinstance(search_tree, _searchtrees.SearchTree)
        self._search_tree = search_tree
        tempo = keywords.get("tempo", (abjad.Duration(1, 4), 60))
        if isinstance(tempo, tuple):
            tempo = abjad.MetronomeMark(*tempo)
        self._tempo = tempo
        time_signature = keywords.get("time_signature", (4, 4))
        if isinstance(time_signature, abjad.TimeSignature):
            self._time_signature = abjad.TimeSignature(time_signature.pair)
        elif isinstance(time_signature, tuple):
            self._time_signature = abjad.TimeSignature(time_signature)
        else:
            raise TypeError(time_signature)
        self._use_full_measure = bool(keywords.get("use_full_measure"))
        QSchema.__init__(self, *arguments, **keywords)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = f"{type(self).__name__}(search_tree={self.search_tree!r},"
        string += f" tempo={self.tempo!r}, time_signature={self.time_signature!r},"
        string += f" use_full_measure={self.use_full_measure})"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self) -> type[_qschemaitems.MeasurewiseQSchemaItem]:
        """
        Gets item class of measurewise q-schema.
        """
        return _qschemaitems.MeasurewiseQSchemaItem

    @property
    def target_class(self) -> type[_qtargets.MeasurewiseQTarget]:
        """
        Gets target class of measurewise q-schema.
        """
        return _qtargets.MeasurewiseQTarget

    @property
    def target_item_class(self) -> type[_qtargetitems.QTargetMeasure]:
        """
        Gets target item class of measurewise q-schema.
        """
        return _qtargetitems.QTargetMeasure

    @property
    def time_signature(self) -> abjad.TimeSignature:
        """
        Gets default time signature of measurewise q-schema.

        ..  container:: example

            >>> q_schema = nauert.MeasurewiseQSchema(
            ...     time_signature=abjad.TimeSignature((3, 4))
            ... )
            >>> q_schema.time_signature
            TimeSignature(pair=(3, 4), hide=False, partial=None)

        ..  container:: example

            If there are multiple time signatures in the QSchema, this returns
            the default time signature of (4, 4).

            >>> a = {"time_signature": abjad.TimeSignature((7, 32))}
            >>> b = {"time_signature": abjad.TimeSignature((3, 4))}
            >>> c = {"time_signature": abjad.TimeSignature((5, 8))}

            >>> settings = {
            ...     2: a,
            ...     4: b,
            ...     6: c,
            ... }

            >>> q_schema = nauert.MeasurewiseQSchema(settings)
            >>> q_schema.time_signature
            TimeSignature(pair=(4, 4), hide=False, partial=None)

        """
        return self._time_signature

    @property
    def use_full_measure(self) -> bool:
        """
        Is true when class uses full-measure-as-beatspan default.
        """
        return self._use_full_measure

import bisect
import copy
import typing

import uqbar.containers
import uqbar.graphs

import abjad

from .qeventproxy import QEventProxy


class QGridLeaf(abjad.rhythmtrees.RhythmTreeMixin, uqbar.containers.UniqueTreeNode):
    """
    Q-grid leaf.

    ..  container:: example

        >>> nauert.QGridLeaf()
        QGridLeaf(preprolated_duration=Duration(1, 1), q_event_proxies=[], is_divisible=True)

    Used internally by ``QGrid``.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        preprolated_duration: abjad.typings.Duration = abjad.Duration(1),
        q_event_proxies: typing.Sequence[QEventProxy] | None = None,
        is_divisible: bool = True,
    ):
        uqbar.containers.UniqueTreeNode.__init__(self)
        assert isinstance(preprolated_duration, abjad.Duration), repr(
            preprolated_duration
        )
        abjad.rhythmtrees.RhythmTreeMixin.__init__(self, preprolated_duration)
        if q_event_proxies is None:
            self._q_event_proxies = []
        else:
            assert all(isinstance(x, QEventProxy) for x in q_event_proxies)
            self._q_event_proxies = list(q_event_proxies)
        self._is_divisible = bool(is_divisible)

    ### SPECIAL METHODS ###

    def __call__(
        self, pulse_duration: abjad.typings.Duration | int
    ) -> list[abjad.Note | abjad.Tuplet]:
        """
        Calls q-grid leaf.
        """
        pulse_duration = abjad.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        return abjad.makers.make_notes(0, total_duration)

    def __graph__(self, **keywords: None) -> uqbar.graphs.Graph:
        """
        Graphviz graph of q-grid leaf.

        Returns Graphviz graph.
        """
        graph = uqbar.graphs.Graph(name="G")
        node = uqbar.graphs.Node(
            attributes={"label": str(self.preprolated_duration), "shape": "box"}
        )
        graph.append(node)
        return graph

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(preprolated_duration={self.preprolated_duration!r}, q_event_proxies={self.q_event_proxies!r}, is_divisible={self.is_divisible!r})"

    ### PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self) -> list[str]:
        return [str(self.preprolated_duration)]

    ### PUBLIC PROPERTIES ###

    @property
    def is_divisible(self) -> bool:
        """
        Flag for whether the node may be further divided
        under some search tree.
        """
        return self._is_divisible

    @is_divisible.setter
    def is_divisible(self, argument):
        self._is_divisible = bool(argument)

    @property
    def preceding_q_event_proxies(self) -> list[QEventProxy]:
        """
        Preceding q-event proxies of q-grid leaf.
        """
        return [x for x in self._q_event_proxies if x.offset < self.start_offset]

    @property
    def q_event_proxies(self) -> list[QEventProxy]:
        """
        Q-event proxies of q-grid leaf.
        """
        return self._q_event_proxies

    @property
    def rtm_format(self) -> str:
        """
        RTM format of q-grid leaf.
        """
        return str(self.preprolated_duration)

    @property
    def succeeding_q_event_proxies(self) -> list[QEventProxy]:
        """
        Succeeding q-event proxies of q-grid leaf.
        """
        return [x for x in self._q_event_proxies if self.start_offset <= x.offset]


class QGridContainer(abjad.rhythmtrees.RhythmTreeContainer):
    """
    Q-grid container.

    ..  container:: example

        >>> nauert.QGridContainer()
        QGridContainer((1, 1))

    Used internally by ``QGrid``.
    """

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self) -> type:
        return QGridLeaf

    @property
    def _node_class(self) -> tuple[type, type]:
        return (type(self), QGridLeaf)

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self) -> tuple[QGridLeaf, ...]:
        """
        Get leaves.
        """
        return tuple(_ for _ in self.depth_first() if isinstance(_, QGridLeaf))


class QGrid:
    """
    Q-grid.

    Rhythm-tree-based model for how millisecond attack points collapse onto the
    offsets generated by a nested rhythmic structure.

    >>> q_grid = nauert.QGrid()

    ..  container:: example

        >>> q_grid
        QGrid(root_node=QGridLeaf(preprolated_duration=Duration(1, 1), q_event_proxies=[], is_divisible=True), next_downbeat=QGridLeaf(preprolated_duration=Duration(1, 1), q_event_proxies=[], is_divisible=True))

    ..  container:: example

        ``QGrids`` model not only the internal nodes of the nesting structure,
        but also the downbeat to the "next" ``QGrid``, allowing events which
        occur very late within one structure to collapse virtually onto the
        beginning of the next structure.

        ``QEventProxies`` can be "loaded in" to the node contained by the
        ``QGrid`` closest to their virtual offset:

        >>> q_event_a = nauert.PitchedQEvent(250, [0])
        >>> q_event_b = nauert.PitchedQEvent(750, [1])
        >>> proxy_a = nauert.QEventProxy(q_event_a, 0.25)
        >>> proxy_b = nauert.QEventProxy(q_event_b, 0.75)

        >>> q_grid.fit_q_events([proxy_a, proxy_b])

        >>> for q_event_proxy in q_grid.root_node.q_event_proxies:
        ...     q_event_proxy
        ...
        QEventProxy(q_event=PitchedQEvent(offset=Offset((250, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=()), offset=Offset((1, 4)))

        >>> for q_event_proxy in q_grid.next_downbeat.q_event_proxies:
        ...     q_event_proxy
        ...
        QEventProxy(q_event=PitchedQEvent(offset=Offset((750, 1)), pitches=(NamedPitch("cs'"),), index=None, attachments=()), offset=Offset((3, 4)))

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_next_downbeat", "_root_node")

    ### INITIALIZATION ###

    def __init__(
        self,
        root_node: QGridLeaf | QGridContainer | None = None,
        next_downbeat: QGridLeaf | None = None,
    ):
        if root_node is None:
            root_node = QGridLeaf(preprolated_duration=abjad.Duration(1, 1))
        assert isinstance(
            root_node,
            (QGridLeaf, QGridContainer),
        )
        if next_downbeat is None:
            next_downbeat = QGridLeaf(preprolated_duration=abjad.Duration(1, 1))
        assert isinstance(next_downbeat, QGridLeaf)
        self._root_node = root_node
        self._next_downbeat = next_downbeat
        self._next_downbeat._offset = abjad.Offset(1)
        self._next_downbeat._offsets_are_current = True

    ### SPECIAL METHODS ###

    def __call__(
        self, beatspan: abjad.typings.Duration | int
    ) -> list[abjad.Note | abjad.Tuplet] | list[abjad.Leaf | abjad.Tuplet]:
        """
        Calls q-grid.
        """
        result = self.root_node(beatspan)
        result_logical_ties = [
            logical_tie for logical_tie in abjad.iterate.logical_ties(result)
        ]
        assert len(result_logical_ties) == len(self.leaves[:-1])
        for logical_tie, q_grid_leaf in zip(result_logical_ties, self.leaves[:-1]):
            if q_grid_leaf.q_event_proxies:
                q_events = [
                    q_event_proxy.q_event
                    for q_event_proxy in q_grid_leaf.q_event_proxies
                ]
                q_events.sort(
                    key=lambda x: 0 if x is None or x.index is None else x.index
                )
                annotation = {"q_events": tuple(q_events)}
                leaf = abjad.get.leaf(logical_tie, 0)
                abjad.attach(annotation, leaf)
        return result

    def __copy__(self, *arguments: None) -> "QGrid":
        """
        Copies q-grid.

        Returns new q-grid.
        """
        root_node, next_downbeat = self._root_node, self._next_downbeat
        return type(self)(copy.deepcopy(root_node), copy.deepcopy(next_downbeat))

    def __eq__(self, argument) -> bool:
        """
        True if `argument` is a q-grid with root node and next downbeat
        equal to those of this q-grid. Otherwise false.

        Returns true or false.
        """
        if type(self) == type(argument):
            if self.root_node == argument.root_node:
                if self.next_downbeat == argument.next_downbeat:
                    return True
        return False

    def __hash__(self) -> int:
        """
        Hashes q-grid.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super(QGrid, self).__hash__()

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(root_node={self.root_node!r}, next_downbeat={self.next_downbeat!r})"

    ### PUBLIC PROPERTIES ###

    @property
    def distance(self) -> typing.Optional[abjad.Duration]:
        r"""The computed total distance (divided by the number of
        ``QEventProxy`` s) of the offset of each ``QEventProxy`` contained by
        the ``QGrid`` to the offset of the ``QGridLeaf`` to which the
        ``QEventProxy`` is attached.

        Return ``Duration`` instance.

        ..  container:: example

            >>> q_grid = nauert.QGrid()

            >>> q_event_a = nauert.PitchedQEvent(250, [0], ["A"])
            >>> q_event_b = nauert.PitchedQEvent(750, [1], ["B"])
            >>> proxy_a = nauert.QEventProxy(q_event_a, 0.25)
            >>> proxy_b = nauert.QEventProxy(q_event_b, 0.75)
            >>> q_grid.fit_q_events([proxy_a, proxy_b])
            >>> print(q_grid.rtm_format)
            1

            >>> for index, (leaf, offset) in enumerate(zip(q_grid.leaves, q_grid.offsets)):
            ...     for q_event_proxy in leaf.q_event_proxies:
            ...         q_event = q_event_proxy.q_event
            ...         print(
            ...             "leaf's index: {}, leaf's offset: {}, q_event: {}".format(
            ...                 index, offset, q_event.attachments
            ...             )
            ...         )
            ...
            leaf's index: 0, leaf's offset: 0, q_event: ('A',)
            leaf's index: 1, leaf's offset: 1, q_event: ('B',)

            >>> q_grid.distance
            Duration(1, 4)

            >>> q_events = q_grid.subdivide_leaves([(0, (1, 1))])
            >>> q_grid.fit_q_events(q_events)
            >>> q_events = q_grid.subdivide_leaves([(0, (1, 1))])
            >>> q_grid.fit_q_events(q_events)
            >>> print(q_grid.rtm_format)
            (1 ((1 (1 1)) 1))

            >>> for index, (leaf, offset) in enumerate(zip(q_grid.leaves, q_grid.offsets)):
            ...     for q_event_proxy in leaf.q_event_proxies:
            ...         q_event = q_event_proxy.q_event
            ...         print(
            ...             "leaf's index: {}, leaf's offset: {}, q_event: {}".format(
            ...                 index, offset, q_event.attachments
            ...             )
            ...         )
            ...
            leaf's index: 1, leaf's offset: 1/4, q_event: ('A',)
            leaf's index: 2, leaf's offset: 1/2, q_event: ('B',)

            >>> q_grid.distance
            Duration(1, 8)

        """
        count = 0
        absolute_distance = abjad.Duration(0)
        for leaf, offset in zip(self.leaves, self.offsets):
            for q_event_proxy in leaf.q_event_proxies:
                absolute_distance += abs(q_event_proxy.offset - offset)
                count += 1
        if count:
            return absolute_distance / count
        return None

    @property
    def leaves(self) -> tuple[QGridLeaf, ...]:
        r"""All of the leaf nodes in the QGrid, including the next
        downbeat's node.

        Returns tuple of ``QGridLeaf`` instances.
        """
        if isinstance(self._root_node, QGridLeaf):
            return (self._root_node, self._next_downbeat)
        return self._root_node.leaves + (self._next_downbeat,)

    @property
    def next_downbeat(self) -> QGridLeaf:
        r"""The node representing the "next" downbeat after the contents
        of the QGrid's tree.

        Return ``QGridLeaf`` instance.
        """
        return self._next_downbeat

    @property
    def offsets(self) -> tuple[abjad.Offset, ...]:
        r"""The offsets between 0 and 1 of all of the leaf nodes in the QGrid.

        Returns tuple of ``Offset`` instances.
        """
        return tuple([x.start_offset for x in self.leaves[:-1]] + [abjad.Offset(1)])

    @property
    def pretty_rtm_format(self) -> str:
        r"""The pretty RTM-format of the root node of the ``QGrid``.

        Returns string.
        """
        return self._root_node.pretty_rtm_format

    @property
    def root_node(self) -> QGridLeaf | QGridContainer:
        r"""The root node of the ``QGrid``.

        Return ``QGridLeaf`` or ``QGridContainer``.
        """
        return self._root_node

    @property
    def rtm_format(self) -> str:
        r"""The RTM format of the root node of the ``QGrid``.

        Returns string.
        """
        return self._root_node.rtm_format

    ### PUBLIC METHODS ###

    def fit_q_events(self, q_event_proxies: typing.Sequence[QEventProxy]) -> None:
        r"""Fit each ``QEventProxy`` in ``q_event_proxies`` onto
        the contained ``QGridLeaf`` whose offset is nearest.

        Returns None
        """
        assert all(isinstance(x, QEventProxy) for x in q_event_proxies)
        leaves, offsets = self.leaves, self.offsets
        for q_event_proxy in q_event_proxies:
            idx = bisect.bisect_left(offsets, q_event_proxy.offset)
            if q_event_proxy.offset == offsets[idx]:
                leaves[idx].q_event_proxies.append(q_event_proxy)
            else:
                left, right = offsets[idx - 1], offsets[idx]
                left_diff = abs(left - q_event_proxy.offset)
                right_diff = abs(right - q_event_proxy.offset)
                if right_diff < left_diff:
                    leaves[idx].q_event_proxies.append(q_event_proxy)
                else:
                    leaves[idx - 1].q_event_proxies.append(q_event_proxy)

    def regroup_leaves_with_unencessary_divisions(self) -> None:
        """
        Regroup leaves that belong to the same parent in which only the first
        leaf contains q_event_prox[y|ies].
        """
        index = 0
        while True:
            leaf = self.leaves[index]
            parent = leaf.parent
            if isinstance(parent, QGridContainer):
                leaves = parent.leaves
                if len(leaves) > 1 and all(
                    [_leaf.q_event_proxies == [] for _leaf in leaves[1:]]
                ):
                    parent_preprolated_duration = parent.preprolated_duration
                    assert isinstance(parent_preprolated_duration, abjad.Duration)
                    new_leaf = QGridLeaf(
                        preprolated_duration=parent_preprolated_duration,
                        q_event_proxies=leaves[0].q_event_proxies,
                    )
                    index = parent.parent.index(parent)
                    parent.parent[index] = [new_leaf]
            index += 1
            if index == len(self.leaves):
                break

    def sort_q_events_by_index(self) -> None:
        r"""Sort ``QEventProxies`` attached to each ``QGridLeaf`` in a
        ``QGrid`` by their index.

        Returns None.
        """
        for leaf in self.leaves:
            leaf.q_event_proxies.sort(key=lambda x: 0 if x.index is None else x.index)

    def subdivide_leaf(
        self,
        leaf: QGridLeaf,
        subdivisions: typing.Sequence[abjad.typings.Duration | int],
    ) -> list[QEventProxy]:
        r"""Replace the ``QGridLeaf`` ``leaf`` contained in a ``QGrid``
        by a ``QGridContainer`` containing ``QGridLeaves`` with durations
        equal to the ratio described in ``subdivisions``

        Returns the ``QEventProxies`` attached to ``leaf``.
        """
        container = QGridContainer(
            preprolated_duration=leaf.preprolated_duration,
            children=[
                QGridLeaf(preprolated_duration=abjad.Duration(subdivision))
                for subdivision in subdivisions
            ],
        )
        if leaf.parent is not None:
            index = leaf.parent.index(leaf)
            leaf.parent[index] = [container]
        # otherwise, our root node if just a QGridLeaf
        else:
            self._root_node = container
        return leaf.q_event_proxies

    def subdivide_leaves(
        self, pairs: typing.Sequence[tuple[int, tuple[int, int]]]
    ) -> list[QEventProxy]:
        r"""Given a sequence of leaf-index:subdivision-ratio pairs ``pairs``,
        subdivide the ``QGridLeaves`` described by the indices into
        ``QGridContainers`` containing ``QGridLeaves`` with durations
        equal to their respective subdivision-ratios.

        Returns the ``QEventProxies`` attached to thus subdivided
        ``QGridLeaf``.
        """
        pairs = sorted(dict(pairs).items())
        leaf_indices = [pair[0] for pair in pairs]
        subdivisions = [pair[1] for pair in pairs]

        all_leaves = self.leaves
        leaves_to_subdivide = [all_leaves[idx] for idx in leaf_indices]

        q_event_proxies = []
        for i, leaf in enumerate(leaves_to_subdivide):
            next_leaf = all_leaves[all_leaves.index(leaf) + 1]
            if next_leaf is self.next_downbeat:
                next_leaf_offset = abjad.Offset(1)
            else:
                next_leaf_offset = next_leaf.start_offset

            q_event_proxies.extend(self.subdivide_leaf(leaf, subdivisions[i]))
            for q_event_proxy in tuple(next_leaf.q_event_proxies):
                if q_event_proxy.offset < next_leaf_offset:
                    idx = next_leaf.q_event_proxies.index(q_event_proxy)
                    q_event_proxies.append(next_leaf.q_event_proxies.pop(idx))

        return q_event_proxies

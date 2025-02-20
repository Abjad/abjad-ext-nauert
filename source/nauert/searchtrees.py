import abc
import copy

import abjad

from . import qgrid as _qgrid


class SearchTree(abc.ABC):
    """
    Abstract search tree.

    ``SearchTrees`` encapsulate strategies for generating collections of
    ``QGrids``, given a set of ``QEventProxy`` instances as input.

    They allow composers to define the degree and quality of nested rhythmic
    subdivisions in the quantization output.  That is to say, they allow
    composers to specify what sorts of tuplets and ratios of pulses may be
    contained within other tuplets, to arbitrary levels of nesting.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_definition",)

    ### INITIALIZER ###

    def __init__(self, definition: dict | None = None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self._is_valid_definition(definition)
        self._definition = definition

    ### SPECIAL METHODS ###

    def __call__(self, q_grid: _qgrid.QGrid) -> list[_qgrid.QGrid]:
        """
        Calls search tree.
        """
        assert isinstance(q_grid, _qgrid.QGrid)
        new_q_grids = []
        commands = self._generate_all_subdivision_commands(q_grid)
        for command in commands:
            new_q_grid = copy.deepcopy(q_grid)
            q_events = new_q_grid.subdivide_leaves(command)
            new_q_grid.fit_q_events(q_events)
            new_q_grids.append(new_q_grid)
        return new_q_grids

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a search tree with definition equal to that of
        this search tree. Otherwise false.
        """
        if type(self) is type(argument):
            if self.definition == argument.definition:
                return True
        return False

    def __hash__(self) -> int:
        """
        Hashes search tree.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(SearchTree, self).__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return f"{type(self).__name__}(definition={self.definition!r})"

    ### PRIVATE METHODS ###

    def _find_divisible_leaf_indices_and_subdivisions(
        self, q_grid: _qgrid.QGrid
    ) -> tuple[list[int], list[tuple[tuple[int, ...], ...]]]:
        # TODO: This should actually check for all QEvents which fall
        # within the leaf's duration,
        # including QEvents attached to the next leaf
        # It may be prudent to actually store QEvents in two lists:
        # before_offset and after_offset
        indices, subdivisions = [], []
        leaves = list(q_grid.leaves)
        i = 0
        for leaf_one, leaf_two in abjad.sequence.nwise(leaves):
            if leaf_one.is_divisible:
                succeeding_proxies = leaf_one.succeeding_q_event_proxies
                preceding_proxies = leaf_two.preceding_q_event_proxies
                if not preceding_proxies and all(
                    proxy.offset == leaf_one.start_offset
                    for proxy in succeeding_proxies
                ):
                    # proxies align perfectly with this leaf
                    pass
                elif preceding_proxies or succeeding_proxies:
                    parentage_ratios = leaf_one._get_parentage_ratios()
                    leaf_subdivisions = self._find_leaf_subdivisions(parentage_ratios)
                    if leaf_subdivisions:
                        indices.append(i)
                        subdivisions.append(tuple(leaf_subdivisions))
            i += 1
        return indices, subdivisions

    @abc.abstractmethod
    def _find_leaf_subdivisions(
        self, parentage_ratios: tuple
    ) -> tuple[tuple[int, ...], ...]:
        raise NotImplementedError

    def _generate_all_subdivision_commands(
        self, q_grid: _qgrid.QGrid
    ) -> tuple[tuple[tuple[int, tuple[int, int]], ...], ...]:
        indices, subdivisions = self._find_divisible_leaf_indices_and_subdivisions(
            q_grid
        )
        if not indices:
            return ()
        combinations = abjad.enumerate.outer_product(subdivisions)
        combinations = [tuple(_) for _ in combinations]
        return tuple(tuple(zip(indices, combo)) for combo in combinations)

    @abc.abstractmethod
    def _is_valid_definition(self, definition: dict) -> bool:
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def default_definition(self) -> dict:
        """
        Gets default search tree definition.
        """
        raise NotImplementedError

    @property
    def definition(self) -> dict:
        """
        Gets search tree definition.
        """
        return self._definition


class UnweightedSearchTree(SearchTree):
    r"""
    Unweighted search tree based on Paul Nauert's model.

    ..  container:: example

        >>> import pprint
        >>> search_tree = nauert.UnweightedSearchTree()
        >>> pprint.pprint(search_tree.definition)
        {2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
            3: {2: {2: None}, 3: None, 5: None},
            5: {2: None, 3: None},
            7: {2: None},
            11: None,
            13: None}

    ..  container:: example

        The search tree defines how nodes in a ``QGrid`` may be subdivided, if
        they happen to contain ``QEvents`` (or, in actuality, ``QEventProxy``
        instances which reference ``QEvents``, but rescale their offsets
        between ``0`` and ``1``).

        In the default definition, the root node of the ``QGrid`` may be
        subdivided into ``2``, ``3``, ``5``, ``7``, ``11`` or ``13`` equal
        parts. If divided into ``2`` parts, the divisions of the root node may
        be divided again into ``2``, ``3``, ``5`` or ``7``, and so forth.

        This definition is structured as a collection of nested dictionaries,
        whose keys are integers, and whose values are either the sentinel
        ``None`` indicating no further permissable divisions, or dictionaries
        obeying these same rules, which then indicate the possibilities for
        further division.

        Calling a ``UnweightedSearchTree`` with a ``QGrid`` instance will
        generate all permissable subdivided ``QGrids``, according to the
        definition of the called search tree:

        >>> q_event_a = nauert.PitchedQEvent(abjad.Offset(130), [0, 1, 4])
        >>> q_event_b = nauert.PitchedQEvent(abjad.Offset(150), [2, 3, 5])
        >>> proxy_a = nauert.QEventProxy(q_event_a, abjad.Offset(0.5))
        >>> proxy_b = nauert.QEventProxy(q_event_b, abjad.Offset(0.667))
        >>> q_grid = nauert.QGrid()
        >>> q_grid.fit_q_events([proxy_a, proxy_b])
        >>> q_grids = search_tree(q_grid)
        >>> for grid in q_grids:
        ...     print(grid.rtm_format)
        (1 (1 1))
        (1 (1 1 1))
        (1 (1 1 1 1 1))
        (1 (1 1 1 1 1 1 1))
        (1 (1 1 1 1 1 1 1 1 1 1 1))
        (1 (1 1 1 1 1 1 1 1 1 1 1 1 1))

    ..  container:: example

        A custom ``UnweightedSearchTree`` may be defined by passing in a
        dictionary, as described above. The following search tree only permits
        divisions of the root node into ``2s`` and ``3s``, and if divided into
        ``2``, a node may be divided once more into ``2`` parts:

        >>> definition = {2: {2: None}, 3: None}
        >>> search_tree = nauert.UnweightedSearchTree(definition)

        >>> q_grids = search_tree(q_grid)
        >>> for grid in q_grids:
        ...     print(grid.rtm_format)
        (1 (1 1))
        (1 (1 1 1))

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _find_leaf_subdivisions(
        self, parentage_ratios: tuple
    ) -> tuple[tuple[int, ...], ...]:
        parentage = [x[1] for x in parentage_ratios[1:]]
        if not parentage:
            return tuple((1,) * x for x in sorted(self._definition.keys()))
        node = self._definition[parentage[0]]
        for item in parentage[1:]:
            node = node[item]
            if node is None:
                return ()
        if node is None:
            return ()
        return tuple((1,) * x for x in sorted(node.keys()))

    def _is_valid_definition(self, definition: dict) -> bool:
        def recurse(n):
            results = []
            for key in n:
                if (
                    not isinstance(key, int)
                    or not 0 < key
                    or not abjad.math.divisors(key) == [1, key]
                ):
                    results.append(False)
                elif not isinstance(n[key], (dict, type(None))):
                    results.append(False)
                elif isinstance(n[key], dict) and not recurse(n[key]):
                    results.append(False)
                else:
                    results.append(True)
            return results

        if not isinstance(definition, dict) or not len(definition):
            return False
        return all(recurse(definition))

    ### PUBLIC PROPERTIES ###

    @property
    def default_definition(self) -> dict:
        """
        The default search tree definition, based on the search tree given by
        Paul Nauert:

        >>> import pprint
        >>> search_tree = nauert.UnweightedSearchTree()
        >>> pprint.pprint(search_tree.default_definition)
        {2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
            3: {2: {2: None}, 3: None, 5: None},
            5: {2: None, 3: None},
            7: {2: None},
            11: None,
            13: None}

        """
        return {
            2: {  # 1/2
                2: {2: {2: None}, 3: None},  # 1/4  # 1/8  # 1/16  # 1/12
                3: None,  # 1/6
                5: None,  # 1/10
                7: None,  # 1/14
            },
            3: {2: {2: None}, 3: None, 5: None},  # 1/3  # 1/6  # 1/12  # 1/9  # 1/15
            5: {2: None, 3: None},  # 1/5  # 1/10  # 1/15
            7: {2: None},  # 1/7  # 1/14
            11: None,  # 1/11
            13: None,  # 1/13
        }


class WeightedSearchTree(SearchTree):
    r"""
    Weighted search tree.

    ..  container:: example

        Allows for dividing nodes in a q-grid into parts with unequal weights.

        >>> search_tree = nauert.WeightedSearchTree()
        >>> search_tree.definition
        {'divisors': (2, 3, 5, 7), 'max_depth': 3, 'max_divisions': 2}

    ..  container:: example

        In ``WeightedSearchTree``'s definition:

            * ``divisors`` controls the sum of the parts of the ratio a node
                may be divided into,
            * ``max_depth`` controls how many levels of tuplet nesting
                are permitted, and
            * ``max_divisions`` controls the maximum permitted length of the
                weights in the ratio.

        Thus, the default ``WeightedSearchTree`` permits the following ratios:

        >>> for composition in search_tree.all_compositions:
        ...     composition
        ...
        (1, 1)
        (2, 1)
        (1, 2)
        (4, 1)
        (3, 2)
        (2, 3)
        (1, 4)
        (6, 1)
        (5, 2)
        (4, 3)
        (3, 4)
        (2, 5)
        (1, 6)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_all_compositions", "_compositions", "_definition")

    ### INITIALIZER ###

    def __init__(self, definition: dict | None = None):
        SearchTree.__init__(self, definition)
        self._compositions = self._precompute_compositions()
        all_compositions = []
        for value in list(self._compositions.values()):
            all_compositions.extend(value)
        self._all_compositions = tuple(all_compositions)

    ### PRIVATE METHODS ###

    def _find_leaf_subdivisions(
        self, parentage_ratios: tuple
    ) -> tuple[tuple[int, ...], ...]:
        if len(parentage_ratios[1:]) < self._definition["max_depth"]:
            return self._all_compositions
        return ()

    def _is_valid_definition(self, definition: dict) -> bool:
        if not isinstance(definition, dict):
            return False
        elif "divisors" not in definition:
            return False
        elif not len(definition["divisors"]):
            return False
        elif not all(isinstance(x, int) and 1 < x for x in definition["divisors"]):
            return False
        elif not all(abjad.math.divisors(x) == [1, x] for x in definition["divisors"]):
            return False
        elif "max_depth" not in definition:
            return False
        elif not isinstance(definition["max_depth"], int):
            return False
        elif not 0 < definition["max_depth"]:
            return False
        elif "max_divisions" not in definition:
            return False
        elif not isinstance(definition["max_divisions"], int):
            return False
        elif not 1 < definition["max_divisions"]:
            return False
        return True

    def _precompute_compositions(
        self,
    ) -> dict[int, list[tuple[int, ...]]]:
        compositions = {}
        max_divisions = self._definition["max_divisions"]
        for divisor in self._definition["divisors"]:
            compositions[divisor] = [
                tuple(x)
                for x in abjad.math.yield_all_compositions_of_integer(divisor)
                if 1 < len(x) <= max_divisions
            ]
        return compositions

    ### PUBLIC PROPERTIES ###

    @property
    def all_compositions(self) -> tuple[tuple[int, ...], ...]:
        """
        Gets all compositions of weighted search tree.
        """
        return self._all_compositions

    @property
    def default_definition(self) -> dict:
        """
        Gets default definition of weighted search tree.
        """
        return {"divisors": (2, 3, 5, 7), "max_depth": 3, "max_divisions": 2}

import typing

import abjad

from .qeventproxy import QEventProxy
from .qgrid import QGrid
from .searchtrees import SearchTree, UnweightedSearchTree


class QuantizationJob:
    r"""Quantization job.

    Copiable, picklable class for generating all ``QGrids`` which are valid
    under a given ``SearchTree`` for a sequence of ``QEventProxies``.

    ..  container:: example

        >>> q_event_a = nauert.PitchedQEvent(250, [0, 1])
        >>> q_event_b = nauert.SilentQEvent(500)
        >>> q_event_c = nauert.PitchedQEvent(750, [3, 7])
        >>> proxy_a = nauert.QEventProxy(q_event_a, 0.25)
        >>> proxy_b = nauert.QEventProxy(q_event_b, 0.5)
        >>> proxy_c = nauert.QEventProxy(q_event_c, 0.75)

        >>> definition = {2: {2: None}, 3: None, 5: None}
        >>> search_tree = nauert.UnweightedSearchTree(definition)

        >>> job = nauert.QuantizationJob(
        ...     1, search_tree, [proxy_a, proxy_b, proxy_c])

    ..  container:: example

        ``QuantizationJob`` generates ``QGrids`` when called, and stores those
        ``QGrids`` on its ``q_grids`` attribute, allowing them to be recalled
        later, even if pickled:

        >>> job()
        >>> for q_grid in job.q_grids:
        ...     print(q_grid.rtm_format)
        1
        (1 (1 1 1 1 1))
        (1 (1 1 1))
        (1 (1 1))
        (1 ((1 (1 1)) (1 (1 1))))

    ``QuantizationJob`` is intended to be useful in multiprocessing-enabled
    environments.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_job_id", "_q_event_proxies", "_q_grids", "_search_tree")

    ### INITIALIZER ###

    def __init__(self, job_id=1, search_tree=None, q_event_proxies=None, q_grids=None):
        search_tree = search_tree or UnweightedSearchTree()
        q_event_proxies = q_event_proxies or []
        assert isinstance(search_tree, SearchTree)
        assert all(isinstance(x, QEventProxy) for x in q_event_proxies)
        self._job_id = job_id
        self._search_tree = search_tree
        self._q_event_proxies = tuple(q_event_proxies)
        if q_grids is None:
            self._q_grids = ()
        else:
            assert all(isinstance(x, QGrid) for x in q_grids)
            self._q_grids = tuple(q_grids)

    ### SPECIAL METHODS ###

    def __call__(self):
        r"""Calls quantization job.

        Returns none.
        """
        # print('XXX')
        # print(format(self.q_event_proxies[0]))

        q_grid = QGrid()
        q_grid.fit_q_events(self.q_event_proxies)

        # print(format(q_grid))

        old_q_grids = []
        new_q_grids = [q_grid]

        while new_q_grids:
            q_grid = new_q_grids.pop()
            search_results = self.search_tree(q_grid)
            # print q_grid.rtm_format
            # for x in search_results:
            #    print '\t', x.rtm_format
            new_q_grids.extend(search_results)
            old_q_grids.append(q_grid)

        # for q_grid in old_q_grids:
        #    print('\t', q_grid)
        # print()

        self._q_grids = tuple(old_q_grids)

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a quantization job with job ID, search tree,
        q-event proxies and q-grids equal to those of this quantization job.
        Otherwise false.
        """
        if type(self) == type(argument):
            if self.job_id == argument.job_id:
                if self.search_tree == argument.search_tree:
                    if self.q_event_proxies == argument.q_event_proxies:
                        if self.q_grids == argument.q_grids:
                            return True
        return False

    def __format__(self, format_specification="") -> str:
        """
        Formats object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes quantization job.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(QuantizationJob, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    ### PUBLIC PROPERTIES ###

    @property
    def job_id(self) -> int:
        """
        The job id of the ``QuantizationJob``.

        Only meaningful when the job is processed via multiprocessing,
        as the job id is necessary to reconstruct the order of jobs.
        """
        return self._job_id

    @property
    def q_event_proxies(self) -> typing.Tuple:
        r"""
        The ``QEventProxies`` the ``QuantizationJob`` was instantiated with.

        >>> q_event_a = nauert.PitchedQEvent(250, [0, 1])
        >>> q_event_b = nauert.SilentQEvent(500)
        >>> q_event_c = nauert.PitchedQEvent(750, [3, 7])
        >>> proxy_a = nauert.QEventProxy(q_event_a, 0.25)
        >>> proxy_b = nauert.QEventProxy(q_event_b, 0.5)
        >>> proxy_c = nauert.QEventProxy(q_event_c, 0.75)

        >>> definition = {2: {2: None}, 3: None, 5: None}
        >>> search_tree = nauert.UnweightedSearchTree(definition)

        >>> job = nauert.QuantizationJob(
        ...     1, search_tree, [proxy_a, proxy_b, proxy_c])
        >>> job()

        >>> for q_event_proxy in job.q_event_proxies:
        ...     string = abjad.storage(q_event_proxy)
        ...     print(string)
        ...
        nauert.QEventProxy(
            nauert.PitchedQEvent(
                offset=abjad.Offset((250, 1)),
                pitches=(
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("cs'"),
                    ),
                ),
            abjad.Offset((1, 4))
            )
        nauert.QEventProxy(
            nauert.SilentQEvent(
                offset=abjad.Offset((500, 1)),
                ),
            abjad.Offset((1, 2))
            )
        nauert.QEventProxy(
            nauert.PitchedQEvent(
                offset=abjad.Offset((750, 1)),
                pitches=(
                    abjad.NamedPitch("ef'"),
                    abjad.NamedPitch("g'"),
                    ),
                ),
            abjad.Offset((3, 4))
            )

        """
        return self._q_event_proxies

    @property
    def q_grids(self) -> typing.Tuple:
        r"""
        The generated ``QGrids``.

        >>> q_event_a = nauert.PitchedQEvent(250, [0, 1])
        >>> q_event_b = nauert.SilentQEvent(500)
        >>> q_event_c = nauert.PitchedQEvent(750, [3, 7])
        >>> proxy_a = nauert.QEventProxy(q_event_a, 0.25)
        >>> proxy_b = nauert.QEventProxy(q_event_b, 0.5)
        >>> proxy_c = nauert.QEventProxy(q_event_c, 0.75)

        >>> definition = {2: {2: None}, 3: None, 5: None}
        >>> search_tree = nauert.UnweightedSearchTree(definition)

        >>> job = nauert.QuantizationJob(
        ...     1, search_tree, [proxy_a, proxy_b, proxy_c])
        >>> job()

        >>> for q_grid in job.q_grids:
        ...     print(q_grid.rtm_format)
        1
        (1 (1 1 1 1 1))
        (1 (1 1 1))
        (1 (1 1))
        (1 ((1 (1 1)) (1 (1 1))))

        """
        return self._q_grids

    @property
    def search_tree(self) -> SearchTree:
        """
        The search tree the ``QuantizationJob`` was instantiated with.
        """
        return self._search_tree

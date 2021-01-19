"""
Extension for quantizing rhythm, based on Paul Nauert's Q-Grid technique.
"""
from ._version import __version__, __version_info__
from .attackpointoptimizers import (
    AttackPointOptimizer,
    MeasurewiseAttackPointOptimizer,
    NaiveAttackPointOptimizer,
    NullAttackPointOptimizer,
)
from .gracehandlers import (
    CollapsingGraceHandler,
    ConcatenatingGraceHandler,
    DiscardingGraceHandler,
    GraceHandler,
)
from .heuristics import DistanceHeuristic, Heuristic
from .jobhandlers import (
    JobHandler,
    ParallelJobHandler,
    ParallelJobHandlerWorker,
    SerialJobHandler,
)
from .qeventproxy import QEventProxy
from .qevents import PitchedQEvent, QEvent, SilentQEvent, TerminalQEvent
from .qeventsequence import QEventSequence
from .qgrid import QGrid, QGridContainer, QGridLeaf
from .qschemaitems import BeatwiseQSchemaItem, MeasurewiseQSchemaItem, QSchemaItem
from .qschemas import BeatwiseQSchema, MeasurewiseQSchema, QSchema
from .qtargetitems import QTargetBeat, QTargetMeasure
from .qtargets import BeatwiseQTarget, MeasurewiseQTarget, QTarget
from .quantizationjob import QuantizationJob
from .quantizer import Quantizer
from .searchtrees import SearchTree, UnweightedSearchTree, WeightedSearchTree

__all__ = [
    "__version__",
    "__version_info__",
    "AttackPointOptimizer",
    "BeatwiseQSchema",
    "BeatwiseQSchemaItem",
    "BeatwiseQTarget",
    "CollapsingGraceHandler",
    "ConcatenatingGraceHandler",
    "DiscardingGraceHandler",
    "DistanceHeuristic",
    "GraceHandler",
    "Heuristic",
    "JobHandler",
    "MeasurewiseAttackPointOptimizer",
    "MeasurewiseQSchema",
    "MeasurewiseQSchemaItem",
    "MeasurewiseQTarget",
    "NaiveAttackPointOptimizer",
    "NullAttackPointOptimizer",
    "ParallelJobHandler",
    "ParallelJobHandlerWorker",
    "PitchedQEvent",
    "QEvent",
    "QEventProxy",
    "QEventSequence",
    "QGrid",
    "QGridContainer",
    "QGridLeaf",
    "QSchema",
    "QSchemaItem",
    "QTarget",
    "QTargetBeat",
    "QTargetMeasure",
    "QuantizationJob",
    "Quantizer",
    "SearchTree",
    "SerialJobHandler",
    "SilentQEvent",
    "TerminalQEvent",
    "UnweightedSearchTree",
    "WeightedSearchTree",
]

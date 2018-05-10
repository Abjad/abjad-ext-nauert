import abjad
import copy
import abjadext.nauert


def test_QGrid___copy___01():
    q_grid = abjadext.nauert.QGrid()
    copied = copy.deepcopy(q_grid)
    assert format(q_grid) == format(copied)
    assert q_grid != copied
    assert q_grid is not copied
    assert q_grid.root_node is not copied.root_node
    assert q_grid.next_downbeat is not copied.next_downbeat

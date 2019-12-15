import abjad
import abjadext.nauert


def test_QEventProxy___init___01():
    q_event = abjadext.nauert.PitchedQEvent(130, [0])
    proxy = abjadext.nauert.QEventProxy(q_event, 0.5)
    assert proxy.q_event == q_event
    assert proxy.offset == abjad.Offset(1, 2)


def test_QEventProxy___init___02():
    q_event = abjadext.nauert.PitchedQEvent(130, [0, 1, 4])
    proxy = abjadext.nauert.QEventProxy(q_event, 100, 1000)
    assert proxy.q_event == q_event
    assert proxy.offset == abjad.Offset(1, 30)

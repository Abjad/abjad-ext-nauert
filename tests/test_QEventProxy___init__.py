import abjad

import nauert


def test_QEventProxy___init___01():
    q_event = nauert.PitchedQEvent(abjad.Offset(130), [0])
    proxy = nauert.QEventProxy(q_event, abjad.Offset(0.5))
    assert proxy.q_event == q_event
    assert proxy.offset == abjad.Offset(1, 2)


def test_QEventProxy___init___02():
    q_event = nauert.PitchedQEvent(abjad.Offset(130), [0, 1, 4])
    proxy = nauert.QEventProxy(q_event, abjad.Offset(100), abjad.Offset(1000))
    assert proxy.q_event == q_event
    assert proxy.offset == abjad.Offset(1, 30)

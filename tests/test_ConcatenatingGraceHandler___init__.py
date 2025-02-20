import abjad

import nauert


def test_ConcatenatingGraceHandler___init___01():
    grace_handler = nauert.ConcatenatingGraceHandler()
    assert grace_handler.grace_duration == abjad.Duration(1, 16)
    assert grace_handler.discard_grace_rest is True


def test_ConcatenatingGraceHandler___init___02():
    grace_handler = nauert.ConcatenatingGraceHandler(discard_grace_rest=False)
    assert grace_handler.grace_duration == abjad.Duration(1, 16)
    assert grace_handler.discard_grace_rest is False
    assert grace_handler.replace_rest_with_final_grace_note is True


def test_ConcatenatingGraceHandler___init___03():
    duration = abjad.Duration(1, 32)
    grace_handler = nauert.ConcatenatingGraceHandler(grace_duration=duration)
    assert grace_handler.grace_duration == abjad.Duration(1, 32)
    assert grace_handler.discard_grace_rest is True
    assert grace_handler.replace_rest_with_final_grace_note is True


def test_ConcatenatingGraceHandler___init___04():
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=True
    )
    assert grace_handler.grace_duration == abjad.Duration(1, 16)
    assert grace_handler.discard_grace_rest is True
    assert grace_handler.replace_rest_with_final_grace_note is True

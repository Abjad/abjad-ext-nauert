import abjad

import nauert


def test_MeasurewiseAttackPointOptimizer___call___01():
    string = r"""
        \tuplet 11/8
        {
            a''8
            ~
            a''8
            ~
            a''8
            ~
            a''8
            ~
            a''8
            ~
            a''8
            ~
            a''8
            \grace {
                e''16
                e''16
            }
            d''8
            ~
            d''8
            r8
            r8
        }
        """
    string = abjad.string.normalize(string)
    container = abjad.Container(string)
    time_signature = abjad.TimeSignature((4, 4))
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    attack_point_optimizer(container, time_signature)
    string = abjad.lilypond(container)
    assert string == abjad.string.normalize(
        r"""
        {
            \tuplet 11/8
            {
                a''2..
                \grace {
                    e''16
                    e''16
                }
                d''4
                r4
            }
        }
        """
    ), print(string)


def test_annotations_survive_measurewise_attack_point_optimimzer():
    container = abjad.Container("c'8~ c'8 c'8 c'4. c'4")
    abjad.annotate(container[0], "q_event_attachments", "test_indicator_0")
    assert (
        abjad.get.annotation(container[0], "q_event_attachments") == "test_indicator_0"
    )
    abjad.annotate(container[3], "q_event_attachments", "test_indicator_1")
    assert (
        abjad.get.annotation(container[3], "q_event_attachments") == "test_indicator_1"
    )
    time_signature = abjad.TimeSignature((4, 4))
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    attack_point_optimizer(container, time_signature)
    string = abjad.lilypond(container)
    assert string == abjad.string.normalize(
        r"""
        {
            c'4
            c'8
            c'8
            ~
            c'4
            c'4
        }
        """
    )
    assert (
        abjad.get.annotation(container[0], "q_event_attachments") == "test_indicator_0"
    )
    assert (
        abjad.get.annotation(container[2], "q_event_attachments") == "test_indicator_1"
    )


def test_annotations_survive_naive_attack_point_optimimzer():
    container = abjad.Container("c'8~ c'8 c'8 c'4. c'4")
    abjad.annotate(container[0], "test_annotation", "test_indicator")
    assert abjad.get.annotation(container[0], "test_annotation") == "test_indicator"
    attack_point_optimizer = nauert.NaiveAttackPointOptimizer()
    attack_point_optimizer(container)
    string = abjad.lilypond(container)
    assert string == abjad.string.normalize(
        r"""
        {
            c'4
            c'8
            c'4.
            c'4
        }
        """
    )
    assert abjad.get.annotation(container[0], "test_annotation") == "test_indicator"

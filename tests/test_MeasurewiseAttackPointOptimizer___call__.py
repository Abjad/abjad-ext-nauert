import abjad
from abjadext import nauert


def test_MeasurewiseAttackPointOptimizer___call___01():
    string = r"""
        \times 8/11 {
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
    string = abjad.String.normalize(string)
    container = abjad.Container(string)
    time_signature = abjad.TimeSignature((4, 4))
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    attack_point_optimizer(container, time_signature)
    string = abjad.lilypond(container)
    assert string == abjad.String.normalize(
        r"""
        {
            \times 8/11 {
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

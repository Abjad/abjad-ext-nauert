import abjad
import abjadext.nauert


def test_Quantizer___call___01():
    milliseconds = [1500, 1500]
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    quantizer = abjadext.nauert.Quantizer()
    result = quantizer(q_events)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'4.
                        c'4.
                        r4
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___02():
    milliseconds = [750, 750]
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    quantizer = abjadext.nauert.Quantizer()
    optimizer = abjadext.nauert.MeasurewiseAttackPointOptimizer()
    result = quantizer(q_events, attack_point_optimizer=optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'8.
                        c'16
                        ~
                        c'8
                        r8
                        r2
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___03():
    milliseconds = [1500, -1000, 1000, 1000, -1000, 1000, -1000, 500]
    sequence = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = abjadext.nauert.NullAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()

    result = quantizer(sequence, attack_point_optimizer=attack_point_optimizer)

    assert isinstance(result, abjad.Voice)
    assert abjad.get.duration(result) == 2

    score = abjad.Score([abjad.Staff([result])])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \new Voice
                {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'4
                        ~
                        c'8
                        r8
                        r8
                        c'8
                        ~
                        c'8
                        c'8
                        ~
                    }
                    {
                        c'8
                        r8
                        r8
                        c'8
                        ~
                        c'8
                        r8
                        r8
                        c'8
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___04():
    milliseconds = [250, 1000, 1000, 1000, 750]
    sequence = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = abjadext.nauert.NullAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()
    result = quantizer(sequence, attack_point_optimizer=attack_point_optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'16
                        c'16
                        ~
                        c'8
                        ~
                        c'16
                        c'16
                        ~
                        c'8
                        ~
                        c'16
                        c'16
                        ~
                        c'8
                        ~
                        c'16
                        c'16
                        ~
                        c'8
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___05():
    q_schema = abjadext.nauert.BeatwiseQSchema(
        {"search_tree": abjadext.nauert.UnweightedSearchTree({2: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({3: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({5: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = abjadext.nauert.NullAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()

    result = quantizer(
        q_events,
        q_schema=q_schema,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \grace {
                        c'16
                    }
                    \tempo 4=60
                    c'8
                    \grace {
                        c'16
                    }
                    c'8
                    \times 2/3
                    {
                        c'8
                        \grace {
                            c'16
                        }
                        c'8
                        c'8
                    }
                    \times 4/5
                    {
                        c'16
                        c'16
                        c'16
                        ~
                        c'16
                        c'16
                    }
                    \times 4/7
                    {
                        c'16
                        ~
                        c'16
                        c'16
                        c'16
                        ~
                        c'16
                        c'16
                        ~
                        c'16
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___06():
    milliseconds = [1000] * 8
    sequence = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = abjadext.nauert.MeasurewiseAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()
    result = quantizer(sequence, attack_point_optimizer=optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                    {
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___07():
    milliseconds = [1000, 750, 1000, 1250] * 2
    sequence = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = abjadext.nauert.MeasurewiseAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()
    result = quantizer(sequence, attack_point_optimizer=optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'4
                        c'8.
                        c'16
                        ~
                        c'8.
                        c'16
                        ~
                        c'4
                    }
                    {
                        c'4
                        c'8.
                        c'16
                        ~
                        c'8.
                        c'16
                        ~
                        c'4
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___08():
    q_schema = abjadext.nauert.BeatwiseQSchema(
        {"search_tree": abjadext.nauert.UnweightedSearchTree({2: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({3: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({5: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = abjadext.nauert.NaiveAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()

    result = quantizer(
        q_events,
        q_schema=q_schema,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \grace {
                        c'16
                    }
                    \tempo 4=60
                    c'8
                    \grace {
                        c'16
                    }
                    c'8
                    \times 2/3
                    {
                        c'8
                        \grace {
                            c'16
                        }
                        c'8
                        c'8
                    }
                    \times 4/5
                    {
                        c'16
                        c'16
                        c'8
                        c'16
                    }
                    \times 4/7
                    {
                        c'8
                        c'16
                        c'8
                        c'8
                    }
                }
            }
        >>
        """
    ), print(abjad.lilypond(score))


def test_Quantizer___call___09():
    q_schema = abjadext.nauert.BeatwiseQSchema(
        {"search_tree": abjadext.nauert.UnweightedSearchTree({2: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({3: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({5: None})},
        {"search_tree": abjadext.nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = abjadext.nauert.MeasurewiseAttackPointOptimizer()
    quantizer = abjadext.nauert.Quantizer()

    try:
        quantizer(
            q_events,
            q_schema=q_schema,
            attack_point_optimizer=attack_point_optimizer,
        )
        assert False
    except TypeError as error:
        assert (
            str(error)
            == "BeatwiseQTarget is not supposed to be used together with MeasurewiseAttackPointOptimizer."
        )

import abjad
from abjadext import nauert


def test_Quantizer___call___01():
    milliseconds = [1500, 1500]
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    quantizer = nauert.Quantizer()
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
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    quantizer = nauert.Quantizer()
    optimizer = nauert.MeasurewiseAttackPointOptimizer()
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
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NullAttackPointOptimizer()
    quantizer = nauert.Quantizer()

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
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NullAttackPointOptimizer()
    quantizer = nauert.Quantizer()
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
    q_schema = nauert.BeatwiseQSchema(
        {"search_tree": nauert.UnweightedSearchTree({2: None})},
        {"search_tree": nauert.UnweightedSearchTree({3: None})},
        {"search_tree": nauert.UnweightedSearchTree({5: None})},
        {"search_tree": nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NullAttackPointOptimizer()
    quantizer = nauert.Quantizer()

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
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = nauert.MeasurewiseAttackPointOptimizer()
    quantizer = nauert.Quantizer()
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
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = nauert.MeasurewiseAttackPointOptimizer()
    quantizer = nauert.Quantizer()
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
    q_schema = nauert.BeatwiseQSchema(
        {"search_tree": nauert.UnweightedSearchTree({2: None})},
        {"search_tree": nauert.UnweightedSearchTree({3: None})},
        {"search_tree": nauert.UnweightedSearchTree({5: None})},
        {"search_tree": nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NaiveAttackPointOptimizer()
    quantizer = nauert.Quantizer()

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
    q_schema = nauert.BeatwiseQSchema(
        {"search_tree": nauert.UnweightedSearchTree({2: None})},
        {"search_tree": nauert.UnweightedSearchTree({3: None})},
        {"search_tree": nauert.UnweightedSearchTree({5: None})},
        {"search_tree": nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    quantizer = nauert.Quantizer()

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


def test_Quantizer___call___10():
    quantizer = nauert.Quantizer()
    durations = [1000, 1000, 1000, 2000, 1000, 1000, 500, 500]
    pitches = range(8)
    pitches = [(x, x + 7) for x in pitches]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=True
    )
    result = quantizer(q_event_sequence, grace_handler=grace_handler)
    string = abjad.lilypond(result)
    assert string == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                \tempo 4=60
                %%% \time 4/4 %%%
                <c' g'>4
                <cs' af'>4
                <d' a'>4
                <ef' bf'>4
                ~
            }
            {
                <ef' bf'>4
                <e' b'>4
                <f' c''>4
                <fs' cs''>8
                <g' d''>8
            }
        }
        """
    ), print(string)


def test_Quantizer___call___11():
    quantizer = nauert.Quantizer()
    durations = [250, 1250, 750, 1000, 250]
    pitches = range(5)
    pitches = [(x, x + 7) for x in pitches]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    time_signature = abjad.TimeSignature((7, 8))
    search_tree = nauert.UnweightedSearchTree(
        definition={
            2: {2: None, 3: None},
            3: {2: None, 3: None},
            5: {2: None},
            7: {2: None},
            13: None,
        }
    )
    q_schema = nauert.MeasurewiseQSchema(
        time_signature=abjad.TimeSignature((7, 8)),
        search_tree=search_tree,
        use_full_measure=True,
    )
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=True
    )
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    result = quantizer(
        q_event_sequence,
        q_schema=q_schema,
        grace_handler=grace_handler,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result])
    string = abjad.lilypond(staff)
    assert string == abjad.String.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \tempo 4=60
                    \time 7/8
                    <c' g'>16
                    <cs' af'>16
                    ~
                    <cs' af'>4
                    <d' a'>8.
                    <ef' bf'>16
                    ~
                    <ef' bf'>8.
                    <e' b'>16
                }
            }
        }
        """
    ), print(string)

import abjad

import nauert


def assert_q_event_attachments(result, all_attachments):
    for logical_tie, attachments in zip(
        abjad.iterate.logical_ties(result, pitched=True), all_attachments
    ):
        first_leaf = abjad.get.leaf(logical_tie, 0)
        q_event_attachments = abjad.get.annotation(first_leaf, "q_event_attachments")
        assert q_event_attachments == attachments, print(q_event_attachments)


def test_quantize_01():
    milliseconds = [1500, 1500]
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    result = nauert.quantize(q_events)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])
    assert abjad.lilypond(score) == abjad.string.normalize(
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


def test_Quantize_02():
    milliseconds = [750, 750]
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = nauert.MeasurewiseAttackPointOptimizer()
    result = nauert.quantize(q_events, attack_point_optimizer=optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])
    assert abjad.lilypond(score) == abjad.string.normalize(
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


def test_Quantize_03():
    milliseconds = [1500, -1000, 1000, 1000, -1000, 1000, -1000, 500]
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NullAttackPointOptimizer()

    result = nauert.quantize(sequence, attack_point_optimizer=attack_point_optimizer)

    assert isinstance(result, abjad.Voice)
    assert abjad.get.duration(result) == 2

    score = abjad.Score([abjad.Staff([result])])

    assert abjad.lilypond(score) == abjad.string.normalize(
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


def test_Quantize_04():
    milliseconds = [250, 1000, 1000, 1000, 750]
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NullAttackPointOptimizer()
    result = nauert.quantize(sequence, attack_point_optimizer=attack_point_optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.string.normalize(
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


def test_Quantize_05():
    q_schema = nauert.BeatwiseQSchema(
        {"search_tree": nauert.UnweightedSearchTree({2: None})},
        {"search_tree": nauert.UnweightedSearchTree({3: None})},
        {"search_tree": nauert.UnweightedSearchTree({5: None})},
        {"search_tree": nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NullAttackPointOptimizer()

    result = nauert.quantize(
        q_events,
        q_schema=q_schema,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.string.normalize(
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
                    \tuplet 3/2
                    {
                        c'8
                        \grace {
                            c'16
                        }
                        c'8
                        c'8
                    }
                    \tuplet 5/4
                    {
                        c'16
                        c'16
                        c'16
                        ~
                        c'16
                        c'16
                    }
                    \tuplet 7/4
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


def test_Quantize_06():
    milliseconds = [1000] * 8
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = nauert.MeasurewiseAttackPointOptimizer()
    result = nauert.quantize(sequence, attack_point_optimizer=optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.string.normalize(
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


def test_Quantize_07():
    milliseconds = [1000, 750, 1000, 1250] * 2
    sequence = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    optimizer = nauert.MeasurewiseAttackPointOptimizer()
    result = nauert.quantize(sequence, attack_point_optimizer=optimizer)
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.string.normalize(
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


def test_Quantize_08():
    q_schema = nauert.BeatwiseQSchema(
        {"search_tree": nauert.UnweightedSearchTree({2: None})},
        {"search_tree": nauert.UnweightedSearchTree({3: None})},
        {"search_tree": nauert.UnweightedSearchTree({5: None})},
        {"search_tree": nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.NaiveAttackPointOptimizer()

    result = nauert.quantize(
        q_events,
        q_schema=q_schema,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result], lilypond_type="RhythmicStaff")
    score = abjad.Score([staff])

    assert abjad.lilypond(score) == abjad.string.normalize(
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
                    \tuplet 3/2
                    {
                        c'8
                        \grace {
                            c'16
                        }
                        c'8
                        c'8
                    }
                    \tuplet 5/4
                    {
                        c'16
                        c'16
                        c'8
                        c'16
                    }
                    \tuplet 7/4
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


def test_Quantize_09():
    q_schema = nauert.BeatwiseQSchema(
        {"search_tree": nauert.UnweightedSearchTree({2: None})},
        {"search_tree": nauert.UnweightedSearchTree({3: None})},
        {"search_tree": nauert.UnweightedSearchTree({5: None})},
        {"search_tree": nauert.UnweightedSearchTree({7: None})},
    )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = nauert.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()

    try:
        nauert.quantize(
            q_events,
            q_schema=q_schema,
            attack_point_optimizer=attack_point_optimizer,
        )
        assert False
    except TypeError as error:
        string = "BeatwiseQTarget is not supposed to be used together"
        string += " with MeasurewiseAttackPointOptimizer."
        assert str(error) == string


def test_Quantize_10():
    durations = [1000, 1000, 1000, 2000, 1000, 1000, 500, 500]
    pitches = range(8)
    all_attachments = [(x,) for x in pitches]
    pitches = [(x, x + 7) for x in pitches]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(
        tuple(zip(durations, pitches, all_attachments))
    )
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=True
    )
    result = nauert.quantize(q_event_sequence, grace_handler=grace_handler)
    string = abjad.lilypond(result)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                %%% \time 4/4 %%%
                \tempo 4=60
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
    assert_q_event_attachments(result, all_attachments)


def test_Quantize_11():
    durations = [250, 1250, 750, 1000, 250]
    pitches = range(5)
    all_attachments = [(x,) for x in pitches]
    pitches = [(x, x + 7) for x in pitches]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(
        tuple(zip(durations, pitches, all_attachments))
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
        time_signature=time_signature,
        search_tree=search_tree,
        use_full_measure=True,
    )
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=True
    )
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    result = nauert.quantize(
        q_event_sequence,
        q_schema=q_schema,
        grace_handler=grace_handler,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result])
    abjad.Score([staff], name="Score")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
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
    assert_q_event_attachments(result, all_attachments)


def test_Quantize_12():
    definition = {"divisors": (2, 3, 5, 7), "max_depth": 2, "max_divisions": 2}
    search_tree = nauert.WeightedSearchTree(definition=definition)
    durations = [457.14285, 814.1, 228.5714, 1440, 960]
    pitches = range(len(durations))
    all_attachments = [(x,) for x in pitches]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(
        tuple(zip(durations, pitches, all_attachments))
    )
    q_schema = nauert.MeasurewiseQSchema(
        search_tree=search_tree, time_signature=(7, 8), use_full_measure=True
    )
    result = nauert.quantize(q_event_sequence, q_schema=q_schema, attach_tempos=True)
    staff = abjad.Staff([result])
    abjad.Score([staff], name="Score")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        \tempo 4=60
                        \time 7/8
                        c'8
                        cs'4
                        ~
                        cs'16
                    }
                    \tuplet 7/4
                    {
                        \grace {
                            d'16
                        }
                        ef'2
                        ~
                        ef'8
                        e'4
                        ~
                    }
                }
                {
                    \tuplet 5/4
                    {
                        e'8
                        r32
                    }
                    r2.
                }
            }
        }
        """
    ), print(string)
    assert_q_event_attachments(result, all_attachments)


def test_Quantize_13():
    definition = {"divisors": (2, 3, 5, 7), "max_depth": 2, "max_divisions": 2}
    search_tree = nauert.WeightedSearchTree(definition=definition)
    durations = [400, 1000, 1260, 840, 20, 610, 420, 2450, 3500]
    pitches = range(len(durations))
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    q_schema = nauert.MeasurewiseQSchema(
        search_tree=search_tree, time_signature=(7, 8), use_full_measure=True
    )
    result = nauert.quantize(q_event_sequence, q_schema=q_schema, attach_tempos=True)
    staff = abjad.Staff([result])
    abjad.Score([staff], name="Score")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 10/7
                    {
                        \tuplet 7/4
                        {
                            \tempo 4=60
                            \time 7/8
                            c'4
                            cs'2
                            ~
                            cs'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 5/3
                        {
                            d'2.
                            ef'2
                        }
                    }
                }
                {
                    \tuplet 5/4
                    {
                        \grace {
                            e'16
                        }
                        f'8.
                        fs'8
                    }
                    g'2
                    ~
                    g'8
                }
                {
                    af'2..
                }
            }
        }
        """
    ), print(string)


def test_Quantize_14():
    definition = {"divisors": (2, 3, 5, 7), "max_depth": 2, "max_divisions": 2}
    search_tree = nauert.WeightedSearchTree(definition=definition)
    durations = [1000, 1000, 1000, 400, 50, 50, 3500]
    pitches = range(len(durations))
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    q_schema = nauert.MeasurewiseQSchema(
        search_tree=search_tree, time_signature=(7, 8), use_full_measure=True
    )
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    result = nauert.quantize(
        q_event_sequence,
        q_schema=q_schema,
        attack_point_optimizer=attack_point_optimizer,
        attach_tempos=True,
    )
    staff = abjad.Staff([result])
    abjad.Score([staff], name="Score")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \tempo 4=60
                    \time 7/8
                    c'4
                    cs'8
                    ~
                    cs'8
                    d'8
                    ~
                    d'8
                    ef'8
                }
                {
                    \grace {
                        e'16
                        f'16
                    }
                    fs'2..
                }
            }
        }
        """
    ), print(string)


def test_Quantize_15():
    durations = [1000, 1000, 1000, 400, 50, 50]
    pitches = range(len(durations))

    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    search_tree = nauert.UnweightedSearchTree()
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    q_schema = nauert.MeasurewiseQSchema(
        search_tree=search_tree, time_signature=(7, 8), use_full_measure=True
    )

    result = nauert.quantize(
        q_event_sequence,
        q_schema=q_schema,
        attach_tempos=True,
        attack_point_optimizer=attack_point_optimizer,
    )

    staff = abjad.Staff([result])
    abjad.Score([staff], name="Score")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \tempo 4=60
                    \time 7/8
                    c'4
                    cs'8
                    ~
                    cs'8
                    d'8
                    ~
                    d'8
                    \afterGrace
                    ef'8
                    {
                        e'16
                        f'16
                    }
                }
            }
        }
        """
    ), print(string)


def test_Quantize_16():
    durations = [1546, 578, 375, 589, 144, 918, 137]
    pitches = list(range(len(durations)))
    pitches[0] = None
    all_attachments = [(x,) for x in pitches]
    all_attachments[0] = ()
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(
        tuple(zip(durations, pitches, all_attachments))
    )
    definition = {"divisors": (2, 3, 5, 7), "max_depth": 2, "max_divisions": 2}
    search_tree = nauert.WeightedSearchTree(definition=definition)
    attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
    q_schema = nauert.MeasurewiseQSchema(
        search_tree=search_tree,
        tempo=abjad.MetronomeMark(abjad.Duration(1, 4), 72),
        time_signature=(7, 8),
        use_full_measure=True,
    )
    result = nauert.quantize(
        q_event_sequence,
        q_schema=q_schema,
        attach_tempos=True,
        attack_point_optimizer=attack_point_optimizer,
    )
    staff = abjad.Staff([result])
    abjad.Score([staff], name="Score")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/5
                    {
                        \tempo 4=72
                        \time 7/8
                        r4.
                        r4
                        cs'4
                    }
                    d'8
                    ef'8
                    ~
                }
                {
                    \tuplet 5/4
                    {
                        ef'16
                        e'32
                        ~
                        e'16
                    }
                    f'4
                    fs'2
                }
            }
        }
        """
    ), print(string)
    assert_q_event_attachments(result, all_attachments[1:])

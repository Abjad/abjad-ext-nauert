\version "2.19.83"
\language "english"
\score
{
    \new Score
    <<
        \new Staff
        {
            \new Voice
            {
                {
                    \tempo 4=78
                    \time 2/4
                    c'4
                    ~
                    \tuplet 5/4
                    {
                        c'16.
                        cs'8..
                        ~
                    }
                }
                {
                    \tuplet 7/4
                    {
                        \tempo 8=57
                        \time 5/4
                        cs'16.
                        d'8
                        ~
                    }
                    \tuplet 5/4
                    {
                        d'16
                        ef'16.
                        ~
                    }
                    \tuplet 3/2
                    {
                        ef'16
                        e'8
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'16
                        f'8
                        ~
                        f'32
                        ~
                    }
                    f'32
                    fs'16.
                    ~
                    \tuplet 5/4
                    {
                        fs'32
                        g'8
                        ~
                    }
                    \tuplet 7/4
                    {
                        g'32
                        r32
                        r16
                        r16
                        r16
                        r16
                        r16
                        r16
                    }
                    r4
                }
            }
        }
    >>
}
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
                    \tempo 4=54
                    \time 4/4
                    c'16..
                    d'64
                    ~
                    \tuplet 5/4
                    {
                        d'8
                        e'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'8
                        ~
                        e'32
                        f'16
                        ~
                    }
                    \tuplet 5/4
                    {
                        f'16.
                        g'16
                        ~
                    }
                    g'16
                    a'16
                    ~
                    \tuplet 5/4
                    {
                        a'16
                        b'16.
                        ~
                    }
                    \tuplet 7/4
                    {
                        b'16
                        c''8
                        ~
                        c''32
                        ~
                    }
                    \tuplet 5/4
                    {
                        c''32
                        r32
                        r32
                        r32
                        r32
                    }
                }
            }
        }
    >>
}
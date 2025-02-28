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
                    c'16
                    ~
                    c'32
                    ~
                    c'64
                    d'64
                    ~
                    \tuplet 5/4
                    {
                        d'32
                        ~
                        d'32
                        ~
                        d'32
                        ~
                        d'32
                        e'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'32
                        ~
                        e'32
                        ~
                        e'32
                        ~
                        e'32
                        ~
                        e'32
                        f'32
                        ~
                        f'32
                        ~
                    }
                    \tuplet 5/4
                    {
                        f'32
                        ~
                        f'32
                        ~
                        f'32
                        g'32
                        ~
                        g'32
                        ~
                    }
                    g'16
                    a'16
                    ~
                    \tuplet 5/4
                    {
                        a'32
                        ~
                        a'32
                        b'32
                        ~
                        b'32
                        ~
                        b'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        b'32
                        ~
                        b'32
                        c''32
                        ~
                        c''32
                        ~
                        c''32
                        ~
                        c''32
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
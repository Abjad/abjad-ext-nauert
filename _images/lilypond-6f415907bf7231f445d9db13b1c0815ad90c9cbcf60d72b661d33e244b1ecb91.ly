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
                \tempo 4=60
                c'4
                cs'4
                \tempo 4=120
                d'2
                ef'4
                ~
                \tempo 4=90
                ef'8.
                e'4
                ~
                e'16
                ~
                \tuplet 3/2
                {
                    \tempo 4=30
                    e'32
                    f'8.
                    fs'8
                    ~
                    fs'32
                    ~
                }
                \tuplet 3/2
                {
                    fs'32
                    g'8.
                    r32
                    r8
                }
            }
        }
    >>
}
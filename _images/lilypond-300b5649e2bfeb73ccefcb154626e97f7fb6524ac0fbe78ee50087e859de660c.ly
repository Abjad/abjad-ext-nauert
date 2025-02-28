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
                    \tempo 4=60
                    \time 4/4
                    c'4
                    \grace {
                        c'16
                    }
                    r4
                    c'4
                    r4
                }
            }
        }
    >>
}
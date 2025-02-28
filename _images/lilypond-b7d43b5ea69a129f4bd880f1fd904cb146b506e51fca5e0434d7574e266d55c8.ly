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
                        r16
                    }
                    c'4
                    r4
                    r4
                }
            }
        }
    >>
}
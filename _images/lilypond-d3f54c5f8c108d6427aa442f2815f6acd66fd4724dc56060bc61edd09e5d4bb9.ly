\version "2.19.83"
\language "english"
\score
{
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
}
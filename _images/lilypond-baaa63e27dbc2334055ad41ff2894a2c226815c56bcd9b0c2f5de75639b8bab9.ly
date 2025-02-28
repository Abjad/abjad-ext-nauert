\version "2.19.83"
\language "english"
\score
{
    \new Voice
    {
        \set proportionalNotationDuration = #1/12
        \tuplet 5/4
        {
            c'4
            \tuplet 3/2
            {
                c'4
                c'4
                c'4
            }
            c'2
        }
    }
}
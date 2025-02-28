\version "2.19.83"
\language "english"
\score
{
    \new Voice
    {
        \tuplet 3/2
        {
            \set Score.proportionalNotationDuration = #1/12
            c'4
            c'4
            c'4
        }
    }
}
\version "2.19.83"
\language "english"
\score
{
    \new Voice
    {
        \tuplet 5/4
        {
            \set Score.proportionalNotationDuration = #1/12
            c'8
            c'8
            c'8
            c'4.
            c'2
        }
    }
}
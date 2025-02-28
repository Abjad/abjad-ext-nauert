\version "2.19.83"
\language "english"
\score
{
    \new Score
    \with
    {
        proportionalNotationDuration = #1/12
    }
    <<
        \new Voice
        {
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'4
                    c'4
                }
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'4
                    c'4
                }
            }
        }
    >>
}
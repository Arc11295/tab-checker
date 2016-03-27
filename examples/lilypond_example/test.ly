\version "2.18.2"
\score {
  \new Staff {
    \time 3/4
    \key d \major
    \tempo 4 = 110 
    \new Voice \relative c'' {
      \set Staff.midiInstrument = #"distorted guitar"
      < a d a' d >2 r4
      e''2 r4
      < a,, d g d' >2 r4
      a'2 \tuplet 3/2{a,4 a8}
      \tuplet 3/2 4 {
        a4 d8 fis4 e8 d4 cis8 
        d4 b8 g4 cis8 a d b
        cis4 a8 g4 d'8 b4 cis8
        d4 e8 fis d e a,4 a8
        a4 d8 fis4 e8 d4 cis8 
        d4 b8 g4 cis8 a d b
        cis4 d8 e4 fis8 g e cis
      } 
      d4 d \tuplet 3/2{a4 a8}
      \tuplet 3/2 4 {
        a4 d8 fis4 e8 d4 cis8 
        d4 b8 g4 cis8 a d b
        cis4 a8 g4 d'8 b4 cis8
        d4 e8 fis d e a,4 a8
        a4 d8 fis4 e8 d4 cis8 
        d4 b8 g4 cis8 a d b
        cis4 d8 e4 fis8 g e cis
      } 
      d4 d \tuplet 3/2 {a'4 a8}
      \tuplet 3/2 4 {
        g fis e fis4 d8 cis d e
        a d, d g d d fis4 fis8
        g a b b g e a4 a8
        g fis d e fis e e4 e8
        d cis d e4 e8 a e cis
        g' d d fis4 fis8 e cis e
        d b d g a b fis d fis
      }
      e4 \tuplet 3/2 4 { e8 fis e a4 a8
        g fis e fis4 d8 cis d e
        a d, d g d d fis4 fis8
        g a b b g e a4 a8
        g fis d e fis e e4 e8
        d cis d e4 e8 a e cis
        g' d d fis4 fis8 e cis e
        d b d g a b fis d fis
    }
    e4 \tuplet 3/2 4 {e a8 a,4 a8}
  }
  }
  \layout{}
  \midi {}
}

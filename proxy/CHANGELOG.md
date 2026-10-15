# Proxy changelog

## Unreleased

- Fix punctuation abbreviation expansion: `&`, `w/`, and `w/o` now expand at
  non-word delimiters without matching inside adjacent words. In particular,
  `w/o data` expands to `without data` rather than `witho data`. Abbreviation
  ambiguity and capitalization loss remain unchanged.

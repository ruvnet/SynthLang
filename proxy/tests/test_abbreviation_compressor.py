"""Regression tests for punctuation boundaries in abbreviation expansion."""

import pytest

from src.app.synthlang.compression.abbreviation import AbbreviationCompressor


@pytest.mark.parametrize(
    "abbreviation,expanded", [("&", "and"), ("w/", "with"), ("w/o", "without")]
)
@pytest.mark.parametrize(
    "before,after", [("", ""), (" ", " "), ("(", ")."), ("\n", "\n")]
)
def test_punctuation_abbreviations_expand_at_delimiters(
    abbreviation, expanded, before, after
):
    result = AbbreviationCompressor().decompress(before + abbreviation + after)

    assert result.success
    assert result.text == before + expanded + after
    assert result.metrics["replacements"] == 1


@pytest.mark.parametrize("abbreviation", ["&", "w/", "w/o"])
@pytest.mark.parametrize("adjacent", ["x", "1", "_", "é"])
@pytest.mark.parametrize("side", ["before", "after"])
def test_punctuation_abbreviations_do_not_expand_inside_words(
    abbreviation, adjacent, side
):
    text = adjacent + abbreviation if side == "before" else abbreviation + adjacent
    result = AbbreviationCompressor().decompress(text)

    assert result.success
    assert result.text == text
    assert result.metrics["replacements"] == 0


@pytest.mark.parametrize(
    "text", ["and", "with data", "without data", "with and without data"]
)
def test_punctuation_abbreviations_round_trip(text):
    compressor = AbbreviationCompressor()
    compressed = compressor.compress(text)
    result = compressor.decompress(compressed.text)

    assert compressed.success
    assert result.success
    assert result.text == text


def test_word_abbreviations_still_respect_boundaries():
    result = AbbreviationCompressor().decompress("(fn) fn_call infobase config2")

    assert result.success
    assert result.text == "(function) fn_call infobase config2"

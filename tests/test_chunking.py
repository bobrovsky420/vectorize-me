from vectorizer.ingest.chunking import chunk_by_words, chunk_by_sections


def test_chunk_by_words_basic_overlap():
    assert chunk_by_words('a b c d e f', 3, 1) == ['a b c', 'c d e', 'e f']


def test_chunk_by_words_single_chunk_when_text_fits():
    assert chunk_by_words('a b c', 5, 1) == ['a b c']


def test_chunk_by_words_empty():
    assert chunk_by_words('   ', 3, 1) == []


def test_chunk_by_sections_splits_on_any_heading_level():
    text = '# Intro\nhello\n\n## Details\nworld\n\n### Sub\ndeep'
    parts = chunk_by_sections(text)
    assert parts == ['# Intro\nhello', '## Details\nworld', '### Sub\ndeep']


def test_chunk_by_sections_merges_preamble_into_first_section():
    text = 'preamble\n\n# Intro\nhello'
    parts = chunk_by_sections(text)
    assert parts == ['preamble\n\n# Intro\nhello']


def test_chunk_by_sections_no_heading_is_single_part():
    assert chunk_by_sections('just some text') == ['just some text']


def test_chunk_by_sections_empty():
    assert chunk_by_sections('   ') == []

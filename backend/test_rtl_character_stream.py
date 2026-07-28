from app.parsers.rtl.character_stream import CharacterStream


def test_initial_state():
    stream = CharacterStream("abc")

    assert stream.peek() == "a"
    assert stream.index == 0
    assert stream.line == 1
    assert stream.column == 1


def test_advance_updates_position():
    stream = CharacterStream("abc")

    assert stream.advance() == "a"
    assert stream.peek() == "b"

    assert stream.index == 1
    assert stream.line == 1
    assert stream.column == 2


def test_eof_detection():
    stream = CharacterStream("a")

    assert not stream.eof()

    stream.advance()

    assert stream.eof()

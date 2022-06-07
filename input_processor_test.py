from input_processor import read_ulog_input


def test_read_log_input():
    result = read_ulog_input("test_dataset")
    assert isinstance(result, dict)
    assert len(result) == 1


def test_read_log_wrong_path():
    result = read_ulog_input("test")
    assert isinstance(result, dict)
    assert bool(result) == False

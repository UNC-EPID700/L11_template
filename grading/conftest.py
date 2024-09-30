def pytest_addoption(parser):
    parser.addoption(
        "--regex",
        action="append", 
        default=[], 
        help="regex to use"
    )

    parser.addoption(
        "--key", 
        action="append", 
        default=[],
        help="Answer key to use"
    )
    parser.addoption(
        "--answer_path",
        action="append",
        default=[],
        help="URL of answer key",
    )
 
    parser.addoption(
        "--files",
        action="append",
        default=[],
        help="List of file names to be graded."
    )

    parser.addoption(
        "--cols",
        action="append",
        default=[],
        help="List of columns to check"
    )


def pytest_generate_tests(metafunc):
    if "regex" in metafunc.fixturenames: 
       metafunc.parametrize(
            "regex", metafunc.config.getoption("regex")) 

    if "key" in metafunc.fixturenames: 
        metafunc.parametrize(
            "key", metafunc.config.getoption("key"))
        
    if "answer_path" in metafunc.fixturenames:
        metafunc.parametrize(
            "answer_path", metafunc.config.getoption("answer_path"))

    if "files" in metafunc.fixturenames:
        metafunc.parametrize(
            "files", metafunc.config.getoption("files"))

    if "cols" in metafunc.fixturenames:
        metafunc.parametrize(
            "cols", metafunc.config.getoption("cols"))

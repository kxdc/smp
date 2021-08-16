from smp import __version__
from main import SimpleMailHelper


def test_version():
    assert __version__ == "0.1.0"


def test_exists_file():
    helper = SimpleMailHelper()
    assert helper.exists_file("../sample.txt") == True
    assert helper.exists_file("../../not_here.txt") == False

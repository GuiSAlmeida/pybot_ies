from utils import get_classes


def test_get_classes_lenght():
    response = get_classes()
    assert len(response) == 10

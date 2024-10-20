
from backend.app.utils.misc_util import get_today


def test_get_today():
    today = get_today()
    print(today)
    assert isinstance(today, str)
    assert len(today) > 0
    assert "(" in today
    assert ")" in today
    assert today.count("(") == 1

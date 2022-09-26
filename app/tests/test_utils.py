from app.utils import is_code, get_slugs


def test_is_code():
    assert is_code(31223) == False
    assert is_code("DFSER") == True
    assert is_code("uk_main") == False


def test_get_slugs():
    slug = "north_europe_main"
    results = get_slugs(slug)
    assert type(results) == list
    assert len(results) > 0


def test_get_slugs_no_result():
    slug = "unkown_region"
    results = get_slugs(slug)
    assert type(results) == list
    assert len(results) == 0
    assert results == []

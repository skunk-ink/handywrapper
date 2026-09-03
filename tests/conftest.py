import pytest

from handywrapper import hsd, hsw

HSD_BASE = 'http://x:testkey@127.0.0.1:12037'
HSW_BASE = 'http://x:testkey@127.0.0.1:12039'


@pytest.fixture
def hsd_client():
    return hsd('testkey', '127.0.0.1', 12037)


@pytest.fixture
def hsw_client():
    return hsw('testkey', '127.0.0.1', 12039)

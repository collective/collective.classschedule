from plone.dexterity.utils import resolveDottedName
from zope.component import createObject

import pytest


@pytest.fixture
def portal_type() -> str:
    return "AcademicCalendar"


class TestContentType:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.container = portal

    def test_get_fti(self, get_fti, portal_type):
        assert get_fti(portal_type) is not None

    def test_create(self, get_fti, portal_type):
        fti = get_fti(portal_type)
        factory = fti.factory
        klass = resolveDottedName(fti.klass)
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, klass)
        assert obj.portal_type == portal_type

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IBuilding(model.Schema):
    """Marker interface and Dexterity Python Schema for Building"""


@implementer(IBuilding)
class Building(Container):
    """Content-type class for IBuilding"""

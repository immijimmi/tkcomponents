import pytest

from tkcomponents import Component


@pytest.fixture
def blank_parent_cls():
    class Blank(Component):
        def _render(self):
            pass

    class Parent(Component):
        def _render(self):
            self.children["blank"] = None

            blank = Blank(self._frame)
            self.children["blank"] = blank

            blank.render().pack()

    return Parent

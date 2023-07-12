import pytest
from tkinter import Tk, Button

from tkcomponents import Component


@pytest.fixture
def window():
    return Tk()


@pytest.fixture
def nested_button_cls():
    class ButtonWrapper(Component):
        COMPONENT_STYLES = {
            "button": {}
        }

        def _render(self):
            button = Button(self._frame, **self.styles["button"])
            self.children["button"] = button

            button.pack()

    class Parent(Component):
        COMPONENT_STYLES = {
            "button_wrapper": {}
        }

        def _render(self):
            button_wrapper = ButtonWrapper(self._frame, styles=self.styles["button_wrapper"])
            self.children["button_wrapper"] = button_wrapper

            button_wrapper.render().pack()

    return Parent

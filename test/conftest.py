import pytest
from tkinter import Tk, Button

from tkcomponents import Component


@pytest.fixture
def window():
    return Tk()


@pytest.fixture
def nested_button_cls():
    class ButtonWrapper(Component):
        def __init__(self, container, get_data=None, on_change=lambda: None,
                     update_interval_ms=None, styles=None):
            super().__init__(container, get_data=get_data, on_change=on_change,
                             update_interval_ms=update_interval_ms, styles=styles)

            styles = styles or {}
            self.styles["button"] = styles.get("button", {})

        def _render(self):
            self.children["button"] = None

            button = Button(self._frame, **self.styles["button"])
            self.children["button"] = button

            button.pack()

    class Parent(Component):
        def __init__(self, container, get_data=None, on_change=lambda: None,
                     update_interval_ms=None, styles=None):
            super().__init__(container, get_data=get_data, on_change=on_change,
                             update_interval_ms=update_interval_ms, styles=styles)

            styles = styles or {}
            self.styles["button_wrapper"] = styles.get("button_wrapper", {})

        def _render(self):
            self.children["button_wrapper"] = None

            button_wrapper = ButtonWrapper(self._frame, styles=self.styles["button_wrapper"])
            self.children["button_wrapper"] = button_wrapper

            button_wrapper.render().pack()

    return Parent

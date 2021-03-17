import pytest
from tkinter import Tk, Frame

from tkcomponents import Component


class TestComponent:
    def test_exists(self, window, nested_button_cls):
        parent = nested_button_cls(window)

        assert parent.exists

        parent.render().pack()
        child = parent.children["button_wrapper"]

        assert child.exists

        parent.render()

        assert not child.exists

    def test_is_rendered(self, window, nested_button_cls):
        parent = nested_button_cls(window)

        assert not parent.is_rendered

        parent.render().pack()
        child = parent.children["button_wrapper"]

        assert child.is_rendered

        parent.render()

        assert not child.is_rendered

    def test_height(self, window, nested_button_cls):
        base_button_height = 5
        default_char_height = 15

        height_chars = 3  # Arbitrarily > 1
        pady = 2
        borderwidth = 1

        height_pixels = base_button_height + (height_chars * default_char_height) + (pady * 2) + (borderwidth * 2)

        parent = nested_button_cls(window, styles={"button_wrapper": {
            "frame": {
                "pady": pady,
                "borderwidth": borderwidth
            },
            "button": {
                "height": height_chars,
                "pady": 0,
                "borderwidth": 0
            }
        }})
        parent.render().pack(fill="both", expand=True)
        child = parent.children["button_wrapper"]

        assert child.height == height_pixels

        height_chars = 4
        pady = 3
        borderwidth = 2

        height_pixels = base_button_height + (height_chars * default_char_height) + (pady * 2) + (borderwidth * 2)

        parent.styles["button_wrapper"]["frame"]["pady"] = pady
        parent.styles["button_wrapper"]["frame"]["borderwidth"] = borderwidth
        parent.styles["button_wrapper"]["button"]["height"] = height_chars

        parent.render()
        child = parent.children["button_wrapper"]

        assert child.height == height_pixels

    def test_width(self, window, nested_button_cls):
        base_button_width = 4
        default_char_width = 7

        width_chars = 3  # Arbitrarily more than the default space reserved for the button text
        padx = 2
        borderwidth = 1

        width_pixels = base_button_width + (width_chars * default_char_width) + (padx * 2) + (borderwidth * 2)

        parent = nested_button_cls(window, styles={"button_wrapper": {
            "frame": {
                "padx": padx,
                "borderwidth": borderwidth
            },
            "button": {
                "width": width_chars,
                "padx": 0,
                "borderwidth": 0
            }
        }})
        parent.render().pack(fill="both", expand=True)

        child = parent.children["button_wrapper"]

        assert child.width == width_pixels

        width_chars = 4
        padx = 3
        borderwidth = 2

        width_pixels = base_button_width + (width_chars * default_char_width) + (padx * 2) + (borderwidth * 2)

        parent.styles["button_wrapper"]["frame"]["padx"] = padx
        parent.styles["button_wrapper"]["frame"]["borderwidth"] = borderwidth
        parent.styles["button_wrapper"]["button"]["width"] = width_chars

        parent.render()
        child = parent.children["button_wrapper"]

        assert child.width == width_pixels

    def test_height_clearance(self, window, nested_button_cls):
        base_button_height = 5
        default_char_height = 15

        height_chars = 3  # Arbitrarily > 1
        pady = 2
        borderwidth = 1

        height_clearance_pixels = base_button_height + (height_chars * default_char_height)

        parent = nested_button_cls(window, styles={"button_wrapper": {
            "frame": {
                "pady": pady,
                "borderwidth": borderwidth
            },
            "button": {
                "height": height_chars,
                "pady": 0,
                "borderwidth": 0
            }
        }})
        parent.render().pack(fill="both", expand=True)

        child = parent.children["button_wrapper"]

        assert child.height_clearance == height_clearance_pixels

        height_chars = 4
        pady = 3
        borderwidth = 2

        height_clearance_pixels = base_button_height + (height_chars * default_char_height)

        parent.styles["button_wrapper"]["frame"]["pady"] = pady
        parent.styles["button_wrapper"]["frame"]["borderwidth"] = borderwidth
        parent.styles["button_wrapper"]["button"]["height"] = height_chars

        parent.render()
        child = parent.children["button_wrapper"]

        assert child.height_clearance == height_clearance_pixels

    def test_width_clearance(self, window, nested_button_cls):
        base_button_width = 4
        default_char_width = 7

        width_chars = 3  # Arbitrarily more than the default space reserved for the button text
        padx = 2
        borderwidth = 1

        width_clearance_pixels = base_button_width + (width_chars * default_char_width)

        parent = nested_button_cls(window, styles={"button_wrapper": {
            "frame": {
                "padx": padx,
                "borderwidth": borderwidth
            },
            "button": {
                "width": width_chars,
                "padx": 0,
                "borderwidth": 0
            }
        }})
        parent.render().pack(fill="both", expand=True)

        child = parent.children["button_wrapper"]

        assert child.width_clearance == width_clearance_pixels

        width_chars = 4
        padx = 3
        borderwidth = 2

        width_clearance_pixels = base_button_width + (width_chars * default_char_width)

        parent.styles["button_wrapper"]["frame"]["padx"] = padx
        parent.styles["button_wrapper"]["frame"]["borderwidth"] = borderwidth
        parent.styles["button_wrapper"]["button"]["width"] = width_chars

        parent.render()
        child = parent.children["button_wrapper"]

        assert child.width_clearance == width_clearance_pixels

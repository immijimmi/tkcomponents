from tkinter import Text, StringVar

from ..component import Component
from ..extensions import GridHelper


class MultilineStringEditor(Component.with_extensions(GridHelper)):
    def __init__(self, container, get_data=None, on_change=(lambda editor, old_value: None),
                 update_interval=None, styles=None):
        super().__init__(container, get_data=get_data, on_change=on_change,
                         update_interval=update_interval, styles=styles)

        styles = {} if not styles else styles
        self.styles["text"] = styles.get("text", {})
        self.styles["text_saved"] = styles.get("text_saved", {})
        self.styles["text_unsaved"] = styles.get("text_unsaved", {})

        self._value = self._get_data(self) if self._get_data else ""

        self.__text_style__current = None  # Used by __apply_text_style

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        try:
            self.children["text"].delete("1.0", "end")
            self.children["text"].insert("1.0", value)
        except KeyError:  # If the text widget has not yet been rendered
            pass

        self._value = self.value

    @property
    def is_unsaved(self):
        if not self._get_data:
            return False

        source_value = self._get_data(self)
        return source_value != self.value

    def _update(self):
        self.__apply_text_style("text_unsaved" if self.is_unsaved else "text_saved")

    def _render(self):
        self.children["text"] = None

        self._apply_frame_stretch(columns=[0], rows=[0])

        text = Text(self._frame, **self.styles["text"])
        self.children["text"] = text
        self.value = self.value  # This just invokes the logic in the .value setter
        text.grid(row=0, column=0, sticky="nswe")

        self.__apply_text_style("text_saved")

    def _handle_input(self):
        old_value = self.value
        self.value = self.children["text"].get("1.0", "end")  # "1.0" is Line 1, Char 0

        self._on_change(self, old_value)

        if self.exists:
            self._update()

    def __apply_text_style(self, style_key):
        """
        This method exists to minimise calls to .configure(), as they can impact insertion cursor functionality
        """

        if style_key != self.__text_style__current:
            self.__text_style__current = style_key
            self.children["text"].configure(**self.styles[style_key])

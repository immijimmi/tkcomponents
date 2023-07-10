from abc import ABC
from tkinter import Frame, Scrollbar, Canvas

from ..component import Component


class ScrollFrame(Component, ABC):
    def __init__(self, container, get_size, is_scroll_vertical: bool = True, get_data=None, on_change=lambda: None,
                 update_interval_ms=None, styles=None):
        super().__init__(container, get_data=get_data, on_change=on_change,
                         update_interval_ms=update_interval_ms, styles=styles)

        """
        To make this frame fit perfectly into a containing `Component` instance, `.get_size()` should
        return that component's `.height_clearance`/`.width_clearance` property
        (depending on whether this component scrolls vertically or horizontally, respectively)
        """
        self._get_size = get_size
        self._is_scroll_vertical = is_scroll_vertical

        styles = styles or {}
        self.styles["inner_frame"] = styles.get("inner_frame", {})
        self.styles["canvas"] = styles.get("canvas", {})
        self.styles["scrollbar"] = styles.get("scrollbar", {})

    def _refresh_frame(self):
        def on_resize(event):
            if not self.is_rendered:
                return

            self._frame__canvas.configure(
                width=0,
                height=0
            )  ##### TODO: Test if this correctly allows the component to resize back down when not being stretched

            if self._is_scroll_vertical:
                height = self._get_size()
                width = self._frame.winfo_reqwidth()
            else:
                height = self._frame.winfo_reqheight()
                width = self._get_size()

            self._frame__canvas.configure(
                width=width,
                height=height,
                scrollregion=self._frame__canvas.bbox("all")
            )
            self._frame.configure(
                width=width,
                height=height
            )

        self._frame__main = Frame(self._outer_frame, **self.styles["frame"])
        self._frame__canvas = Canvas(self._frame__main, highlightthickness=0, **self.styles["canvas"])
        self._frame__scroll = Scrollbar(
            self._frame__main,
            orient=("vertical" if self._is_scroll_vertical else "horizontal"),
            command=(self._frame__canvas.yview if self._is_scroll_vertical else self._frame__canvas.xview),
            **self.styles["scrollbar"]
        )
        self._frame = Frame(self._frame__canvas, **self.styles["inner_frame"])

        # Custom configuration for the Canvas window
        if self._is_scroll_vertical:
            canvas_height = self._get_size()
            canvas_width = self._frame.winfo_reqwidth()
            canvas_scrollcommand_option = "yscrollcommand"
        else:
            canvas_height = self._frame.winfo_reqheight()
            canvas_width = self._get_size()
            canvas_scrollcommand_option = "xscrollcommand"

        self._frame__canvas.create_window((0, 0), window=self._frame, anchor="nw")
        self._frame__canvas.configure(
            height=canvas_height, width=canvas_width,
            scrollregion=self._frame__canvas.bbox("all"),
            **{canvas_scrollcommand_option: self._frame__scroll.set}
        )
        self._frame__main.bind("<Configure>", on_resize)
        self._enable_mousewheel_scroll(self._frame__canvas, do_include_children=False)

        if self._is_scroll_vertical:
            self._frame__scroll.grid(row=0, column=1, sticky="nse")
        else:
            self._frame__scroll.grid(row=1, column=0, sticky="swe")
        self._frame__main.grid(row=0, column=0, sticky="nswe")
        self._frame__canvas.grid(row=0, column=0, sticky="nswe")

    def _enable_mousewheel_scroll(self, widget, do_include_children: bool = False):
        """
        Any widgets rendered inside this component which should still allow the canvas to scroll when hovering over
        them must be passed into this method.

        If `do_include_children` is `True`, any child widgets contained within the provided widget (recursively)
        will also have scrolling enabled when hovering over them
        """

        if self._is_scroll_vertical:
            canvas_scroll_function = self._frame__canvas.yview_scroll
        else:
            canvas_scroll_function = self._frame__canvas.xview_scroll

        widget.bind(
            "<MouseWheel>",
            lambda event: canvas_scroll_function(self.__get_scroll_direction(event.delta), "units")
        )

        if do_include_children:
            widgets_to_add = widget.winfo_children()

            while widgets_to_add:
                child_widgets_to_add = []

                for widget_to_add in widgets_to_add:
                    widget.bind(
                        "<MouseWheel>",
                        lambda event: canvas_scroll_function(self.__get_scroll_direction(event.delta), "units")
                    )

                    child_widgets_to_add += widget_to_add.winfo_children()

                widgets_to_add = child_widgets_to_add

    @staticmethod
    def __get_scroll_direction(event_delta):
        return int(-1 * (event_delta / abs(event_delta)))

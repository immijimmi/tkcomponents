from objectextensions import Extendable

from abc import ABC
from tkinter import Frame


class Component(Extendable, ABC):
    def __init__(self, container, get_data=None, on_change=lambda: None,
                 update_interval=None, styles=None):
        super().__init__()

        self._container = container

        self._outer_frame = Frame(self._container)
        self._frame = None  # Add child elements to this frame in _render()

        # Allow the outer frame to expand to fill the container
        self._outer_frame.rowconfigure(0, weight=1)
        self._outer_frame.columnconfigure(0, weight=1)

        # All element styles should be stored here, as their own dicts
        self.styles = {}
        styles = {} if not styles else styles
        self.styles["frame"] = styles.get("frame", {})

        # Use this space to keep hold of any elements that might need configuring in _update or _get_data
        self.children = {}

        self._update_interval = update_interval  # Milliseconds

        """
        This function should receive this component instance as a parameter and return any data from the
        application state that is needed by this component.
        If it is set to None rather than a function, this indicates that there is no outside data source.
        Other aspects of this component (styles, etc.) can be edited during the execution of this function.
        """
        self._get_data = get_data
        """
        When the state of this component changes, this function should be called and passed this component instance
        and any event data as parameters.
        The function should perform any additional external work needed.
        """
        self._on_change = on_change

    @property
    def exists(self):
        return self._outer_frame.winfo_exists()

    @property
    def is_rendered(self):
        if self._frame is None:
            return False

        self._frame.update()
        return self._frame.winfo_exists()

    @property
    def height(self):
        self._outer_frame.update()
        return self._outer_frame.winfo_height()

    @property
    def width(self):
        self._outer_frame.update()
        return self._outer_frame.winfo_width()

    @property
    def height_clearance(self):
        if not self.is_rendered:
            return None

        frame_padding = self.styles["frame"].get("pady", 0)
        frame_borderwidth = self.styles["frame"].get("borderwidth", 0)
        total_buffer = (2 * frame_padding) + (2 * frame_borderwidth)

        return self._frame.winfo_height() - total_buffer

    @property
    def width_clearance(self):
        if not self.is_rendered:
            return None

        frame_padding = self.styles["frame"].get("padx", 0)
        frame_borderwidth = self.styles["frame"].get("borderwidth", 0)
        total_buffer = (2 * frame_padding) + (2 * frame_borderwidth)

        return self._frame.winfo_width() - total_buffer

    def render(self):
        for child_element in self._outer_frame.winfo_children():
            child_element.destroy()
        self._refresh_frame()

        self._render()

        if self._update_interval:
            self._frame.after(self._update_interval, self._update_loop)

        return self._outer_frame

    def _update_loop(self):
        self._frame.after_cancel(self._update_loop)

        if not self.exists:
            return

        if self._update_interval:
            self._frame.after(self._update_interval, self._update_loop)

        self._update()

        if self._needs_render:
            self.render()

    # Overridable Methods

    @property
    def _needs_render(self):
        """
        Should return a True value only once per time a re-render is required.
        If the component will never need to poll for a re-render, this method need not be overridden.
        """
        return False

    def _refresh_frame(self):
        """
        Only needs overriding if the component as a container needs extra functionality.
        """
        self._frame = Frame(self._outer_frame, **self.styles["frame"])

        self._frame.grid(row=0, column=0, sticky="nswe")

    def _update(self):
        """
        If the component will not need to directly update any values outside of a new render,
        this method need not be overridden.
        """
        pass

    def _render(self):
        raise NotImplementedError

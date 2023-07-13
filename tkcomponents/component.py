from objectextensions import Extendable, Decorators

from abc import ABC
from tkinter import Frame, Widget
from typing import Optional, Any, Callable


class Component(Extendable, ABC):
    """
    A blank base component which extends lifecycle methods to be overriden as necessary
    """

    """
    This attribute can optionally be overwritten in each subclass, with a new dictionary containing
    any *additional* style labels (and their default values) those subclasses expect to receive and use inside
    `._render()`. Styles from all classes in the hierarchy which define styles under this attribute name will be
    aggregated into `self.styles`, so that they are all available to be used as necessary in each successive subclass
    """
    COMPONENT_STYLES: dict[str, dict[str, Any]] = {
        "frame": {}
    }

    def __init__(
            self, container: Widget,
            get_data: Optional[Callable[["Component"], Any]] = None,
            on_change: Callable[["Component", Any], None] = (lambda component, event_data: None),
            update_interval_ms: Optional[int] = None, styles: Optional[dict[str, dict[str, Any]]] = None
    ):
        super().__init__()

        self._container = container

        self._outer_frame = Frame(self._container)
        self._frame = None  # Add child elements to this frame in ._render()

        # Allows the outer frame to expand to fill the containing area
        self._outer_frame.rowconfigure(0, weight=1)
        self._outer_frame.columnconfigure(0, weight=1)

        """
        All widget/component styles are stored in this dictionary, as their own dicts under a relevant string key.
        Nesting may optionally be employed if desired to pass styles down through multiple layers of components
        """
        self.styles: dict[str, dict[str, Any]] = {}

        # Populating `self.styles`
        styles_working = {**(styles or {})}
        for style_label, default_style_value in self.registered_styles.items():
            self.styles[style_label] = styles_working.pop(style_label, default_style_value)

        # There should be no remaining data in here after removing any styles also registered in `COMPONENT_STYLES`
        if styles_working:
            raise ValueError(f"unused styles passed into component: {tuple(styles_working.keys())}")

        self._children = {}

        self._update_interval_ms = update_interval_ms

        """
        The below function should receive this component instance as a parameter and return any external data
        that is needed by this component - this may be as simple as returning static initialisation params, or
        as complicated as processing the application state to provide a tailored value each time it is called.

        It should be called only from within the constructor and within `._update()` (if necessary).

        Can be None rather than a function, which indicates that there is no need for a data source in the component.
        Other aspects of this component (styles, etc.) may be edited by this function as needed
        """
        self._get_data = get_data

        """
        When the state of this component changes, the below function should be called and passed this component instance
        and any event data as parameters.
        This function is also responsible for performing any additional external work that may be needed as a result
        of the event that has triggered it
        """
        self._on_change = on_change

    @property
    def exists(self) -> bool:
        """
        Used to check that the component has not been destroyed before performing work on it, for example if a parent
        component has executed a fresh `.render()`
        """

        return self._outer_frame.winfo_exists()

    @property
    def is_rendered(self) -> bool:
        """
        Used internally to check that a component has rendered its contained widgets, before accessing them
        """

        if self._frame is None:
            return False

        self._frame.update()
        return self._frame.winfo_exists()

    @property
    def height(self) -> int:
        self._outer_frame.update()
        return self._outer_frame.winfo_height()

    @property
    def width(self) -> int:
        self._outer_frame.update()
        return self._outer_frame.winfo_width()

    @property
    def height_clearance(self) -> Optional[int]:
        """
        Represents the amount of vertical space inside the widget (values such as padding and border are removed)
        """

        if not self.is_rendered:
            return None

        frame_padding = self.styles["frame"].get("pady", 0)
        frame_borderwidth = self.styles["frame"].get("borderwidth", 0)
        total_buffer = (2 * frame_padding) + (2 * frame_borderwidth)

        return self._frame.winfo_height() - total_buffer

    @property
    def width_clearance(self) -> Optional[int]:
        """
        Represents the amount of horizontal space inside the widget (values such as padding and border are removed)
        """

        if not self.is_rendered:
            return None

        frame_padding = self.styles["frame"].get("padx", 0)
        frame_borderwidth = self.styles["frame"].get("borderwidth", 0)
        total_buffer = (2 * frame_padding) + (2 * frame_borderwidth)

        return self._frame.winfo_width() - total_buffer

    @property
    def children(self) -> dict:
        """
        Use this dictionary to store references to any child widgets/components as needed, within `._render()`.
        Any stored data will be automatically cleared immediately before the next `._render()` call,
        to prevent unintended behaviour due to lingering references to old child elements
        """

        return self._children

    @Decorators.classproperty
    def registered_styles(cls) -> dict[str, dict[str, Any]]:
        styles = {}

        for included_cls in cls.__mro__:
            if included_cls_styles := included_cls.__dict__.get("COMPONENT_STYLES", None):
                for style_label, default_style_value in included_cls_styles.items():
                    if style_label in styles:
                        raise KeyError(
                            f"duplicate style label defined in multiple classes in the hierarchy: {style_label}"
                        )

                    styles[style_label] = default_style_value

        return styles

    def render(self) -> Frame:
        """
        This method should be invoked externally, and the returned frame have `.pack()` or `.grid()` called on it.
        It will always need to be called at least once, from the containing scope, but can be called again
        if its child widgets need to be completely refreshed
        """

        for child_element in self._outer_frame.winfo_children():
            child_element.destroy()
        self.children.clear()

        self._refresh_frame()
        self._render()

        if self._update_interval_ms:
            self._frame.after(self._update_interval_ms, self._update_loop)

        return self._outer_frame

    def update(self) -> None:
        """
        This method is optional and should be invoked externally if necessary,
        in situations where `._update()` needs to be carried out immediately rather than at the next update interval
        """

        if not self.exists:
            return

        self._update()

        if self._needs_render:
            self.render()

    def _update_loop(self) -> None:
        """
        Used internally to handle updating the component once per update interval (if update interval was provided)
        """

        self._frame.after_cancel(self._update_loop)

        if not self.exists:
            return

        if self._update_interval_ms:
            self._frame.after(self._update_interval_ms, self._update_loop)

        self._update()

        if self._needs_render:
            self.render()

    # Overridable Methods

    @property
    def _needs_render(self) -> bool:
        """
        Overridable method.
        Should return a `True` value only once per time a re-render is required.
        If the component will never need to poll for a re-render, this method need not be overridden
        """

        return False

    def _refresh_frame(self) -> None:
        """
        Overridable method.
        Handles creating a new blank frame to store as `self._frame` at the top of each `.render()` call.
        Only needs overriding if this component requires extra base functionality before any child components
        are rendered onto its surface.

        Any overriding method should still set a new `Frame` object to `self._frame`, to be used
        as the main surface to render child widgets to
        """

        self._frame = Frame(self._outer_frame, **self.styles["frame"])

        self._frame.grid(row=0, column=0, sticky="nswe")

    def _update(self) -> None:
        """
        Overridable method.
        Handles updating the component state once per update interval (if update interval was provided).
        If the component will not need to directly update its state outside of a new render,
        this method need not be overridden
        """

        pass

    def _render(self) -> None:
        """
        Overridable method.
        Any child components should be rendered to `self._frame` in this method
        """

        raise NotImplementedError

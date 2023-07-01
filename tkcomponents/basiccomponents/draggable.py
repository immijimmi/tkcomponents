from tkinter import Frame
from tkinter.dnd import dnd_start
from functools import partial
from abc import ABC

from ..component import Component


class Draggable(Component, ABC):
    def add_draggable_widget(self, widget, do_include_children: bool = False) -> None:
        """
        This method binds any tkinter widget (and all of its children recursively,
        if `do_include_children` is True) to this component's drag-and-drop functionality.

        In order to make this Component itself draggable, this method should be called and passed
        `self._frame` at the top of `._render()`. If this is not done, this component will still be capable of
        interacting with other dragged widgets but will not itself be draggable

        In order to bind another Component object to this Component's drag-and-drop functionality,
        this method can be called and passed the Frame widget returned by that Component object's `.render()` method
        """

        widget.bind("<Button-1>", partial(dnd_start, self))

        if do_include_children:
            widgets_to_add = [*widget.winfo_children]

            while widgets_to_add:
                child_widgets_to_add = []

                for widget_to_add in widgets_to_add:
                    widget_to_add.bind("<Button-1>", partial(dnd_start, self))

                    child_widgets_to_add += widget_to_add.winfo_children()

                widgets_to_add = child_widgets_to_add

    def dnd_accept(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def dnd_motion(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def dnd_leave(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def dnd_enter(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def dnd_commit(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def dnd_end(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def _refresh_frame(self) -> None:
        draggable_self = self  # renamed variable to prevent shadowing in inner class below

        class DraggableFrame(Frame):
            """
            Custom Frame class which simply defers its drag and drop lifecycle methods to the parent component
            """

            @staticmethod
            def dnd_accept(source, event):
                return self.dnd_accept(source, event)

            @staticmethod
            def dnd_motion(source, event):
                return self.dnd_motion(source, event)

            @staticmethod
            def dnd_leave(source, event):
                return self.dnd_leave(source, event)

            @staticmethod
            def dnd_enter(source, event):
                return self.dnd_enter(source, event)

            @staticmethod
            def dnd_commit(source, event):
                return self.dnd_commit(source, event)

            @staticmethod
            def dnd_end(source, event):
                return self.dnd_end(source, event)

        self._frame = DraggableFrame(self._outer_frame, **self.styles["frame"])

        self._frame.grid(row=0, column=0, sticky="nswe")

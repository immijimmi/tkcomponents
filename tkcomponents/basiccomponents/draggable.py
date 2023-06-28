from tkinter import Frame
from tkinter.dnd import dnd_start
from functools import partial
from abc import ABC

from ..component import Component


class Draggable(Component, ABC):
    def _refresh_frame(self) -> None:
        class DraggableFrame(Frame):
            """
            Custom Frame class which simply defers its drag and drop lifecycle methods to the parent component
            """

            def __init__(self, container, *args, **kwargs):
                super().__init__(container, *args, **kwargs)

                self.bind("<Button-1>", partial(dnd_start, self))

            def dnd_accept(self, source, event):
                return self.dnd_accept(source, event)

            def dnd_motion(self, source, event):
                return self.dnd_motion(source, event)

            def dnd_leave(self, source, event):
                return self.dnd_leave(source, event)

            def dnd_enter(self, source, event):
                return self.dnd_enter(source, event)

            def dnd_commit(self, source, event):
                return self.dnd_commit(source, event)

            def dnd_end(self, source, event):
                return self.dnd_end(source, event)

        self._frame = DraggableFrame(self._outer_frame, **self.styles["frame"])

        self._frame.grid(row=0, column=0, sticky="nswe")

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

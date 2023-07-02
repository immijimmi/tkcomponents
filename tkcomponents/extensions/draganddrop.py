from objectextensions import Extension

from tkinter.dnd import dnd_start
from functools import partial

from ..component import Component


class DragAndDrop(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, Component)

    @staticmethod
    def extend(target_cls):
        Extension._set(target_cls, "add_draggable_widget", DragAndDrop.__add_draggable_widget)

        Extension._set(target_cls, "dnd_accept", DragAndDrop.__dnd_accept)
        Extension._set(target_cls, "dnd_motion", DragAndDrop.__dnd_motion)
        Extension._set(target_cls, "dnd_leave", DragAndDrop.__dnd_leave)
        Extension._set(target_cls, "dnd_enter", DragAndDrop.__dnd_enter)
        Extension._set(target_cls, "dnd_commit", DragAndDrop.__dnd_commit)
        Extension._set(target_cls, "dnd_end", DragAndDrop.__dnd_end)

        Extension._wrap(target_cls, "_refresh_frame", DragAndDrop.__wrap_refresh_frame)

    def __wrap_refresh_frame(self, *args, **kwargs):
        yield
        self._frame.dnd_accept = self.dnd_accept
        self._frame.dnd_motion = self.dnd_motion
        self._frame.dnd_leave = self.dnd_leave
        self._frame.dnd_enter = self.dnd_enter
        self._frame.dnd_commit = self.dnd_commit
        self._frame.dnd_end = self.dnd_end

    def __add_draggable_widget(self, widget, do_include_children: bool = False) -> None:
        """
        This method binds any tkinter widget (and all of its children recursively,
        if `do_include_children` is True) to this component's drag-and-drop functionality.

        In order to make this Component itself draggable, this method should be called and passed
        `self._frame` anywhere during the execution of `._render()`. If this is not done, this component will still be
        capable of interacting with other dragged widgets but will not itself be draggable.

        In order to bind another Component object to this Component's drag-and-drop functionality,
        this method can be called and passed the Frame widget returned by that Component object's `.render()` method
        """

        widget.bind("<Button-1>", partial(dnd_start, self))

        if do_include_children:
            widgets_to_add = widget.winfo_children()

            while widgets_to_add:
                child_widgets_to_add = []

                for widget_to_add in widgets_to_add:
                    widget_to_add.bind("<Button-1>", partial(dnd_start, self))

                    child_widgets_to_add += widget_to_add.winfo_children()

                widgets_to_add = child_widgets_to_add

    def __dnd_accept(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def __dnd_motion(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def __dnd_leave(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def __dnd_enter(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def __dnd_commit(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

    def __dnd_end(self, source, event):
        """
        Overridable method.
        Implement as necessary for your drag and drop functionality
        """

        pass

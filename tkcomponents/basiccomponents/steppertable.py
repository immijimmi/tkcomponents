from functools import partial
from tkinter import Label
from typing import Any, Optional, Callable

from ..component import Component
from ..extensions import GridHelper
from .stepper import Stepper


class StepperTable(Component.with_extensions(GridHelper)):
    def __init__(
        self, container,
        axis_labels: tuple[tuple[str, ...], tuple[str, ...]], axis_values: tuple[tuple[Any, ...], tuple[Any, ...]],
        get_data: Optional[Callable[[Any, Any, Stepper], Any]] = None,
        on_change=(lambda x_value, y_value, stepper, step_amount: None),
        before_steps=(("-", -1),), after_steps=(("+", 1),),
        format_label=(lambda stepper: str(stepper.value)), limits=(None, None), is_horizontal=True,
        update_interval_ms=None, styles=None
    ):
        super().__init__(container, get_data=get_data, on_change=on_change, styles=styles)

        styles = styles or {}
        self.styles["x_label"] = styles.get("x_label", {})
        self.styles["y_label"] = styles.get("y_label", {})

        self._stepper_kwargs = {
            "before_steps": before_steps,
            "after_steps": after_steps,
            "format_label": format_label,
            "limits": limits,
            "is_horizontal": is_horizontal,
            "update_interval_ms": update_interval_ms,
            "styles": styles.get("stepper", {})
        }

        self.axis_labels = axis_labels
        self.axis_values = axis_values

    def _render(self):
        self.children["axis_labels"] = [[], []]
        self.children["steppers"] = {}

        self._apply_frame_stretch(columns=[0], rows=[1])

        for x_index, x_label in enumerate(self.axis_labels[0]):
            label = Label(self._frame, text=x_label, **self.styles["x_label"])
            self.children["axis_labels"][0].append(label)
            label.grid(row=0, column=x_index+1, sticky="nswe")

        for y_index, y_label in enumerate(self.axis_labels[1]):
            label = Label(self._frame, text=y_label, **self.styles["y_label"])
            self.children["axis_labels"][1].append(label)
            label.grid(row=y_index+2, column=0, sticky="nswe")

        for x_index, x_value in enumerate(self.axis_values[0]):
            for y_index, y_value in enumerate(self.axis_values[1]):
                stepper = Stepper(
                    self._frame,
                    get_data=partial(self._get_data, x_value, y_value) if self._get_data else None,
                    on_change=partial(self._on_change, x_value, y_value),
                    **self._stepper_kwargs
                )
                self.children["steppers"][(x_index, y_index)] = stepper
                stepper.render().grid(row=y_index+2, column=x_index+1, sticky="nswe")

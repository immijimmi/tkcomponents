from tkinter import Label, Button, StringVar
from functools import partial
from typing import Callable, Any, Optional

from ..component import Component
from ..extensions import GridHelper


class Stepper(Component.with_extensions(GridHelper)):
    def __init__(
        self, container,
        get_data: Optional[Callable[["Stepper"], Any]] = None,
        on_change: Callable[["Stepper", Any], None] = (lambda stepper, step_amount: None),
        before_steps: tuple[tuple[str,  Any], ...] = (("-", -1),),
        after_steps: tuple[tuple[str,  Any], ...] = (("+", 1),),
        format_label: Callable[["Stepper"], str] = (lambda stepper: str(stepper.value)),
        limits: Optional[tuple[Any, Any]] = (None, None), is_horizontal: bool = True,
        update_interval_ms=None, styles=None
    ):
        super().__init__(container, get_data=get_data, on_change=on_change,
                         update_interval_ms=update_interval_ms, styles=styles)

        self.before_steps = before_steps
        self.after_steps = after_steps
        self.format_label = format_label
        self.is_horizontal = is_horizontal

        self.min = limits[0]
        self.max = limits[1]

        styles = styles or {}
        self.styles["button"] = styles.get("button", {})
        self.styles["label"] = styles.get("label", {})

        self.value = self._get_data(self) if self._get_data else 0

        self._label_var = StringVar()
        self._label_var.set(self.format_label(self.value))

    def _update(self):
        if self._get_data:
            self.value = self._get_data(self)

        self._label_var.set(self.format_label(self.value))

        self._set_button_states()

    def _render(self):
        self.children["before_buttons"] = []
        self.children["after_buttons"] = []
        self.children["label"] = None

        row_stretch = [0] if self.is_horizontal else [len(self.before_steps)]
        column_stretch = [len(self.before_steps)] if self.is_horizontal else [0]
        self._apply_frame_stretch(rows=row_stretch, columns=column_stretch)

        row_index, column_index = 0, 0

        if self.is_horizontal:
            for step_label, step_amount in self.before_steps:
                button = Button(
                    self._frame, text=step_label,
                    command=partial(self._handle_click, step_amount), **self.styles["button"]
                )
                self.children["before_buttons"].append(((step_label, step_amount), button))
                button.grid(row=row_index, column=column_index, sticky="nswe")
                column_index += 1

            label = Label(self._frame, textvariable=self._label_var, **self.styles["label"])
            self.children["label"] = label
            label.grid(row=row_index, column=column_index, sticky="nswe")
            column_index += 1

            for step_label, step_amount in self.after_steps:
                button = Button(
                    self._frame, text=step_label,
                    command=partial(self._handle_click, step_amount), **self.styles["button"]
                )
                self.children["after_buttons"].append(((step_label, step_amount), button))
                button.grid(row=row_index, column=column_index, sticky="nswe")
                column_index += 1

        else:
            for step_label, step_amount in self.before_steps:
                button = Button(
                    self._frame, text=step_label,
                    command=partial(self._handle_click, step_amount), **self.styles["button"]
                )
                self.children["before_buttons"].append(((step_label, step_amount), button))
                button.grid(row=row_index, column=column_index, sticky="nswe")
                row_index += 1

            label = Label(self._frame, textvariable=self._label_var, **self.styles["label"])
            self.children["label"] = label
            label.grid(row=row_index, column=column_index, sticky="nswe")
            row_index += 1

            for step_label, step_amount in self.after_steps:
                button = Button(
                    self._frame, text=step_label,
                    command=partial(self._handle_click, step_amount), **self.styles["button"]
                )
                self.children["after_buttons"].append(((step_label, step_amount), button))
                button.grid(row=row_index, column=column_index, sticky="nswe")
                row_index += 1

        self._set_button_states()

    def _handle_click(self, step_amount):
        self.value += step_amount

        # Added for redundancy
        if self.min is not None:
            self.value = max(self.min, self.value)
        if self.max is not None:
            self.value = min(self.max, self.value)

        self._on_change(self, step_amount)

        if self.exists:
            self._update()

    def _set_button_states(self):
        all_buttons = self.children["before_buttons"] + self.children["after_buttons"]

        for (step_label, step_amount), button in all_buttons:
            value_after_button_press = self.value + step_amount

            if (value_after_button_press < self.min) or (value_after_button_press > self.max):
                button.config(state="disabled")
            else:
                button.config(state="normal")

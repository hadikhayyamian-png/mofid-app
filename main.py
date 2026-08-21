import math
import random
from datetime import datetime, timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class ChartWidget(Widget):

    PERIODS = {
        "1D": 1,
        "3D": 3,
        "1W": 7,
        "2W": 14,
        "1M": 30,
        "6M": 180,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data = []
        self.period = 14
        self.start_index = 0
        self.selected_index = None

        self.bind(size=self.redraw, pos=self.redraw)

    def set_data(self, data):
        self.data = data
        self.selected_index = None

        if self.data:
            self.start_index = max(0, len(self.data) - self.period)

        self.redraw()

    def set_period(self, period):
        self.period = self.PERIODS[period]
        self.selected_index = None

        if self.data:
            self.start_index = max(0, len(self.data) - self.period)

        self.redraw()

    def visible_data(self):
        if not self.data:
            return []

        end = min(len(self.data), self.start_index + self.period)
        return self.data[self.start_index:end]

    def redraw(self, *args):
        self.canvas.clear()

        with self.canvas:
            Color(0.055, 0.055, 0.055, 1)
            Rectangle(pos=self.pos, size=self.size)

        visible = self.visible_data()

        if not visible:
            return

        left = self.x + 55
        right = self.right - 20
        bottom = self.y + 45
        top = self.top - 30

        if right <= left or top <= bottom:
            return

        values = []

        for item in visible:
            values.append(item["buy"])
            values.append(item["sell"])

        ymin = min(values)
        ymax = max(values)

        if ymax == ymin:
            ymax += 1
            ymin -= 1

        margin = (ymax - ymin) * 0.1
        ymin -= margin
        ymax += margin

        def x_position(i):
            if len(visible) == 1:
                return (left + right) / 2

            return left + i * (right - left) / (len(visible) - 1)

        def y_position(value):
            return bottom + (value - ymin) / (ymax - ymin) * (top - bottom)

        # Grid
        Color(0.18, 0.18, 0.18, 1)

        for j in range(5):
            y = bottom + j * (top - bottom) / 4
            Line(points=[left, y, right, y], width=1)

        # Buy line
        buy_points = []

        for i, item in enumerate(visible):
            buy_points.extend([x_position(i), y_position(item["buy"])])

        Color(0.25, 0.85, 0.35, 1)

        if len(buy_points) >= 4:
            Line(points=buy_points, width=2)

        # Sell line
        sell_points = []

        for i, item in enumerate(visible):
            sell_points.extend([x_position(i), y_position(item["sell"])])

        Color(0.95, 0.25, 0.25, 1)

        if len(sell_points) >= 4:
            Line(points=sell_points, width=2)

        # Data point markers
        for i, item in enumerate(visible):

            x = x_position(i)

            Color(0.25, 0.85, 0.35, 1)
            Ellipse(
                pos=(x - 4, y_position(item["buy"]) - 4),
                size=(8, 8)
            )

            Color(0.95, 0.25, 0.25, 1)
            Ellipse(
                pos=(x - 4, y_position(item["sell"]) - 4),
                size=(8, 8)
            )

        # Selected point
        if self.selected_index is not None:
            local_index = self.selected_index - self.start_index

            if 0 <= local_index < len(visible):

                item = self.data[self.selected_index]
                x = x_position(local_index)

                Color(1, 1, 1, 1)
                Line(
                    points=[x, bottom, x, top],
                    width=1
                )

                Color(1, 1, 1, 1)

                Ellipse(
                    pos=(x - 7, y_position(item["buy"]) - 7),
                    size=(14, 14)
                )

                Ellipse(
                    pos=(x - 7, y_position(item["sell"]) - 7),
                    size=(14, 14)
                )

    def on_touch_down(self, touch):

        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        visible = self.visible_data()

        if not visible:
            return True

        left = self.x + 55
        right = self.right - 20

        if right <= left:
            return True

        # Find closest data point.
        best_index = None
        best_distance = float("inf")

        for i in range(len(visible)):

            if len(visible) == 1:
                x = (left + right) / 2
            else:
                x = left + i * (right - left) / (len(visible) - 1)

            distance = abs(touch.x - x)

            if distance < best_distance:
                best_distance = distance
                best_index = i

        if best_index is not None and best_distance <= 40:

            self.selected_index = self.start_index + best_index

            self.redraw()

            item = self.data[self.selected_index]

            app = App.get_running_app()

            app.show_point_information(item)

            return True

        return True

    def on_touch_move(self, touch):

        if not self.collide_point(*touch.pos):
            return True

        if not hasattr(self, "_last_touch_x"):
            self._last_touch_x = touch.x
            return True

        dx = touch.x - self._last_touch_x

        if abs(dx) >= 8:

            shift = -1 if dx > 0 else 1

            new_start = self.start_index + shift

            maximum = max(0, len(self.data) - self.period)

            new_start = max(0, min(new_start, maximum))

            if new_start != self.start_index:
                self.start_index = new_start
                self.selected_index = None
                self.redraw()

            self._last_touch_x = touch.x

        return True

    def on_touch_up(self, touch):

        self._last_touch_x = None

        return True


class MofidApp(App):

    def build(self):

        self.title = "Mofid Tracker"

        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        with root.canvas.before:
            Color(0.035, 0.035, 0.035, 1)
            self.background = Rectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=lambda obj, value: setattr(
                self.background, "pos", value
            ),
            size=lambda obj, value: setattr(
                self.background, "size", value
            )
        )

        # Title
        title = Label(
            text="Mofid Funds - Money Flow Tracker",
            font_size="19sp",
            bold=True,
            size_hint_y=None,
            height=45
        )

        root.add_widget(title)

        # Symbol selection
        symbol_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=45,
            spacing=5
        )

        self.symbol_input = TextInput(
            text="Etemas",
            hint_text="Enter نماد",
            multiline=False,
            size_hint_x=0.65
        )

        add_button = Button(
            text="+ Add نماد",
            size_hint_x=0.35
        )

        add_button.bind(on_press=self.add_symbol)

        symbol_row.add_widget(self.symbol_input)
        symbol_row.add_widget(add_button)

        root.add_widget(symbol_row)

        # Symbol list
        self.symbols = [
            "Etemas",
            "Nami",
            "Aram",
            "Momtaz"
        ]

        self.symbol_buttons = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=40,
            spacing=4
        )

        root.add_widget(self.symbol_buttons)

        self.refresh_symbol_buttons()

        # Chart
        self.chart = ChartWidget()

        root.add_widget(self.chart)

        # Information area
        self.info_label = Label(
            text="Tap a data point to see its value.",
            size_hint_y=None,
            height=55,
            halign="center",
            valign="middle"
        )

        self.info_label.bind(
            size=lambda obj, value: setattr(
                obj, "text_size", value
            )
        )

        root.add_widget(self.info_label)

        # Period buttons
        period_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=45,
            spacing=3
        )

        for period in ["1D", "3D", "1W", "2W", "1M", "6M"]:

            button = Button(text=period)

            button.bind(
                on_press=lambda instance,
                p=period: self.change_period(p)
            )

            period_row.add_widget(button)

        root.add_widget(period_row)

        self.current_symbol = "Etemas"

        self.load_symbol(self.current_symbol)

        return root

    def generate_mock_data(self, days=180):

        data = []

        base_buy = 350
        base_sell = 300

       

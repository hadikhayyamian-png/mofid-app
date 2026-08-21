from kivy_garden.graph import Graph, MeshLinePlot

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import random


class TouchPanGraph(Graph):

    def __init__(self, **kwargs):
        super(TouchPanGraph, self).__init__(**kwargs)

        self.total_points = 60
        self.touch_start_x = 0
        self.view_span = 15

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            self.touch_start_x = touch.x
            touch.grab(self)
            return True

        return super(TouchPanGraph, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        if touch.grab_current is self:

            dx = touch.x - self.touch_start_x
            shift = int(dx / 30)

            if shift != 0:

                new_xmin = self.xmin - shift
                new_xmax = self.xmax - shift

                if new_xmin >= 0 and new_xmax <= self.total_points:
                    self.xmin = new_xmin
                    self.xmax = new_xmax
                    self.touch_start_x = touch.x

            return True

        return super(TouchPanGraph, self).on_touch_move(touch)

    def on_touch_up(self, touch):

        if touch.grab_current is self:
            touch.ungrab(self)
            return True

        return super(TouchPanGraph, self).on_touch_up(touch)


class EnhancedGraphApp(App):

    def build(self):

        self.root_layout = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=10
        )

        with self.root_layout.canvas.before:
            Color(0.07, 0.07, 0.07, 1)

            self.rect = Rectangle(
                size=self.root_layout.size,
                pos=self.root_layout.pos
            )

        self.root_layout.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        title = Label(
            text="Mofid Funds - Legal Money Flow Tracker",
            font_size='18sp',
            size_hint_y=0.08,
            bold=True
        )

        self.root_layout.add_widget(title)

        selector_row = GridLayout(
            cols=2,
            size_hint_y=0.08,
            spacing=10
        )

        selector_row.add_widget(
            Label(
                text="Select Fund:",
                size_hint_x=0.3,
                halign='right'
            )
        )

        self.fund_spinner = Spinner(
            text='Etemas (اتماس)',
            values=(
                'Etemas (اتماس)',
                'Nami (نامی)',
                'Aram (آرام)',
                'Momtaz (ممتاز)'
            ),
            size_hint_x=0.7,
            background_color=(0.15, 0.15, 0.15, 1)
        )

        self.fund_spinner.bind(
            text=self.on_fund_change
        )

        selector_row.add_widget(
            self.fund_spinner
        )

        self.root_layout.add_widget(
            selector_row
        )

        self.total_points = 60

        self.buy_data = [
            random.randint(150, 550)
            for _ in range(self.total_points)
        ]

        self.sell_data = [
            random.randint(100, 500)
            for _ in range(self.total_points)
        ]

        self.graph = TouchPanGraph(
            xlabel='Trading Days (Past -> Present)',
            ylabel='Billion Rials',
            x_ticks_major=5,
            y_ticks_major=100,
            y_grid_label=True,
            x_grid_label=True,
            padding=10,
            x_grid=True,
            y_grid=True,
            xmin=self.total_points - 15,
            xmax=self.total_points,
            ymin=0,
            ymax=600,
            draw_border=False,
            background_color=(0.1, 0.1, 0.1, 1),
            label_options={
                'color': [1, 1, 1, 1]
            }
        )

        self.graph.total_points = self.total_points

        self.root_layout.add_widget(
            self.graph
        )

        legend_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.05,
            spacing=20
        )

        legend_row.add_widget(
            Label(
                text="● Legal Buy Volume (Green)",
                color=(0.3, 0.85, 0.3, 1),
                font_size='12sp'
            )
        )

        legend_row.add_widget(
            Label(
                text="● Legal Sell Volume (Red)",
                color=(0.95, 0.25, 0.25, 1),
                font_size='12sp'
            )
        )

        self.root_layout.add_widget(
            legend_row
        )

        control_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.08,
            spacing=10
        )

        instruction_label = Label(
            text="Drag directly on the chart area to slide weeks",
            font_size='12sp',
            size_hint_x=0.7
        )

        btn_reset = Button(
            text="Reset View",
            on_press=self.reset_view,
            background_color=(0.3, 0.3, 0.3, 1),
            size_hint_x=0.3
        )

        control_row.add_widget(
            instruction_label
        )

        control_row.add_widget(
            btn_reset
        )

        self.root_layout.add_widget(
            control_row
        )

        self.plot_buy = MeshLinePlot(
            color=[0.3, 0.85, 0.3, 1]
        )

        self.plot_sell = MeshLinePlot(
            color=[0.95, 0.25, 0.25, 1]
        )

        self.graph.add_plot(
            self.plot_buy
        )

        self.graph.add_plot(
            self.plot_sell
        )

        self.update_plots()

        return self.root_layout

    def update_plots(self):

        self.plot_buy.points = [
            (i, self.buy_data[i])
            for i in range(self.total_points)
        ]

        self.plot_sell.points = [
            (i, self.sell_data[i])
            for i in range(self.total_points)
        ]

    def reset_view(self, instance):

        self.graph.xmin = self.total_points - 15
        self.graph.xmax = self.total_points

    def on_fund_change(self, spinner, text):

        self.buy_data = [
            random.randint(150, 550)
            for _ in range(self.total_points)
        ]

        self.sell_data = [
            random.randint(100, 500)
            for _ in range(self.total_points)
        ]

        self.update_plots()
        self.reset_view(None)

    def _update_rect(self, instance, value):

        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    EnhancedGraphApp().run()

import os
import deepdish as dd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation


class SubplotAnimation(animation.TimedAnimation):
    def __init__(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2, sharex=ax1)
        ax3 = fig.add_subplot(3, 1, 3, sharex=ax1)

        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax3 = ax3

        self.t = np.linspace(0, 10, 1000)
        self.x = np.zeros(self.t.shape)
        self.y = np.zeros(self.t.shape)
        self.z = np.zeros(self.t.shape)

        ax1.set_ylabel('x')
        self.line1 = Line2D([], [], color='black')
        ax1.add_line(self.line1)
        ax1.set_ylim(-0.1, 0.1)
        # ax1.set_aspect('equal', 'datalim')

        ax2.set_ylabel('y')
        self.line2 = Line2D([], [], color='black')
        ax2.add_line(self.line2)
        ax2.set_ylim(-0.1, 0.1)

        ax3.set_ylabel('z')
        ax3.set_xlabel('Time (sec)')
        self.line3 = Line2D([], [], color='black')
        ax3.add_line(self.line3)
        ax3.set_ylim(-0.1, 0.1)
        ax3.set_xlim(0, 10)

        animation.TimedAnimation.__init__(self, fig, interval=200, blit=True)

    def _draw_frame(self, frame_num):
        i = frame_num

        self.ax1.set_title("Frame #{}".format(i + 1))
        print("Processing frame #{}".format(i + 1))

        # Load data
        for root, dirs, files in os.walk('tmp/train/events'):
            file = files[i]
            label, data_mtx = dd.io.load("/".join((root, file)))
            data_mtx -= data_mtx.mean(axis=1, keepdims=True)
            self.x = data_mtx[0]
            self.y = data_mtx[1]
            self.z = data_mtx[2]

            # print(self.x.shape, self.y.shape, self.z.shape)

        # Update data
        self.line1.set_data(self.t, self.x)
        self.line2.set_data(self.t, self.y)
        self.line3.set_data(self.t, self.z)

        # Update y axis range
        update_range = True
        if update_range:
            yrange = np.max(np.abs(data_mtx))
            self.ax1.set_ylim(-yrange, yrange)
            self.ax2.set_ylim(-yrange, yrange)
            self.ax3.set_ylim(-yrange, yrange)

        self._drawn_artists = [self.line1, self.line2, self.line3]

        self.fig.canvas.set_window_title("Frame #{}".format(i))

    def new_frame_seq(self):
        return iter(range(1842))

    def _init_draw(self):
        lines = [self.line1, self.line2, self.line3]
        for l in lines:
            l.set_data([], [])


ani = SubplotAnimation()
ani.save('tmp/video/events_dynamic_y_range.mp4')
# plt.show()

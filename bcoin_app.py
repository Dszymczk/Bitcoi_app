# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/
# Powered by CoinDesk
# https://www.coindesk.com/price/bitcoin
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import urllib
import json
import pandas as pd
import numpy as np

style.use('ggplot')
matplotlib.use("TkAgg")

LARGE_FONT = ("Verdana", 12)

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)


def animate(i):
    # pullData = open('sampleText.txt', 'r').read()
    # dataArray = pullData.split('\n')
    # xar = []
    # yar = []
    # for eachLine in dataArray:
    #     if len(eachLine)>1:
    #         try:
    #             x, y = eachLine.split(',')
    #             xar.append(int(x))
    #             yar.append(int(y))
    #         except ValueError:
    #             print("Wrong data input")
    # a.clear()
    # a.plot(xar, yar)
    dataLink = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    data = urllib.request.urlopen(dataLink)
    data = data.readall().decode("utf-8")
    data = json.loads(data)

    data = data['bpi']['USD']['rate_float']
    data = pd.DataFrame(data)

    buys = data[(data['type'] == "bid")]
    buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()

    sells = data[(data['type'] == "ask")]
    sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()

    a.clear()

    a.plot_date(buyDates, buys["price"])
    a.plot_date(sellDates, sells["price"])

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default='clienticon.ico')
        tk.Tk.wm_title(self, "Sea of BTC Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("""ALPHA Bitcoin trading application
        use at your own risk. There is no promise
        of warranty."""), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the page 1", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Visit Start Page",
                           command=lambda: controller.show_frame(StartPage))
        button.pack()
        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the page 2", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Visit Page 1",
                           command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = tk.Button(self, text="Visit Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()


class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # f = Figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111)
        # t = arange(0.0, 3.0, 0.01)
        # s = sin(2 * pi * t)
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def qf(quickPrint):
    print(quickPrint)


app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()

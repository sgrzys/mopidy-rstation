from Tkinter import Button, Checkbutton, DISABLED, Tk
from threading import Thread


class IrdaSimulator():
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.playing_led = None
        thread = Thread(target=self.initial_simulator)
        thread.start()

    def initial_simulator(self):
        root = Tk()
        root.title("Irda Simulator")
        ch_minus = Button(root, text="CH-", command=self.ch_minus)
        ch = Button(root, text="CH", command=self.ch)
        ch_plus = Button(root, text="CH+", command=self.ch_plus)
        prev = Button(root, text="|<<", command=self.prev)
        next = Button(root, text=">>|", command=self.next)
        play_pause = Button(root, text=">||", command=self.play_pause)
        vol_down = Button(root, text="vol -", command=self.vol_down)
        vol_up = Button(root, text="vol +", command=self.vol_up)
        eq = Button(root, text="EQ", command=self.eq)
        num0 = Button(root, text="0", command=self.num0)
        fl_minus = Button(root, text="FL-", command=self.fl_minus)
        fl_plus = Button(root, text="FL+", command=self.fl_plus)
        num1 = Button(root, text="1", command=self.num1)
        num2 = Button(root, text="2", command=self.num2)
        num3 = Button(root, text="3", command=self.num3)
        num4 = Button(root, text="4", command=self.num4)
        num5 = Button(root, text="5", command=self.num5)
        num6 = Button(root, text="6", command=self.num6)
        num7 = Button(root, text="7", command=self.num7)
        num8 = Button(root, text="8", command=self.num8)
        num9 = Button(root, text="9", command=self.num9)
        self.playing_led = Checkbutton(text="playing_led", state=DISABLED)

        ch_minus.grid(row=0, column=1)
        ch.grid(row=0, column=2)
        ch_plus.grid(row=0, column=3)
        prev.grid(row=1, column=1)
        next.grid(row=1, column=2)
        play_pause.grid(row=1, column=3)
        vol_down.grid(row=2, column=1)
        vol_up.grid(row=2, column=2)
        eq.grid(row=2, column=3)
        num0.grid(row=3, column=1)
        fl_minus.grid(row=3, column=2)
        fl_plus.grid(row=3, column=3)
        num1.grid(row=4, column=1)
        num2.grid(row=4, column=2)
        num3.grid(row=4, column=3)
        num4.grid(row=5, column=1)
        num5.grid(row=5, column=2)
        num6.grid(row=5, column=3)
        num7.grid(row=6, column=1)
        num8.grid(row=6, column=2)
        num9.grid(row=6, column=3)
        self.playing_led.grid(row=7, column=1)

        root.mainloop()

    def ch_minus(self):
        self.dispatcher.handleCommand('ch_minus')

    def ch(self):
        self.dispatcher.handleCommand('ch')

    def ch_plus(self):
        self.dispatcher.handleCommand('ch_plus')

    def prev(self):
        self.dispatcher.handleCommand('prev')

    def next(self):
        self.dispatcher.handleCommand('next')

    def play_pause(self):
        self.dispatcher.handleCommand('play_pause')

    def vol_down(self):
        self.dispatcher.handleCommand('vol_down')

    def vol_up(self):
        self.dispatcher.handleCommand('vol_up')

    def eq(self):
        self.dispatcher.handleCommand('eq')

    def num0(self):
        self.dispatcher.handleCommand('num0')

    def fl_minus(self):
        self.dispatcher.handleCommand('fl_minus')

    def fl_plus(self):
        self.dispatcher.handleCommand('fl_plus')

    def num1(self):
        self.dispatcher.handleCommand('num1')

    def num2(self):
        self.dispatcher.handleCommand('num2')

    def num3(self):
        self.dispatcher.handleCommand('num3')

    def num4(self):
        self.dispatcher.handleCommand('num4')

    def num5(self):
        self.dispatcher.handleCommand('num5')

    def num6(self):
        self.dispatcher.handleCommand('num6')

    def num7(self):
        self.dispatcher.handleCommand('num7')

    def num8(self):
        self.dispatcher.handleCommand('num8')

    def num9(self):
        self.dispatcher.handleCommand('num9')

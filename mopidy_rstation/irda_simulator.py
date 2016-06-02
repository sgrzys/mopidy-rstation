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
        previous = Button(root, text="Previous", command=self.previous)
        main = Button(root, text="Main button", command=self.main)
        next = Button(root, text="Next", command=self.next)
        vol_up = Button(root, text="Vol +", command=self.vol_up)
        vol_up_long = Button(root, text="Vol + long", command=self.vol_up_long)
        vol_down = Button(root, text="Vol -", command=self.vol_down)
        vol_down_long = Button(root, text="Vol - long",
                               command=self.vol_down_long)
        main_long = Button(root, text="Main long", command=self.main_long)
        self.playing_led = Checkbutton(text="playing_led", state=DISABLED)

        vol_up.grid(row=0, column=1)
        vol_up_long.grid(row=0, column=2)
        previous.grid(row=1, column=0)
        main.grid(row=1, column=1)
        main_long.grid(row=1, column=2)
        next.grid(row=1, column=3)
        vol_down.grid(row=2, column=1)
        vol_down_long.grid(row=2, column=2)
        self.playing_led.grid(row=3, column=1)

        root.mainloop()

    def previous(self):
        self.dispatcher.handleCommand('previous')

    def main(self):
        self.dispatcher.handleCommand({'key': 'main', 'long': False})

    def main_long(self):
        self.dispatcher.handleCommand({'key': 'main', 'long': True})

    def next(self):
        self.dispatcher.handleCommand('next')

    def vol_up(self):
        self.dispatcher.handleCommand('volumeup')

    def vol_down(self):
        self.dispatcher.handleCommand('volumedown')

    def vol_down_long(self):
        self.dispatcher.handleCommand('volumeup')

    def vol_up_long(self):
        self.dispatcher.handleCommand({'key': 'volume_up', 'long': True})

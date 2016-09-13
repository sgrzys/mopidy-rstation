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
        track_list_prev = Button(
            root, text="CH-", command=self.track_list_prev)
        track_list_enter = Button(
            root, text="CH", command=self.track_list_enter)
        track_list_next = Button(
            root, text="CH+", command=self.track_list_next)
        player_prev = Button(root, text="|<<", command=self.player_prev)
        player_next = Button(root, text=">>|", command=self.player_next)
        player_play_pause = Button(
            root, text=">||", command=self.player_play_pause)
        vol_down = Button(root, text="vol -", command=self.vol_down)
        vol_up = Button(root, text="vol +", command=self.vol_up)
        change_lang = Button(root, text="EQ", command=self.change_lang)
        num0 = Button(root, text="0", command=self.num0)
        backlight_down = Button(root, text="FL-", command=self.backlight_down)
        backlight_up = Button(root, text="FL+", command=self.backlight_up)
        num1 = Button(root, text="1", command=self.num1)
        lib_root_dir = Button(root, text="2", command=self.lib_root_dir)
        num3 = Button(root, text="3", command=self.num3)
        lib_prev = Button(root, text="4", command=self.lib_prev)
        lib_enter = Button(root, text="5", command=self.lib_enter)
        lib_next = Button(root, text="6", command=self.lib_next)
        lib_audiobook = Button(root, text="7", command=self.lib_audiobook)
        lib_radio = Button(root, text="8", command=self.lib_radio)
        lib_music = Button(root, text="9", command=self.lib_music)
        self.playing_led = Checkbutton(text="playing_led", state=DISABLED)

        track_list_prev.grid(row=0, column=1)
        track_list_enter.grid(row=0, column=2)
        track_list_next.grid(row=0, column=3)
        player_prev.grid(row=1, column=1)
        player_next.grid(row=1, column=2)
        player_play_pause.grid(row=1, column=3)
        vol_down.grid(row=2, column=1)
        vol_up.grid(row=2, column=2)
        change_lang.grid(row=2, column=3)
        num0.grid(row=3, column=1)
        backlight_down.grid(row=3, column=2)
        backlight_up.grid(row=3, column=3)
        num1.grid(row=4, column=1)
        lib_root_dir.grid(row=4, column=2)
        num3.grid(row=4, column=3)
        lib_prev.grid(row=5, column=1)
        lib_enter.grid(row=5, column=2)
        lib_next.grid(row=5, column=3)
        lib_audiobook.grid(row=6, column=1)
        lib_radio.grid(row=6, column=2)
        lib_music.grid(row=6, column=3)
        self.playing_led.grid(row=7, column=1)

        root.mainloop()

    def track_list_prev(self):
        self.dispatcher.handleCommand('track_list_prev')

    def track_list_enter(self):
        self.dispatcher.handleCommand('ch')

    def track_list_next(self):
        self.dispatcher.handleCommand('track_list_next')

    def player_prev(self):
        self.dispatcher.handleCommand('prev')

    def player_next(self):
        self.dispatcher.handleCommand('next')

    def player_play_pause(self):
        self.dispatcher.handleCommand('player_play_pause')

    def vol_down(self):
        self.dispatcher.handleCommand('vol_down')

    def vol_up(self):
        self.dispatcher.handleCommand('vol_up')

    def change_lang(self):
        self.dispatcher.handleCommand('eq')

    def num0(self):
        self.dispatcher.handleCommand('num0')

    def backlight_down(self):
        self.dispatcher.handleCommand('backlight_down')

    def backlight_up(self):
        self.dispatcher.handleCommand('backlight_up')

    def num1(self):
        self.dispatcher.handleCommand('num1')

    def lib_root_dir(self):
        self.dispatcher.handleCommand('lib_root_dir')

    def num3(self):
        self.dispatcher.handleCommand('num3')

    def lib_prev(self):
        self.dispatcher.handleCommand('lib_prev')

    def lib_enter(self):
        self.dispatcher.handleCommand('lib_enter')

    def lib_next(self):
        self.dispatcher.handleCommand('lib_next')

    def lib_audiobook(self):
        self.dispatcher.handleCommand('lib_audiobook')

    def lib_radio(self):
        self.dispatcher.handleCommand('lib_radio')

    def lib_music(self):
        self.dispatcher.handleCommand('lib_music')

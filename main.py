from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

from PhaseEncodingAudioStego import PhaseEncodingAudioStego


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        # init TITle, giao diện mã hóa, giải mã
        self.master.title("Mã Hóa Pha Âm Thanh")
        self.pack(fill=BOTH, expand=1)
        self.drawEnocoding()
        self.drawDecoding()

    def drawEnocoding(self):
        # encode Label
        self.encodeVar = StringVar()
        self.encodelabel = Label(root, textvariable=self.encodeVar)
        self.encodelabel.place(x=10, y=10)
        self.encodeVar.set("Mã Hóa ")
        # creating a button instance
        self.selectFileButton = Button(self, text=" Chọn File để mã hóa ", command=self.selectFile)
        self.selectFileButton.place(x=10, y=60)

        # file location label
        self.var = StringVar()
        self.label = Label(root, textvariable=self.var, relief=RAISED)
        self.label.place(x=10, y=90)
        # placing the button on my window

        # entry box
        self.entryText = Entry(root)
        self.entryText.place(x=10, y=140)
        self.entryText.insert(0, "Thong diep ma hoa ")
        # encode Button
        self.encodeButton = Button(self, text="Mã Hóa", command=self.encode)
        self.encodeButton.place(x=10, y=180)

        # encoded  location label
        self.enocdedLocation = StringVar()
        self.locationOfEncodeFile = Label(root, textvariable=self.enocdedLocation)
        self.locationOfEncodeFile.place(x=10, y=240)

    def drawDecoding(self):
        # decode Label
        self.decodeVar = StringVar()
        self.decodelabel = Label(root, textvariable=self.decodeVar)
        self.decodelabel.place(x=500, y=10)
        self.decodeVar.set("Giải mã ")

        # select algo
        # self.decodeOptionsVar = StringVar()
        # self.decodeOptionsVar.set("Mã Hóa Pha")  # default value
        #
        # self.decodingOptionsMenu = OptionMenu(root, self.decodeOptionsVar)
        # self.decodingOptionsMenu.place(x=500, y=50)
        # creating a button instance
        self.selectFileDecodeButton = Button(self, text="Chọn File cần giải mã ", command=self.selectFileDecode)
        self.selectFileDecodeButton.place(x=500, y=60)
        #
        # file location label
        self.decodeFileVar = StringVar()
        self.decodeFileLabel = Label(root, textvariable=self.decodeFileVar, relief=RAISED)
        self.decodeFileLabel.place(x=500, y=100)

        self.decodeButton = Button(self, text="Giải Mã", command=self.decode)
        self.decodeButton.place(x=500, y=160)
        #
        # decoded text label
        self.decodedString = StringVar()
        self.decodedStringlabel = Label(root, textvariable=self.decodedString, font=(None, 40))
        self.decodedStringlabel.place(x=500, y=310)

    def client_exit(self):
        exit()

    def selectFile(self):
        # file selection
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelected = root.filename
        self.var.set(root.filename)

    def selectFileDecode(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelcetedForDecode = root.filename
        self.decodeFileVar.set(root.filename)

    def encode(self):
        algo = PhaseEncodingAudioStego()
        result = algo.encodeAudio(self.fileSelected, self.entryText.get())
        self.enocdedLocation.set(result)

    def decode(self):
        algo = PhaseEncodingAudioStego()
        result = algo.decodeAudio(self.fileSelcetedForDecode)
        self.decodedString.set(result)


# resolution
root = Tk()
root.geometry("700x700")
# instance of window
app = Window(root)
# mainloop
root.mainloop()

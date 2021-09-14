from abc import abstractproperty
from tkinter import Button, Entry, Frame, Label, Text
from tkinter.constants import CENTER, DISABLED, FLAT, LEFT, RAISED, SUNKEN, WORD


def createIcon(app, title, img, command):
    icon = Button(app, text=title,
                  font='Poppins',
                  image=img,
                  highlightthickness=0,
                  relief='flat',
                  bd=0,
                  bg="#ccc",
                  #   activebackground='#fff',
                  cursor='hand2',
                  command=command,
                  )
    return icon


def createFormalButton(app, title, command):
    button = Button(app, text=title,
                    font='Poppins',
                    padx=16,
                    pady=16,
                    width=16,
                    bg='#ddd',
                    highlightthickness=0,
                    relief='flat',
                    bd=0,
                    activebackground='red',
                    cursor='hand2',
                    command=command
                    )
    return button


def createLabel(app, text, font):
    label = Label(app,
                  relief='flat',
                  text=text,
                  bg='#ccc',
                  fg='#000',
                  padx=16,
                  pady=16,
                  font=font,
                  highlightthickness=0,
                  bd=0,
                  justify=LEFT,
                  wraplength=500
                  )
    return label


def createInput(app):
    input = Entry(app, bd=0, font=('Poppins, 12'),
                  bg='#eee', relief=FLAT, borderwidth=8)
    return input


def createText(app, f):
    text = Text(app, font=f, autoseparators=True,
                setgrid=True, wrap=WORD)
    return text


def createFrame(app):
    frame = Frame(app, bg='#ccc')
    return frame

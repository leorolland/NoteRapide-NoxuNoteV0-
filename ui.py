# coding=utf8
from tkinter import *
import tkinter.filedialog
import tkinter.scrolledtext as tkst
import os

bg = '#D9D8D9'

win = Tk()

frame1 = Frame(
    master = win,
    bg = '#C3C1C3'
)

textArea = tkst.ScrolledText(
    master    = frame1,
    wrap    = WORD,
    width    = 121,
    height    = 34,
    undo    = 1,
    maxundo    = 15,
    borderwidth = 5,
    bg = "#333333",
    foreground = "#FFFFFF"
)

# Tags configuration
textArea.tag_configure('blue', foreground='#60D9F1')
textArea.tag_configure('red', foreground='#FC1E70')
textArea.tag_configure('yellow', foreground='#E6DC6D')

def setText(texte='Erreur de chargement'):
    textArea.delete("1.0", END)
    textArea.insert(END, texte)

# Définition de la fenêtre graphique
win.minsize(width=898, height=602)
win.maxsize(width=898, height=602)
win.title('Note Rapide')
win.configure(background=bg)

# TextArea
# textArea = scrollTxtArea(win)
frame1.grid(row=1,column=0, columnspan=5)
textArea.pack(padx=10, pady=10, fill=BOTH, expand=True)

# File title
labelNom = Label(text='Nom : ', background=bg)
labelNom.grid(row=0,column=0,sticky='e', pady=5)
nomFichier = Text(win, height=1, width=25)
nomFichier.grid(row=0, column=1, pady=5,sticky='w')

# Informations bas de fenetre
labelWordCount = Label(text="0 mots, 0 caractères", background=bg)
labelWordCount.grid(row=2,column=0, sticky='w')

# Génération
def enregistrer():
    rawtext = textArea.get("1.0", END)
    name = nomFichier.get("1.0", END).replace("\n",'').replace(' ','_')
    note = open("/Users/blacky/Documents/cours/notes/nt_%s.txt"%(name), "w", encoding="utf-8")
    note.write(rawtext)
    note.close()
    print("Enregistrement effectué avec succès !")

def generate():
    enregistrer()
    name = nomFichier.get("1.0", END).replace("\n",'').replace(' ','_')
    os.system('python3 main.py "%s"'%(name))
    os.system('open /Users/blacky/Documents/cours/pdfs/%s.pdf'%(name))

def checkCode():
    rawtext = textArea.get("1.0", END)
    textArea.delete("1.0", END)

    twodot = False # Vrai dès que l'on détecte un ":"

    for line in rawtext:
        for character in line:

            if twodot: # Si le caractère suivant fait parti du twodot
                if character == ' ': # Dans le cas d'un espace on ne fait rien et on réinitialise la variable
                    twodot = False
                    textArea.insert(END, ' ')
                else:
                    textArea.insert(END, character, "blue") # Sinon on met le texte en bleu

            elif character == '#':
                textArea.insert(END, character, "red")

            elif character == '_':
                textArea.insert(END, character, "blue")

            elif character == '*':
                textArea.insert(END, character, "blue")

            elif character == '|':
                textArea.insert(END, character, "yellow")

            elif character == '[':
                textArea.insert(END, character, "yellow")

            elif character == ']':
                textArea.insert(END, character, "yellow")

            elif character == ':':
                twodot = True
                textArea.insert(END, character, "blue")

            else:
                textArea.insert(END, character)

def ouvrir():
    enregistrer()
    options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    filename = tkinter.filedialog.askopenfilename(**options)

    note = open(filename, "r", encoding='utf-8').read()
    setText(note)
    nomFichier.delete("1.0", END)
    filename = filename.split('/')[-1].replace('.txt','').replace('nt_','')
    nomFichier.insert(END, filename)

    checkCode()

title = False

def onKeyPress(event):
    try:
        rawtext = textArea.get("1.0", END)
        characterCount = len(rawtext)-1
        wordCount = len(rawtext.split(' '))-1
        labelWordCount.configure(text='%s mots, %s caractères'%(wordCount, characterCount))

        if event.char == '#':
            textArea.delete("insert-1c", "insert")
            textArea.insert("insert", event.char, "red")

        elif event.char == '_':
            textArea.delete("insert-1c", "insert")
            textArea.insert("insert", event.char, "blue")

        elif event.char == '*':
            textArea.delete("insert-1c", "insert")
            textArea.insert("insert", event.char, "blue")

        elif event.char == '|':
            textArea.delete("insert-1c", "insert")
            textArea.insert("insert", event.char, "yellow")

        elif event.char == "[":
            textArea.delete("insert-1c", "insert")
            textArea.insert("insert", event.char, "yellow")

        elif event.char == "[":
            textArea.delete("insert-1c", "insert")
            textArea.insert("insert", event.char, "yellow")

    except Exception:
        pass

enregistrerButton = Button(win, text="Enregistrer", command=enregistrer)
enregistrerButton.grid(row=0, column=2, pady=5,sticky='w')
generateButton = Button(win, text="Générer le PDF", command=generate)
generateButton.grid(row=0, column=4, pady=5,sticky='w')
ouvrirButton = Button(win, text="Ouvrir", command=ouvrir)
ouvrirButton.grid(row=0, column=3,sticky='w')

win.bind_all('<Key>', onKeyPress)

textArea.insert(END, "manuscrit\n")

win.mainloop()
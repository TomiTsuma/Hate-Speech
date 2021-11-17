import tkinter as tk
from prepareText import prepareText
import pickle
import numpy as np

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Determine the presence of Hate Speech')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Enter your text:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)
loaded_model = pickle.load(open('HateSpeech.sav', 'rb'))

sample_text = tk.Entry(root)
sample_text.pack()

def pred():
    x1 = entry1.get()
    array =  prepareText(x1)
    prediction = loaded_model.predict([array])
    sample_text.insert(0, prediction)

    return(prediction)
    

    
    
    
    
button1 = tk.Button(text='Perform prediction', command=pred, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()
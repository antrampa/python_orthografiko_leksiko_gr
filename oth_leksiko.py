from tkinter import *

# Create window object
app = Tk()

# Fields
# Correct word
c_word = StringVar()
c_word_label = Label(app, text="Λέξη", font=('Bold', 14), pady=20, padx=20)
c_word_label.grid(row=0, column=0, sticky=W)
c_word_entry = Entry(app, textvariable=c_word)
c_word_entry.grid(row=0, column=1)
# Extra info
e_info = StringVar()
e_info_label = Label(app, text="Πληροφορίες",
                     font=('Bold', 14), padx=20)
e_info_label.grid(row=0, column=2, sticky=W)
e_info_entry = Entry(app, textvariable=e_info)
e_info_entry.grid(row=0, column=3)
# wrong_word
wrong_word = StringVar()
wrong_word_label = Label(app, text="Λάθος Ορθογραφία (,)",
                         font=('Bold', 14), padx=20)
wrong_word_label.grid(row=1, column=0, sticky=W)
wrong_word_entry = Entry(app, textvariable=wrong_word)
wrong_word_entry.grid(row=1, column=1)

# Words
words_list = Listbox(app, height=8, width=80, border=0)
words_list.grid(row=3, column=0, columnspan=4,
                rowspan=6, padx=20, pady=20, sticky=W)


app.title('Ελληνικό Ορθογραφικό Λεξικό')
app.geometry("800x550")

# Start application
app.mainloop()

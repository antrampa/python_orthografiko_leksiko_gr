from tkinter import *

# functions


def populate_list():
    print('Populate list')


def add_word():
    print("Add")


def remove_word():
    print("Remove")


def update_word():
    print("Update")


def clear_text():
    print("Clear")


# Create window object
app = Tk()

# Fields
# Correct word
c_word = StringVar()
c_word_label = Label(app, text="Λέξη", font=('Bold', 14), pady=20, padx=20)
c_word_label.grid(row=0, column=0, sticky=W)
c_word_entry = Entry(app, width=20, textvariable=c_word)
c_word_entry.grid(row=0, column=1, sticky=W)
# Extra info
e_info = StringVar()
e_info_label = Label(app, text="Πληροφορίες",
                     font=('Bold', 14), padx=20)
e_info_label.grid(row=0, column=2, sticky=W)
e_info_entry = Entry(app, width=10, textvariable=e_info)
e_info_entry.grid(row=0, column=3, sticky=W)
# wrong_word
wrong_word = StringVar()
wrong_word_label = Label(app, text="Λάθος Ορθογραφία (,)",
                         font=('Bold', 14), padx=20)
wrong_word_label.grid(row=1, column=0, sticky=W)
wrong_word_entry = Entry(app, width=50, textvariable=wrong_word)
wrong_word_entry.grid(row=1, column=1, columnspan=3, sticky=W)

# Words
words_list = Listbox(app, height=8, width=80, border=0)
words_list.grid(row=3, column=0, columnspan=4,
                rowspan=6, padx=20, pady=20, sticky=W)

# Scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=4)
words_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=words_list.yview)

# Buttons
add_btn = Button(app, text="Καταχώρηση", width=12, command=add_word)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text="Διαγραφή", width=12, command=remove_word)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text="Ενημέρωση", width=12, command=update_word)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text="Καθαρισμός", width=12, command=clear_text)
clear_btn.grid(row=2, column=3, pady=20)


app.title('Ελληνικό Ορθογραφικό Λεξικό')
app.geometry("800x550")

# Start application
app.mainloop()

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QVBoxLayout, QWidget, QPushButton,QLabel,QListWidget,QLineEdit,QTextEdit,QInputDialog,QHBoxLayout,QBoxLayout,QFormLayout,QMessageBox
from PyQt5.QtGui import QFont
import json
app=QApplication([])
warning=QMessageBox()
warning.setIcon(QMessageBox.Warning)
warning.setWindowTitle("Error")

notes_win=QWidget()
notes_win.setWindowTitle("Розумні замітки")
notes_win.resize(900,600)

list_notes=QListWidget()
list_notes_label=QLabel("Список заміток")

button_note_create=QPushButton("Створити замітку")
button_note_del=QPushButton("Видалити замітку")
button_note_save=QPushButton("Зберегти замітку")

field1_tag=QLineEdit("")
field1_tag.setPlaceholderText("Введіть тег...")
field_tag=QTextEdit()
field_text=QTextEdit()
field_text.setFont(QFont("Comic Sans MS"))
field_text.setStyleSheet("""
        font-size: 18px;
        background-image: url(photo.jpg);
        background-repeat: no-repeat;
""")
button_tag_add = QPushButton("Додати до замітки ")
button_tag_del=QPushButton("Відкрипити від замітки")
button_tag_search=QPushButton("Шукати замітки по тегу")
list_tags=QListWidget()
list_tags_label=QLabel("Список тегів")

layout_notes=QHBoxLayout()
col_1=QVBoxLayout()
col_1.addWidget(field_text)

col_2=QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1=QHBoxLayout()

row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2=QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field1_tag)
row3=QHBoxLayout()
row3.addWidget(button_tag_add)
row3.addWidget(button_tag_del)
row4=QHBoxLayout()
row4.addWidget(button_tag_search)

col_2.addLayout(row3)
col_2.addLayout(row4)
layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)
notes_win.setLayout(layout_notes)
def show_note():
    key=list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])
def add_note():
    note_name,ok=QInputDialog.getText(notes_win,'Додати замітку','Назва замітки')
    if ok and note_name!='':
        notes[note_name]={"текст":"","теги":[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)
def save_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        notes[key]["текст"]=field_text.toPlainText()
        with open("notes_data.json","w") as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        print(notes)
    else:
        warning.setText("Замітка для зберігання не вибрані")
        warning.show()
def del_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json","w") as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        print(notes)
    else:
        warning.setText("Замітка для вилучення не обрана")
        warning.show()
def add_tag():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=field1_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json","w") as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        print(notes)
    else:
        warning.setText("Замітка для додавання тегу не обрана")
        warning.show()
def del_tag():
    if list_notes.selectedItems():
        keys=key=list_notes.selectedItems()[0].text()
        tag=list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data_json","w")as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        warning.setText("Тег для вилучення не обраний")
        warning.show()
def search_tag():
    print(button_tag_search.text())
    tag=field1_tag.text()
    if button_tag_search.text()=="Шукати замітки по тегу" and tag:
        print(tag)
        notes_filtrated={}
        for note in notes[note]["теги"]:
            notes_filtrated[note]=notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Скинути пошук":
        field1_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Шукати замітки по тегу")
        print(button_tag_search.text())
    else:
        pass
buttonstyle=[button_tag_del,button_tag_add,button_note_save,button_note_del,button_note_create,button_tag_search]
for u in buttonstyle:
    u.setStyleSheet("""
                background-image: url(png.jpg);
                background-position: center;
                background-repeat: no-repeat;
                color: white
""")

labelstyle=[list_tags_label,list_notes_label]

for f in labelstyle:
    f.setStyleSheet("""
    background-color: #969696
""")
button_note_create.clicked.connect(add_note)            
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
with open("notes_data.json","r") as file:
    notes=json.load(file)
list_notes.addItems(notes)

notes_win.show()
app.exec_()
import sys
from PyQt5.QtWidgets import (QInputDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
                             QListWidget, QMessageBox, QDateTimeEdit, QDialog, QLabel,
                             QDialogButtonBox, QCheckBox)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, Qt


class ReminderDialog(QDialog):  
    taskAccepted = pyqtSignal(str)  

    def __init__(self, task, parent=None):  
        super().__init__(parent)  
        self.setWindowTitle("Reminder")  
        layout = QVBoxLayout()  
        self.label = QLabel(f"Reminder for task '{task}' reached!")  
        layout.addWidget(self.label)  
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)  
        buttons.accepted.connect(self.accept)  
        layout.addWidget(buttons)  
        self.setLayout(layout)  
        buttons.accepted.connect(lambda: self.taskAccepted.emit(task))  


class ToDoListApp(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
        self.loadTasks()  

    def initUI(self):  
        self.setWindowTitle('To-Do List')  
        self.setGeometry(100, 100, 600, 400)  

        main_layout = QVBoxLayout()  

        input_layout = QHBoxLayout()  
        self.task_input = QLineEdit()  
        self.reminder_input = QDateTimeEdit()  
        self.reminder_checkbox = QCheckBox("Set Reminder")  
        add_button = QPushButton('Add Task')  
        add_button.clicked.connect(self.addTask)  
        input_layout.addWidget(self.task_input)  
        input_layout.addWidget(self.reminder_input)  
        input_layout.addWidget(self.reminder_checkbox)  
        input_layout.addWidget(add_button)  
        main_layout.addLayout(input_layout)  

        self.task_list = QListWidget()  
        main_layout.addWidget(self.task_list)  

        buttons_layout = QHBoxLayout()  
        self.delete_button = QPushButton('Delete Task')  
        self.delete_button.clicked.connect(self.deleteTask)  
        buttons_layout.addWidget(self.delete_button)  

        self.complete_button = QPushButton('Mark as Complete')  
        self.complete_button.clicked.connect(self.markAsComplete)  
        buttons_layout.addWidget(self.complete_button)  

        self.important_button = QPushButton('Mark as Important')  
        self.important_button.clicked.connect(self.markAsImportant)  
        buttons_layout.addWidget(self.important_button)  

        self.edit_button = QPushButton('Edit Task')  
        self.edit_button.clicked.connect(self.editTask)  
        buttons_layout.addWidget(self.edit_button)  

        self.clear_button = QPushButton('Clear All Tasks')  
        self.clear_button.clicked.connect(self.clearTasks)  
        buttons_layout.addWidget(self.clear_button)  

        main_layout.addLayout(buttons_layout)  

        self.setLayout(main_layout)  

        self.timer = QTimer(self)  
        self.timer.timeout.connect(self.checkReminders)  
        self.timer.start(1000)  

        self.reminders = {}  
        self.displayed_reminders = {}  
        self.tasks = {}  


    def addTask(self):  
        task = self.task_input.text()  
        if task:  
            reminder_time = self.reminder_input.dateTime()  
            set_reminder = self.reminder_checkbox.isChecked()  
            self.tasks[task] = {'reminder_time': reminder_time.toPyDateTime(), 'important': False,
                               'complete': False, 'set_reminder': set_reminder}  
            self.task_list.addItem(task)  
            if set_reminder:  
                self.setReminder(task, reminder_time)
            self.saveTasks()  
            self.task_input.clear()  
        else:  
            QMessageBox.warning(self, 'Warning', 'Please enter a task!')

    def deleteTask(self):  
        selected_item = self.task_list.currentItem()  
        if selected_item:  
            task = selected_item.text()  
            if task in self.reminders:  
                del self.reminders[task]
            del self.tasks[task]  
            self.task_list.takeItem(self.task_list.row(selected_item))  
            self.saveTasks()  
        else:  
            QMessageBox.warning(self, 'Warning', 'Please select a task to delete!')

    def markAsComplete(self):  
        selected_item = self.task_list.currentItem()  
        if selected_item:  
            task = selected_item.text()  
            self.tasks[task]['complete'] = True  
            selected_item.setCheckState(Qt.Checked)  
            self.saveTasks()  
        else:  
            QMessageBox.warning(self, 'Warning', 'Please select a task to mark as complete!')

    def markAsImportant(self):  
        selected_item = self.task_list.currentItem()  
        if selected_item:  
            task = selected_item.text()  
            self.tasks[task]['important'] = True  
            self.updateTaskColor(task)  
            self.saveTasks()  
        else:  
            QMessageBox.warning(self, 'Warning', 'Please select a task to mark as important!')

    def editTask(self):  
        selected_item = self.task_list.currentItem()  
        if selected_item:  
            task = selected_item.text()  
            reminder_time = self.tasks[task]['reminder_time']  
            new_task, ok = QInputDialog.getText(self, 'Edit Task', 'Enter new task name:', QLineEdit.Normal, task)  
            if ok:  
                new_reminder_time = self.reminder_input.dateTime()  
                set_reminder = self.reminder_checkbox.isChecked()  
                self.deleteTask()  
                self.task_input.setText(new_task)  
                self.reminder_input.setDateTime(new_reminder_time)  
                self.reminder_checkbox.setChecked(set_reminder)  
                self.addTask()  
        else:  
            QMessageBox.warning(self, 'Warning', 'Please select a task to edit!')

    def clearTasks(self):  
        self.task_list.clear()  
        self.tasks.clear()  
        self.saveTasks()  

    def setReminder(self, task, reminder_time):  
        self.reminders[task] = reminder_time.toPyDateTime()  

    def checkReminders(self):  
        current_time = QDateTime.currentDateTime()  
        for task, reminder_time in list(self.reminders.items()):  
            if current_time >= reminder_time and task not in self.displayed_reminders:  
                reminder_dialog = ReminderDialog(task, self)  
                reminder_dialog.taskAccepted.connect(self.handleTaskAccepted)  
                self.displayed_reminders[task] = reminder_dialog  
                reminder_dialog.exec_()  
                del self.reminders[task]  

    def handleTaskAccepted(self, task):  
        if task in self.displayed_reminders:  
            del self.displayed_reminders[task]  

    def updateTaskColor(self, task):  
        color = QColor('red')  
        items = self.task_list.findItems(task, Qt.MatchExactly)  
        if items:  
            for item in items:  
                item.setBackground(color)  

    def saveTasks(self):  
        with open('tasks.txt', 'w') as f:  
            for task, data in self.tasks.items():  
                f.write(f"{task},{data['reminder_time']},{data['important']},{data['complete']},{data['set_reminder']}\n")  

    def loadTasks(self):  
        try:  
            with open('tasks.txt', 'r') as f:  
                for line in f:  
                    task_data = line.strip().split(',')  
                    if len(task_data) == 5:  
                        task, reminder_time, important, complete, set_reminder = task_data  
                        reminder_time = QDateTime.fromString(reminder_time, Qt.ISODate)  
                        self.tasks[task] = {'reminder_time': reminder_time.toPyDateTime(), 'important': bool(important),  
                                            'complete': bool(complete), 'set_reminder': bool(set_reminder)}  
                        self.task_list.addItem(task)  
                        if self.tasks[task]['important']:  
                            self.updateTaskColor(task)  
                        if self.tasks[task]['complete']:  
                            self.task_list.item(self.task_list.count() - 1).setCheckState(Qt.Checked)  
                        if self.tasks[task]['set_reminder']:  
                            self.setReminder(task, reminder_time)  
                    else:  
                        print(f"Ignoring invalid task data: {line}")
        except FileNotFoundError:  
            pass  

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    todo_app = ToDoListApp()  
    todo_app.show()  
    sys.exit(app.exec_())  

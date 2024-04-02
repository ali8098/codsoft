import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, QLabel, QInputDialog

class Contact:
    def __init__(self, name, phone_number, email, address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            'name': self.name,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['name'], data['phone_number'], data['email'], data['address'])

class PhoneBook(QWidget):
    def __init__(self):
        super().__init__()
        self.contacts = []
        self.original_contacts = []  # Store the original list of contacts
        self.initUI()
        self.load_contacts()

    def initUI(self):
        self.setWindowTitle("Contact Book")
        self.setGeometry(100, 100, 600, 600)

        main_layout = QVBoxLayout()

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel('Name:'))
        self.name_input = QLineEdit()
        input_layout.addWidget(self.name_input)

        input_layout.addWidget(QLabel('Phone Number:'))
        self.phone_input = QLineEdit()
        input_layout.addWidget(self.phone_input)

        input_layout.addWidget(QLabel('Email:'))
        self.email_input = QLineEdit()  
        input_layout.addWidget(self.email_input)  

        input_layout.addWidget(QLabel('Address:'))
        self.address_input = QLineEdit()  
        input_layout.addWidget(self.address_input)  

        main_layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add Contact')
        add_button.clicked.connect(self.add_contact)
        button_layout.addWidget(add_button)

        search_button = QPushButton('Search Contact')
        search_button.clicked.connect(self.search_contact)
        button_layout.addWidget(search_button)

        back_button = QPushButton('Orignal Contact List')
        back_button.clicked.connect(self.show_all_contacts)
        button_layout.addWidget(back_button)

        edit_button = QPushButton('Edit Contact')
        edit_button.clicked.connect(self.edit_selected_contact)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Delete Contact')
        delete_button.clicked.connect(self.delete_selected_contact)
        button_layout.addWidget(delete_button)

        main_layout.addLayout(button_layout)

        self.contact_list = QListWidget()
        main_layout.addWidget(self.contact_list)

        self.setLayout(main_layout)

    def add_contact(self):
        name = self.name_input.text()
        phone_number = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        if name and phone_number:
            contact = Contact(name, phone_number, email, address)
            self.contacts.append(contact)
            self.original_contacts.append(contact)  # Update original contacts
            self.save_contacts()
            self.clear_input_fields()
            self.update_contact_list()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a name and phone number!')

    def search_contact(self):
        search_text, ok = QInputDialog.getText(self, 'Search Contact', 'Enter name or phone number:')
        if ok:
            results = [contact for contact in self.original_contacts if
                       search_text.lower() in contact.name.lower() or search_text in contact.phone_number]
            if results:
                self.display_contact_list(results)
            else:
                QMessageBox.information(self, 'Search Results', 'No matching contacts found.')

    def show_all_contacts(self):
        self.display_contact_list(self.original_contacts)

    def edit_selected_contact(self):
        selected_items = self.contact_list.selectedItems()
        if selected_items:
            index = self.contact_list.row(selected_items[0])
            self.edit_contact(index)
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a contact to edit!')

    def edit_contact(self, index):
        if index >= 0 and index < len(self.contacts):
            contact = self.contacts[index]
            name, ok = QInputDialog.getText(self, 'Edit Contact', f'Edit name for {contact.name}:', QLineEdit.Normal, contact.name)
            if ok:
                phone_number, ok = QInputDialog.getText(self, 'Edit Contact', f'Edit phone number for {contact.name}:', QLineEdit.Normal, contact.phone_number)
                if ok:
                    email, ok = QInputDialog.getText(self, 'Edit Contact', f'Edit email for {contact.name}:', QLineEdit.Normal, contact.email)
                    if ok:
                        address, ok = QInputDialog.getText(self, 'Edit Contact', f'Edit address for {contact.name}:', QLineEdit.Normal, contact.address)
                        if ok:
                            contact.name = name
                            contact.phone_number = phone_number
                            contact.email = email
                            contact.address = address
                            self.save_contacts()
                            self.update_contact_list()
        else:
            QMessageBox.warning(self, 'Warning', 'Invalid contact index!')

    def delete_selected_contact(self):
        selected_items = self.contact_list.selectedItems()
        if selected_items:
            index = self.contact_list.row(selected_items[0])
            del self.contacts[index]
            self.original_contacts = self.contacts[:]  # Update original contacts
            self.save_contacts()
            self.update_contact_list()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a contact to delete!')

    def update_contact_list(self):
        self.display_contact_list(self.contacts)

    def display_contact_list(self, contacts):
        self.contact_list.clear()
        for contact in contacts:
            self.contact_list.addItem(f'{contact.name}: {contact.phone_number}: {contact.email}: {contact.address}')

    def clear_input_fields(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump([contact.to_dict() for contact in self.contacts], f)

    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as f:
                data = json.load(f)
                self.contacts = [Contact.from_dict(contact_data) for contact_data in data]
                self.original_contacts = self.contacts[:]  # Set original contacts
                self.update_contact_list()
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    contact_manager = PhoneBook()
    contact_manager.show()
    sys.exit(app.exec())

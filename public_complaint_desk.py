import sys
import csv
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFormLayout
)
from PyQt5.QtGui import QIcon, QPixmap

class PublicComplaintDesk(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Public Complaint Desk')
        self.setWindowIcon(QIcon('icon.png'))  # Add your icon path here
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Adding a graphic at the top
        self.image_label = QLabel(self)
        self.pixmap = QPixmap('logo.png')  # Add your logo path here
        self.image_label.setPixmap(self.pixmap)
        self.layout.addWidget(self.image_label)

        form_layout = QFormLayout()

        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Enter your name')
        form_layout.addRow('Name:', self.nameInput)

        self.complaintInput = QLineEdit(self)
        self.complaintInput.setPlaceholderText('Enter your complaint here')
        form_layout.addRow('Complaint:', self.complaintInput)

        self.submitButton = QPushButton('Submit Complaint', self)
        self.submitButton.clicked.connect(self.submitComplaint)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.submitButton)

        self.checkStatusInput = QLineEdit(self)
        self.checkStatusInput.setPlaceholderText('Enter your complaint ID to check status')
        self.layout.addWidget(self.checkStatusInput)

        self.checkStatusButton = QPushButton('Check Status', self)
        self.checkStatusButton.clicked.connect(self.checkStatus)
        self.layout.addWidget(self.checkStatusButton)

        self.statusLabel = QLabel('', self)
        self.layout.addWidget(self.statusLabel)

        self.setLayout(self.layout)

    def generate_complaint_id(self):
        """Generate a unique 5-digit complaint ID."""
        existing_ids = set()
        try:
            with open('complaints.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    existing_ids.add(row[0])
        except FileNotFoundError:
            pass

        while True:
            complaint_id = str(random.randint(10000, 99999))
            if complaint_id not in existing_ids:
                return complaint_id

    def submitComplaint(self):
        name = self.nameInput.text()
        complaint = self.complaintInput.text()
        if not name or not complaint:
            QMessageBox.warning(self, 'Input Error', 'Please enter your name and complaint.')
            return

        complaint_id = self.generate_complaint_id()
        with open('complaints.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([complaint_id, name, complaint, 'Pending'])

        QMessageBox.information(self, 'Complaint Submitted', f'Your complaint ID is {complaint_id}')
        self.nameInput.clear()
        self.complaintInput.clear()

    def checkStatus(self):
        complaint_id = self.checkStatusInput.text()
        if not complaint_id:
            QMessageBox.warning(self, 'Input Error', 'Please enter a complaint ID.')
            return

        found = False
        try:
            with open('complaints.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == complaint_id:
                        self.statusLabel.setText(f'Status: {row[3]}')
                        found = True
                        break
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'No complaints found.')

        if not found:
            QMessageBox.warning(self, 'Error', 'Complaint ID not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PublicComplaintDesk()
    ex.show()
    sys.exit(app.exec_())

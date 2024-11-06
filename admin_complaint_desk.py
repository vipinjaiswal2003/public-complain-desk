import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFormLayout
)
from PyQt5.QtGui import QIcon
class AdminComplaintDesk(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Complaint Desk')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.complaintIDInput = QLineEdit(self)
        self.complaintIDInput.setPlaceholderText('Enter complaint ID to update status')
        form_layout.addRow('Complaint ID:', self.complaintIDInput)

        self.statusInput = QLineEdit(self)
        self.statusInput.setPlaceholderText('Enter new status')
        form_layout.addRow('New Status:', self.statusInput)

        self.updateStatusButton = QPushButton('Update Status', self)
        self.updateStatusButton.clicked.connect(self.updateStatus)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.updateStatusButton)

        self.setLayout(self.layout)

    def updateStatus(self):
        complaint_id = self.complaintIDInput.text()
        new_status = self.statusInput.text()
        if not complaint_id or not new_status:
            QMessageBox.warning(self, 'Input Error', 'Please enter both complaint ID and new status.')
            return

        found = False
        rows = []
        with open('complaints.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == complaint_id:
                    row[3] = new_status
                    found = True
                rows.append(row)

        if found:
            with open('complaints.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            QMessageBox.information(self, 'Status Updated', 'Complaint status updated successfully.')
        else:
            QMessageBox.warning(self, 'Error', 'Complaint ID not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AdminComplaintDesk()
    ex.show()
    sys.exit(app.exec_())

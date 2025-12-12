from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


class AddWidgetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Monitor")

        layout = QVBoxLayout(self)

        self.source_label = QLabel("Data source:")
        self.source_combo = QComboBox()
        self.source_combo.addItems(["None", "Test"])

        self.name_label = QLabel("Data type:")
        self.name_combo = QComboBox()
        self.name_combo.setEnabled(False)

        self.display_label = QLabel("Display type:")
        self.display_combo = QComboBox()
        self.display_combo.setEnabled(False)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        layout.addWidget(self.source_label)
        layout.addWidget(self.source_combo)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_combo)
        layout.addWidget(self.display_label)
        layout.addWidget(self.display_combo)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

        self.source_combo.currentIndexChanged.connect(self.toggle_name_combo)

    def toggle_name_combo(self):
        if self.source_combo.currentIndex() == 1:
            self.name_combo.addItems([
                "None",
                "Oil temp",
                "Coolant temp",
                "RPM", "Speed",
                "Fuel pressure",
                "Oil pressure",
                "Engine load %"
            ])
            self.name_combo.setEnabled(True)
            self.name_combo.currentIndexChanged.connect(self.toggle_display_combo)

    def toggle_display_combo(self):
        if self.name_combo.currentIndex() != 0:
            self.display_combo.addItems(["None", "Plain text", "Circular odometer"])
            self.display_combo.setEnabled(True)
            self.display_combo.currentIndexChanged.connect(self.toggle_ok_button)

    def toggle_ok_button(self):
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)

    def get_inputs(self):
        return self.source_combo.currentText(), self.name_combo.currentText(), self.display_combo.currentText()
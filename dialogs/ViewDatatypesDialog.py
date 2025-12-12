from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QLabel, QLineEdit, \
    QComboBox, QDialogButtonBox
from pathlib import Path

from utils.DataTypes import load_datatypes_from_json
from utils.OBDPaths import OBDPaths


class ViewDatatypesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 200)

        with open (OBDPaths.UserDataTypes, "r", encoding="utf-8") as f:
            user_data_types = load_datatypes_from_json(f.read())


        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Datatypes")
        self.tree.setIndentation(20)
        layout.addWidget(self.tree)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.StandardButton.Save).setEnabled(False) # TODO: Make the save button actually save the new data whatever. Also add a "reset to defaults" button
        layout.addWidget(self.buttons)

        for key in user_data_types:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, user_data_types[key].name)

            # Create child items for details
            range_item = QTreeWidgetItem(parent)
            units_item = QTreeWidgetItem(parent)
            display_item = QTreeWidgetItem(parent)

            # Create and add Range widget
            range_widget = self.create_range_widget(user_data_types[key])
            self.tree.setItemWidget(range_item, 0, range_widget)

            # Create and add Units widget
            units_widget = self.create_units_widget(user_data_types[key])
            self.tree.setItemWidget(units_item, 0, units_widget)

            # Create and add Display Type widget
            display_widget = self.create_display_widget(user_data_types[key])
            self.tree.setItemWidget(display_item, 0, display_widget)

    def create_range_widget(self, datatype):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Range:"))

        min_edit = QLineEdit(str(datatype.min_value))
        min_edit.setMaximumWidth(100)
        layout.addWidget(min_edit)

        layout.addWidget(QLabel("-"))

        max_edit = QLineEdit(str(datatype.max_value))
        max_edit.setMaximumWidth(100)
        layout.addWidget(max_edit)

        layout.addStretch()

        return widget

    def create_units_widget(self, datatype):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Units:"))

        combo = QComboBox()
        combo.addItem(datatype.default_unit)
        for unit in datatype.alternate_units:
            if unit != datatype.default_unit:
                combo.addItem(unit)
        combo.setCurrentText(datatype.default_unit)
        combo.setMaximumWidth(150)
        layout.addWidget(combo)

        layout.addStretch()

        return widget

    def create_display_widget(self, datatype):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Display Type:"))

        combo = QComboBox()
        combo.addItem(datatype.default_display_type.pretty())
        for display_type in datatype.alternate_display_types:
            if display_type.pretty() != datatype.default_display_type.pretty():
                combo.addItem(display_type.pretty())
        combo.setCurrentText(datatype.default_display_type.pretty())
        combo.setMaximumWidth(150)
        layout.addWidget(combo)

        layout.addStretch()

        return widget
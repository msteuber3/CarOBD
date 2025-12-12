from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QDialogButtonBox, QTreeWidgetItem, QWidget, QHBoxLayout, \
    QLabel, QRadioButton, QComboBox, QLineEdit

from utils.DataTypes import DataType
from utils.Layout import load_all_layouts, Layout


class ViewLayoutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layouts_dict = load_all_layouts()

        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Datatypes")
        self.tree.setIndentation(20)
        layout.addWidget(self.tree)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)  # TODO: Make the save button actually save the new layout
        layout.addWidget(self.buttons)

        for key in layouts_dict:
            top_level_parent = QTreeWidgetItem(self.tree)
            top_level_parent.setText(0, layouts_dict[key].name)

            is_default_item = QTreeWidgetItem(top_level_parent)
            source_item = QTreeWidgetItem(top_level_parent)

            is_default_widget = self.create_default_widget(layouts_dict[key])
            self.tree.setItemWidget(is_default_item, 0, is_default_widget)

            source_item.setText(0, f"Source: {layouts_dict[key].source}")
            self.tree.setItemWidget(source_item, 0, None)

            for widget in layouts_dict[key].widgets:
                widgets_parent = QTreeWidgetItem(top_level_parent)
                widgets_parent.setText(0, layouts_dict[key].widgets[widget].name)

                range_item = QTreeWidgetItem(widgets_parent)
                units_item = QTreeWidgetItem(widgets_parent)
                display_item = QTreeWidgetItem(widgets_parent)

                range_widget = self.create_range_widget(layouts_dict[key].widgets[widget])
                self.tree.setItemWidget(range_item, 0, range_widget)

                units_widget = self.create_units_widget(layouts_dict[key].widgets[widget])
                self.tree.setItemWidget(units_item, 0, units_widget)

                display_widget = self.create_display_widget(layouts_dict[key].widgets[widget])
                self.tree.setItemWidget(display_item, 0, display_widget)

    def create_default_widget(self, layout_item: Layout):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Default layout:"))

        button = QRadioButton()
        if layout_item.default:
            button.setChecked(True)
        layout.addWidget(button)
        return widget

    def create_range_widget(self, datatype: DataType):
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
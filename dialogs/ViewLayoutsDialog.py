from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QDialogButtonBox, QTreeWidgetItem

from utils.Layout import load_all_layouts


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

            for data in layouts_dict[key].sequence_map:
                if data[0] == 'd':


            # Create child items for details
            range_item = QTreeWidgetItem(parent)
            units_item = QTreeWidgetItem(parent)
            display_item = QTreeWidgetItem(parent)

            # Create and add Range widget
            range_widget = self.create_range_widget(layouts_dict[key])
            self.tree.setItemWidget(range_item, 0, range_widget)

            # Create and add Units widget
            units_widget = self.create_units_widget(layouts_dict[key])
            self.tree.setItemWidget(units_item, 0, units_widget)

            # Create and add Display Type widget
            display_widget = self.create_display_widget(layouts_dict[key])
            self.tree.setItemWidget(display_item, 0, display_widget)
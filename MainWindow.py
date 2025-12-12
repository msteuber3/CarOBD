import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QSlider, QWidget, QSizePolicy, QHBoxLayout, QMenu
from dialogs.AddWidgetDialog import AddWidgetDialog
from custom_widgets.OdometerWidget import OdometerWidget
from custom_widgets.PlainTextDisplay import PlainTextDisplay
from dialogs.ViewDatatypesDialog import ViewDatatypesDialog
from dialogs.ViewLayoutsDialog import ViewLayoutsDialog
from dialogs.ViewScriptsDialog import ViewScriptsDialog

slider_test = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_list = []
        self.setWindowTitle("Aleko's Racecar OBD")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget(self)
        self.layout = QHBoxLayout(self.central_widget)

        self.__set_monitor_widgets_items()
        self.__create_menu_items()

    def __set_monitor_widgets_items(self):
        if slider_test:
            val_test_widget1 = QWidget(self.central_widget)
            self.__add_test_odometer("TEST", val_test_widget1)
            self.widget_list.append(val_test_widget1)

            val_test_widget2 = QWidget(self.central_widget)
            self.__add_test_plain_text("TEST", val_test_widget2)
            self.widget_list.append(val_test_widget2)
        else:
            odometer = OdometerWidget("Speed", parent=self.central_widget)
            odometer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self.widget_list.append(odometer)

        for widget in self.widget_list:
            self.layout.addWidget(widget)

        self.setCentralWidget(self.central_widget)

    def __load_from_json(self, json_file):
        pass #TODO

    ######################################################################
    ####################  Display test setup  ############################
    ######################################################################

    def __add_test_odometer(self, name, val_test_widget):
        odometer = OdometerWidget(name, parent=val_test_widget)
        odometer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.__add_test_slider(odometer, val_test_widget)

    def __add_test_plain_text(self, name, val_test_widget):
        plain_text = PlainTextDisplay(name, parent=val_test_widget)
        plain_text.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.__add_test_slider(plain_text, val_test_widget)

    def __add_test_slider(self, display_meter, parent):
        slider_layout = QVBoxLayout(parent)

        slider = QSlider(Qt.Orientation.Horizontal, parent=parent)
        slider.setRange(0, 260)
        slider.valueChanged.connect(display_meter.set_value)
        slider.setFixedWidth(display_meter.sizeHint().width())

        slider_layout.addWidget(display_meter)
        slider_layout.addWidget(slider)

    ######################################################################

    ######################################################################
    ####################  Menu Options  ##################################
    ######################################################################

    def __create_menu_items(self):
        edit_add_widget = QAction("Add monitor", self)
        edit_add_widget.triggered.connect(self.__add_monitor_widget)

        edit_state_start = QAction("Modify layout", self)
        edit_state_start.triggered.connect(self.__begin_edit_state)

        view_layouts = QAction("Layouts", self)
        view_layouts.triggered.connect(self.__view_layouts)

        save_current_layout = QAction("Save current layout", self)
        save_current_layout.triggered.connect(self.__save_current_layout)

        load_layout_submenu = QMenu("Load layout", self)
        for f in os.listdir("./config/layouts"):
            layout_action = QAction(f.replace(".json", ""), self)
            layout_action.triggered.connect(lambda _, file=f: self.__load_from_json(file))
            load_layout_submenu.addAction(layout_action)

        save_current_layout_as_default = QAction("Save current layout as default", self)
        save_current_layout_as_default.triggered.connect(self.__save_current_layout_as_default)

        view_datatypes = QAction("Data types", self)
        view_datatypes.triggered.connect(self.__view_datatypes)

        view_data_sources = QAction("Data sources", self)
        view_data_sources.triggered.connect(self.__view_data_sources)

        menu = self.menuBar()

        edit_menu = menu.addMenu("&Edit")
        edit_menu.addAction(edit_add_widget)
        edit_menu.addAction(edit_state_start)

        options_menu = menu.addMenu("&Options")
        options_menu.addAction(view_layouts)
        options_menu.addAction(save_current_layout)
        options_menu.addMenu(load_layout_submenu)
        options_menu.addAction(save_current_layout_as_default)
        options_menu.addSeparator()
        options_menu.addAction(view_datatypes)
        options_menu.addSeparator()
        options_menu.addAction(view_data_sources)

        self.setMenuWidget(menu)

    def __add_monitor_widget(self):
        dialog = AddWidgetDialog(self)

        if dialog.exec():
            source, name, display_type = dialog.get_inputs()
            self.__add_new_widget(source, name, display_type)
        else:
            print("Dialog closed")

    def __add_new_widget(self, source, name, display_type):
        if source == "Test":
            if display_type == "Plain text":
                val_test_widget = QWidget(self.central_widget)
                self.__add_test_plain_text(name, val_test_widget)
                self.widget_list.append(val_test_widget)
                self.layout.addWidget(self.widget_list[-1])
                self.update()
            elif display_type == "Circular odometer":
                val_test_widget = QWidget(self.central_widget)
                self.__add_test_odometer(name, val_test_widget)
                self.widget_list.append(val_test_widget)
                self.layout.addWidget(self.widget_list[-1])
                self.update()

    def __begin_edit_state(self): #TODO
        print("Edit state started")

    def __view_layouts(self):
        dialog = ViewLayoutsDialog(parent=self)
        dialog.exec()

    def __save_current_layout(self): #TODO
        print("Save current layout")

    def __save_current_layout_as_default(self): #TODO
        print("Save current layout as default")

    def __view_datatypes(self):
        dialog = ViewDatatypesDialog(self)
        dialog.exec()

    def __view_data_sources(self):
        dialog = ViewScriptsDialog(self)
        dialog.exec()

    ######################################################################



######################################################################
################  start app & create/show window  ####################
######################################################################

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
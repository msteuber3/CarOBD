import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QSlider, QWidget, QSizePolicy, QHBoxLayout, QMenu
from PyQt6.uic.properties import needsWidget

from custom_widgets.DisplayMeter import DisplayMeter
from dialogs.AddWidgetDialog import AddWidgetDialog
from custom_widgets.OdometerWidget import OdometerWidget
from custom_widgets.PlainTextDisplay import PlainTextDisplay
from dialogs.ViewDatatypesDialog import ViewDatatypesDialog
from dialogs.ViewLayoutsDialog import ViewLayoutsDialog
from dialogs.ViewScriptsDialog import ViewScriptsDialog
from utils.DataTypes import DisplayMeterSerial, DataType
from utils.Layout import load_default_layout, load_layout
from utils.OBDPaths import OBDPaths

slider_test = True

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Things that need to happen here:
         - Set the window info. Geometry, title, central widget, layout, and menu items.
         - Then, two options:
            a.) No config file found - a bigass plus sign that takes you to a monitor creation window
            b.) Config file found - create the widgets in the layout. They belong to the main window.
                Keep the config file path here too so we can edit it, but we don't really need it past setup.
        """
        super().__init__()
        # Set basic window info
        self.setWindowTitle("Aleko's Racecar OBD")
        self.setGeometry(100, 100, 1000, 600)

        # Create the central widget that'll hold all of the non-permanent UI elements
        self.central_widget = QWidget(self)
        self.layout = QHBoxLayout(self.central_widget)

        #self.__set_monitor_widgets_items()
        # Set the menu
        self.__create_menu_items()
        # And look for a configuration file
        self.config = load_default_layout()
        self.widget_list = []
        # This is so that later on I can tell when the config has changed
        self.configuration_name = None

        # Finally. Doit
        self.setup_ui_elements()

    def setup_ui_elements(self):
        """ Check the configuration member and the list of widgets. """
        """ If the config member is not empty, clear the list, add the widgets to it, and store the name such that I can check if it changed
            If it is and the list is empty (it should be on startup), default to an empty_layout  """
        if self.config:
            try:
                self.widget_list.clear()
                self.configuration_name = self.config.name # Store the config name to help detect changes to it later
                for key, widget in self.config.widgets.items():
                    temp_widget = self.generate_widget(widget)
                    if temp_widget is not None:
                        self.widget_list.append(temp_widget)
                        self.layout.addWidget(self.widget_list[-1]) #messy. I dont like.
                self.central_widget.setLayout(self.layout)
                self.update()
            except Exception as e:
                print(e)


    def generate_widget(self, widget) -> DisplayMeter | None:
        match widget.default_display_type.value:
            case DisplayMeterSerial.CIRCULAR_GAUGE.value:
                new_widget = OdometerWidget(widget, self.central_widget)
                new_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                return new_widget
            case DisplayMeterSerial.PLAIN_TEXT.value:
                new_widget = PlainTextDisplay(widget, self.central_widget)
                new_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                return new_widget
            case DisplayMeterSerial.HORIZONTAL_TACHOMETER:
                return None #TODO
            case _:
                return None

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

        for f in os.listdir(OBDPaths.Layouts):
            layout_action = QAction(f.replace(".json", ""), self)
            layout_action.triggered.connect(lambda _, file=f: self.__load_from_json(OBDPaths.Layouts / file))
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

    def __load_from_json(self, json_file):  # Perhaps split this into load default layout and set layout
        """intended to hook up to the load_layout menu item"""
        with open(json_file, encoding='utf-8') as json_file:
            selected_layout = load_layout(json_file.read())

        if selected_layout is not None:
            if len(selected_layout.widgets) > 0:
                self.current_ui_layout = selected_layout
                self.setup_ui_elements()

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
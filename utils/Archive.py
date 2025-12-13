"""
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
        """






    ######################################################################
    ####################  Display test setup  ############################
    ######################################################################
"""
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
"""
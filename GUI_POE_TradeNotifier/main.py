import sys
import os
from pathlib import Path
from functools import cache, lru_cache

import telegram_send
from PyQt5 import (QtCore,
                   QtGui,
                   QtWidgets,
                   )

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog,
                             QMessageBox, )

from ui import Ui_MainWindow
from poe_notifier import PoeNotifier


class Notifier(QThread):
    thread_active = False

    def __init__(self, mode, path_to_watch):
        QThread.__init__(self)
        self.poe_notifier = PoeNotifier(mode)
        self.poe_notifier.path_to_watch = path_to_watch

    def run(self):
        self.thread_active = True
        while self.thread_active:
            self.poe_notifier.start()

    def stop(self):
        self.poe_notifier.stop()
        self.thread_active = False
        self.wait()


class ConfigureBot(QThread):
    thread_active = False

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.thread_active = True
        while self.thread_active:
            os.system("start /wait cmd /c telegram-send -c")
            self.thread_active = False


class MainApp(QtWidgets.QMainWindow):
    path_to_client = ''
    bot_pass = ''
    mode = ''

    def __init__(self):
        super(MainApp, self).__init__()

        # First thread (Notifier)
        self.notifier = Notifier(self.path_to_client, self.mode)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PathOfExile Trade Notifier v0.1")
        self.setWindowIcon(QIcon('icon_without_bg.png'))
        self.ui.input_path.setPlaceholderText('*\\Steam\\steamapps\\common\\Path of Exile\\logs\\Client.txt')
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_start.clicked.connect(self.start_notifier)
        self.ui.btn_stop.clicked.connect(self.stop_notifier)
        self.ui.btn_browse_path.clicked.connect(self.open_file_browser)
        self.ui.btn_connect.clicked.connect(self.configure_bot)
        self.ui.btn_test_message.clicked.connect(self.test_message)

    def configure_bot(self):
        self.configure_bot_thread = ConfigureBot()
        self.configure_bot_thread.start()
        self.ui.output_log.append('Started configuration...')

    def test_message(self):
        telegram_send.send(messages=['ITS ALIVE!!!'])
        self.ui.output_log.append('Test message send...')

    @staticmethod
    def info_box_path():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QMessageBox{min-width: 150px;}")
        msg.setWindowTitle("Wrong path")
        msg.setText("You NEED enter the right path to 'Client.txt'!")
        msg.setInformativeText("*\\Steam\\steamapps\\common\\Path of Exile\\logs\\Client.txt")
        msg.exec_()

    @staticmethod
    def info_box_conf_done():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QMessageBox{min-width: 150px;}")
        msg.setWindowTitle("Bot connected!")
        msg.setText("You can try to send test message for your bot...")
        # msg.setInformativeText("*\\Steam\\steamapps\\common\\Path of Exile\\logs\\Client.txt")
        msg.exec_()

    def open_file_browser(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        self.path_to_client = dlg.getOpenFileName(self, 'Open File', '', 'TXT file (*.txt)')[0]
        self.ui.input_path.setText(self.path_to_client)

    def start_notifier_module(self):
        self.notifier = Notifier(self.mode, self.path_to_client)
        self.notifier.start()
        self.ui.btn_stop.setEnabled(True)
        self.ui.btn_start.setEnabled(False)
        self.ui.output_log.append('Notifier was started...')

    def check_path_and_start_module(self):
        client_file = Path(self.ui.input_path.text())
        if client_file.is_file() and client_file.name == 'Client.txt':
            self.path_to_client = self.ui.input_path.text()
            self.start_notifier_module()
        else:
            self.info_box_path()

    def start_notifier(self):
        if self.ui.rBtn_pm.isChecked():  # Checking radio buttons to set mode for PoeNotifier class
            self.mode = self.ui.rBtn_pm.text().lower()
        elif self.ui.rBtn_trade.isChecked():  # Checking radio buttons to set mode for PoeNotifier class
            self.mode = self.ui.rBtn_trade.text().lower()

        self.check_path_and_start_module()

    def stop_notifier(self):
        if self.notifier.thread_active:
            self.ui.btn_stop.setEnabled(False)
            self.ui.btn_start.setEnabled(True)
            self.notifier.stop()
            self.ui.output_log.append('Notifier was stopped...')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MainApp()
    application.show()

    sys.exit(app.exec())

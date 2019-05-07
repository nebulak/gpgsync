# -*- coding: utf-8 -*-
"""
GPG Sync
Helps users have up-to-date public keys for everyone in their organization
https://github.com/firstlookmedia/gpgsync
Copyright (C) 2016 First Look Media

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from PyQt5 import QtCore, QtWidgets, QtGui


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, common):
        super(SettingsDialog, self).__init__()
        self.c = common

        self.setWindowTitle(_('GPG Sync Settings'))
        self.setMinimumSize(425, 200)
        self.setMaximumSize(425, 400)
        self.settings = self.c.settings

        self.settings_layout = SettingsLayout(self.settings)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.settings_layout)
        self.setLayout(layout)

class SettingsLayout(QtWidgets.QVBoxLayout):
    def __init__(self, settings):
        super(SettingsLayout, self).__init__()
        self.settings = settings
        self.c = self.settings.c

        self.run_automatically_checkbox = QtWidgets.QCheckBox(_("Run GPG Sync automatically on login"))
        if self.settings.run_automatically:
            self.run_automatically_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.run_automatically_checkbox.setCheckState(QtCore.Qt.Unchecked)

        autostart_vlayout = QtWidgets.QVBoxLayout()
        autostart_vlayout.addWidget(self.run_automatically_checkbox)
        autostart_group = QtWidgets.QGroupBox(_("Start automatically"))
        autostart_group.setLayout(autostart_vlayout)


        self.run_autoupdate_checkbox = QtWidgets.QCheckBox(_("Check for updates automatically"))
        if self.settings.run_autoupdate:
            self.run_autoupdate_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.run_autoupdate_checkbox.setCheckState(QtCore.Qt.Unchecked)
        # self.run_autoupdate_checkbox.stateChanged.connect(self.run_autoupdate_changed)

        # Update interval
        update_interval_hlayout = QtWidgets.QHBoxLayout()
        update_interval_label = QtWidgets.QLabel(_('Time between keylist syncs (in hours)'))
        self.update_interval_edit = QtWidgets.QLineEdit()
        self.update_interval_edit.setText(self.settings.update_interval_hours.decode())
        update_interval_hlayout.addWidget(update_interval_label)
        update_interval_hlayout.addWidget(self.update_interval_edit)

        update_interval_group = QtWidgets.QGroupBox(_("Sync frequency"))
        update_interval_group.setLayout(update_interval_hlayout)

        # SOCKS5 proxy settings
        self.use_proxy = QtWidgets.QCheckBox()
        self.use_proxy.setText(_("Check for updates through SOCKS5 proxy (e.g. Tor)"))
        if self.settings.automatic_update_use_proxy:
            self.use_proxy.setCheckState(QtCore.Qt.Checked)
        else:
            self.use_proxy.setCheckState(QtCore.Qt.Unchecked)

        proxy_host_label = QtWidgets.QLabel(_('Host'))
        self.proxy_host_edit = QtWidgets.QLineEdit()
        self.proxy_host_edit.setText(self.settings.automatic_update_proxy_host.decode())
        proxy_port_label = QtWidgets.QLabel(_('Port'))
        self.proxy_port_edit = QtWidgets.QLineEdit()
        self.proxy_port_edit.setText(self.settings.automatic_update_proxy_port.decode())

        proxy_hlayout = QtWidgets.QHBoxLayout()
        proxy_hlayout.addWidget(proxy_host_label)
        proxy_hlayout.addWidget(self.proxy_host_edit)
        proxy_hlayout.addWidget(proxy_port_label)
        proxy_hlayout.addWidget(self.proxy_port_edit)

        proxy_vlayout = QtWidgets.QVBoxLayout()
        proxy_vlayout.addWidget(self.run_autoupdate_checkbox)
        proxy_vlayout.addWidget(self.use_proxy)
        proxy_vlayout.addLayout(proxy_hlayout)

        autoupdate_group = QtWidgets.QGroupBox(_("Automatic Updates"))
        autoupdate_group.setLayout(proxy_vlayout)

        save_button = QtWidgets.QPushButton(_("Save Settings"))
        save_button.clicked.connect(self.save_settings)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addStretch()

        self.addWidget(autostart_group)
        self.addWidget(update_interval_group)
        if self.c.os != 'Linux':
            self.addWidget(autoupdate_group)
        self.addLayout(button_layout)

    def is_number(self, input):
        try:
            float(input)
            return True
        except ValueError:
            return False

    def save_settings(self):
        self.settings.run_automatically = (self.run_automatically_checkbox.checkState() == QtCore.Qt.Checked)
        if self.c.os != 'Linux':
            self.settings.run_autoupdate = (self.run_autoupdate_checkbox.checkState() == QtCore.Qt.Checked)
            self.settings.automatic_update_use_proxy = (self.use_proxy.checkState() == QtCore.Qt.Checked)
            self.settings.automatic_update_proxy_host = self.proxy_host_edit.text().strip().encode()
            self.settings.automatic_update_proxy_port = self.proxy_port_edit.text().strip().encode()

        # test that the input is actually a number, eventually visually show an error if not
        if self.is_number(self.update_interval_edit.text().strip()):
            self.settings.update_interval_hours = self.update_interval_edit.text().strip().encode()

        # if save is successful, close the dialog
        if self.settings.save():
            self.parent().parent().close()

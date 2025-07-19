import sys
import time
import psutil
import subprocess
import platform
import socket
import threading
import queue
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTabWidget, QPushButton, QLabel, QComboBox, QTableWidget,
                            QTableWidgetItem, QSystemTrayIcon, QMenu, QDialog, QFormLayout,
                            QLineEdit, QCheckBox, QTextEdit, QProgressBar, QSplitter,
                            QGroupBox, QStatusBar, QFileDialog, QMessageBox)
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QTimer, QCoreApplication, QTranslator, QLocale
import pyqtgraph as pg
import numpy as np
import pandas as pd
from scapy.all import sniff, get_if_list
import ping3
from collections import defaultdict

# Try importing netifaces, handle if not available
try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False

# Translation dictionaries
translations = {
    'en': {
        'title': 'Wi-Fi Network Monitor',
        'interface': 'Network Interface',
        'start_monitor': 'Start Monitoring',
        'stop_monitor': 'Stop Monitoring',
        'settings': 'Settings',
        'export': 'Export Data',
        'clear': 'Clear Data',
        'language': 'Language',
        'theme': 'Theme',
        'light_theme': 'Light',
        'dark_theme': 'Dark',
        'save_settings': 'Save Settings',
        'signal_strength': 'Signal Strength (dBm)',
        'bandwidth': 'Bandwidth Usage (Mbps)',
        'packet_rate': 'Packet Rate (packets/s)',
        'latency': 'Latency (ms)',
        'connected_devices': 'Connected Devices',
        'network_info': 'Network Information',
        'ssid': 'SSID',
        'bssid': 'BSSID',
        'channel': 'Channel',
        'security': 'Security',
        'ip_address': 'IP Address',
        'gateway': 'Gateway',
        'dns': 'DNS',
        'logs': 'Logs',
        'statistics': 'Statistics',
        'export_csv': 'Export to CSV',
        'export_json': 'Export to JSON',
        'refresh_rate': 'Refresh Rate (ms)',
        'notification_threshold': 'Notification Threshold (%)',
        'enable_notifications': 'Enable Notifications',
        'status': 'Status',
        'running': 'Running',
        'stopped': 'Stopped',
        'error': 'Error',
        'no_data': 'No data available',
        'select_interface': 'Select a network interface',
        'no_interfaces': 'No network interfaces found',
        'dependency_error': 'Dependency missing: {dep}. Some features may be limited.'
    },
    'fa': {
        'title': 'نظارت بر شبکه وای‌فای',
        'interface': 'رابط شبکه',
        'start_monitor': 'شروع نظارت',
        'stop_monitor': 'توقف نظارت',
        'settings': 'تنظیمات',
        'export': 'خروجی گرفتن',
        'clear': 'پاک کردن داده‌ها',
        'language': 'زبان',
        'theme': 'تم',
        'light_theme': 'روشن',
        'dark_theme': 'تیره',
        'save_settings': 'ذخیره تنظیمات',
        'signal_strength': 'قدرت سیگنال (dBm)',
        'bandwidth': 'استفاده از پهنای باند (Mbps)',
        'packet_rate': 'نرخ بسته‌ها (بسته/ثانیه)',
        'latency': 'تاخیر (میلی‌ثانیه)',
        'connected_devices': 'دستگاه‌های متصل',
        'network_info': 'اطلاعات شبکه',
        'ssid': 'SSID',
        'bssid': 'BSSID',
        'channel': 'کانال',
        'security': 'امنیت',
        'ip_address': 'آدرس IP',
        'gateway': 'دروازه',
        'dns': 'DNS',
        'logs': 'لاگ‌ها',
        'statistics': 'آمار',
        'export_csv': 'خروجی به CSV',
        'export_json': 'خروجی به JSON',
        'refresh_rate': 'نرخ به‌روزرسانی (میلی‌ثانیه)',
        'notification_threshold': 'آستانه اعلان (%)',
        'enable_notifications': 'فعال کردن اعلان‌ها',
        'status': 'وضعیت',
        'running': 'در حال اجرا',
        'stopped': 'متوقف',
        'error': 'خطا',
        'no_data': 'داده‌ای موجود نیست',
        'select_interface': 'یک رابط شبکه انتخاب کنید',
        'no_interfaces': 'رابط شبکه‌ای یافت نشد',
        'dependency_error': 'وابستگی غایب: {dep}. برخی ویژگی‌ها ممکن است محدود شوند.'
    },
    'zh': {
        'title': 'Wi-Fi 网络监控',
        'interface': '网络接口',
        'start_monitor': '开始监控',
        'stop_monitor': '停止监控',
        'settings': '设置',
        'export': '导出数据',
        'clear': '清除数据',
        'language': '语言',
        'theme': '主题',
        'light_theme': '明亮',
        'dark_theme': '暗黑',
        'save_settings': '保存设置',
        'signal_strength': '信号强度 (dBm)',
        'bandwidth': '带宽使用量 (Mbps)',
        'packet_rate': '数据包速率 (包/秒)',
        'latency': '延迟 (毫秒)',
        'connected_devices': '连接的设备',
        'network_info': '网络信息',
        'ssid': 'SSID',
        'bssid': 'BSSID',
        'channel': '频道',
        'security': '安全',
        'ip_address': 'IP 地址',
        'gateway': '网关',
        'dns': 'DNS',
        'logs': '日志',
        'statistics': '统计',
        'export_csv': '导出为 CSV',
        'export_json': '导出为 JSON',
        'refresh_rate': '刷新率 (毫秒)',
        'notification_threshold': '通知阈值 (%)',
        'enable_notifications': '启用通知',
        'status': '状态',
        'running': '运行中',
        'stopped': '已停止',
        'error': '错误',
        'no_data': '无可用数据',
        'select_interface': '选择一个网络接口',
        'no_interfaces': '未找到网络接口',
        'dependency_error': '缺少依赖项: {dep}。某些功能可能受限。'
    }
}

class WiFiMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpg'))  
        self.trans = QTranslator()
        self.current_language = 'en'
        self.current_theme = 'light'
        self.monitoring = False
        self.interface = None
        self.data_queue = queue.Queue()
        self.network_data = defaultdict(list)
        self.devices = {}
        self.last_packet_count = 0
        self.last_bytes = 0
        self.start_time = time.time()
        self.setup_ui()
        self.setup_system_tray()  # فعال کردن system tray
        self.load_settings()
        self.update_translations()
        self.apply_theme()
        
        if not NETIFACES_AVAILABLE:
            self.log_error(translations[self.current_language]['dependency_error'].format(dep='netifaces'))

    def setup_ui(self):
        self.setWindowTitle(translations[self.current_language]['title'])
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        dashboard_widget = QWidget()
        dashboard_layout = QHBoxLayout(dashboard_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        dashboard_layout.addWidget(splitter)
        
        left_panel = QGroupBox(translations[self.current_language]['network_info'])
        left_layout = QVBoxLayout(left_panel)
        
        self.signal_plot = pg.PlotWidget(title=translations[self.current_language]['signal_strength'])
        self.signal_data = []
        self.signal_curve = self.signal_plot.plot(pen='b')
        left_layout.addWidget(self.signal_plot)
        
        self.bandwidth_plot = pg.PlotWidget(title=translations[self.current_language]['bandwidth'])
        self.bandwidth_data = []
        self.bandwidth_curve = self.bandwidth_plot.plot(pen='g')
        left_layout.addWidget(self.bandwidth_plot)
        
        self.packet_plot = pg.PlotWidget(title=translations[self.current_language]['packet_rate'])
        self.packet_data = []
        self.packet_curve = self.packet_plot.plot(pen='r')
        left_layout.addWidget(self.packet_plot)
        
        self.latency_plot = pg.PlotWidget(title=translations[self.current_language]['latency'])
        self.latency_data = []
        self.latency_curve = self.latency_plot.plot(pen='y')
        left_layout.addWidget(self.latency_plot)
        
        splitter.addWidget(left_panel)
        
        right_panel = QGroupBox(translations[self.current_language]['network_info'])
        right_layout = QVBoxLayout(right_panel)
        
        self.network_info = QTextEdit()
        self.network_info.setReadOnly(True)
        right_layout.addWidget(self.network_info)
        
        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(4)
        self.devices_table.setHorizontalHeaderLabels(['MAC', 'IP', 'Last Seen', 'Vendor'])
        right_layout.addWidget(self.devices_table)
        
        splitter.addWidget(right_panel)
        self.tabs.addTab(dashboard_widget, translations[self.current_language]['network_info'])
        
        logs_widget = QWidget()
        logs_layout = QVBoxLayout(logs_widget)
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        logs_layout.addWidget(self.logs_text)
        self.tabs.addTab(logs_widget, translations[self.current_language]['logs'])
        
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        stats_layout.addWidget(self.stats_text)
        self.tabs.addTab(stats_widget, translations[self.current_language]['statistics'])
        
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        self.interface_combo = QComboBox()
        self.populate_interfaces()
        control_layout.addWidget(QLabel(translations[self.current_language]['interface']))
        control_layout.addWidget(self.interface_combo)
        
        self.start_button = QPushButton(translations[self.current_language]['start_monitor'])
        self.start_button.clicked.connect(self.start_monitoring)
        control_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton(translations[self.current_language]['stop_monitor'])
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)
        
        self.settings_button = QPushButton(translations[self.current_language]['settings'])
        self.settings_button.clicked.connect(self.show_settings)
        control_layout.addWidget(self.settings_button)
        
        self.export_button = QPushButton(translations[self.current_language]['export'])
        self.export_button.clicked.connect(self.export_data)
        control_layout.addWidget(self.export_button)
        
        self.clear_button = QPushButton(translations[self.current_language]['clear'])
        self.clear_button.clicked.connect(self.clear_data)
        control_layout.addWidget(self.clear_button)
        
        main_layout.addWidget(control_panel)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel(translations[self.current_language]['status'] + ': ' + 
                                translations[self.current_language]['stopped'])
        self.status_bar.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def setup_system_tray(self):
        # Commented out due to missing icon
        # self.tray_icon = QSystemTrayIcon(QIcon('icon.png'), self)
        # tray_menu = QMenu()
        # show_action = tray_menu.addAction(translations[self.current_language]['title'])
        # show_action.triggered.connect(self.show)
        # quit_action = tray_menu.addAction("Quit")
        # quit_action.triggered.connect(QCoreApplication.quit)
        # self.tray_icon.setContextMenu(tray_menu)
        # self.tray_icon.show()
        # pass
        self.tray_icon = QSystemTrayIcon(QIcon('logo.jpg'), self)  # تنظیم favicon
        tray_menu = QMenu()
        show_action = tray_menu.addAction(translations[self.current_language]['title'])
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QCoreApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def populate_interfaces(self):
        interfaces = get_if_list()
        self.interface_combo.addItem(translations[self.current_language]['select_interface'])
        for iface in interfaces:
            self.interface_combo.addItem(iface)
        if not interfaces:
            self.interface_combo.addItem(translations[self.current_language]['no_interfaces'])

    def start_monitoring(self):
        if self.interface_combo.currentIndex() == 0:
            QMessageBox.warning(self, translations[self.current_language]['error'], 
                              translations[self.current_language]['select_interface'])
            return
        
        self.interface = self.interface_combo.currentText()
        self.monitoring = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText(translations[self.current_language]['status'] + ': ' + 
                                translations[self.current_language]['running'])
        
        self.monitor_thread = threading.Thread(target=self.monitor_network)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText(translations[self.current_language]['status'] + ': ' + 
                                translations[self.current_language]['stopped'])

    def monitor_network(self):
        while self.monitoring:
            try:
                signal = self.get_signal_strength()
                bandwidth = self.get_bandwidth()
                packet_rate = self.get_packet_rate()
                latency = self.get_latency()
                
                data = {
                    'timestamp': time.time(),
                    'signal': signal,
                    'bandwidth': bandwidth,
                    'packet_rate': packet_rate,
                    'latency': latency,
                    'devices': self.get_connected_devices()
                }
                
                self.data_queue.put(data)
                
                if self.settings.get('notifications', False):
                    if bandwidth > self.settings.get('threshold', 80):
                        self.log_error(f"High bandwidth usage: {bandwidth:.2f} Mbps")
                
                time.sleep(self.settings.get('refresh_rate', 1) / 1000)
                
            except Exception as e:
                self.log_error(str(e))
                time.sleep(1)

    def get_signal_strength(self):
        if platform.system() == 'Windows':
            try:
                output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8', errors='ignore')
                for line in output.split('\n'):
                    if 'Signal' in line:
                        return int(line.split(':')[1].strip().replace('%', '')) * -1
                    if 'SSID' in line and not 'BSSID' in line:
                        self.network_data['ssid'].append(line.split(':')[1].strip())
                    if 'Channel' in line:
                        self.network_data['channel'].append(line.split(':')[1].strip())
                    if 'Authentication' in line:
                        self.network_data['security'].append(line.split(':')[1].strip())
                return -100
            except:
                return -100
        return -100

    def get_bandwidth(self):
        net_io = psutil.net_io_counters(pernic=True).get(self.interface, None)
        if not net_io:
            return 0
        current_bytes = net_io.bytes_sent + net_io.bytes_recv
        bandwidth = (current_bytes - self.last_bytes) * 8 / 1000000
        self.last_bytes = current_bytes
        return bandwidth

    def get_packet_rate(self):
        net_io = psutil.net_io_counters(pernic=True).get(self.interface, None)
        if not net_io:
            return 0
        current_packets = net_io.packets_sent + net_io.packets_recv
        packet_rate = current_packets - self.last_packet_count
        self.last_packet_count = current_packets
        return packet_rate

    def get_latency(self):
        try:
            latency = ping3.ping('8.8.8.8', timeout=1)
            return latency * 1000 if latency else 0
        except:
            return 0

    def get_connected_devices(self):
        devices = {}
        try:
            if platform.system() == 'Windows':
                output = subprocess.check_output(['arp', '-a']).decode('utf-8', errors='ignore')
                for line in output.split('\n'):
                    if '.' in line and '-' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            ip = parts[0]
                            mac = parts[1]
                            devices[mac] = {'ip': ip, 'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'vendor': 'Unknown'}
        except:
            pass
        return devices

    def update_ui(self):
        try:
            while not self.data_queue.empty():
                data = self.data_queue.get()
                
                self.signal_data.append(data['signal'])
                self.bandwidth_data.append(data['bandwidth'])
                self.packet_data.append(data['packet_rate'])
                self.latency_data.append(data['latency'])
                
                if len(self.signal_data) > 100:
                    self.signal_data.pop(0)
                    self.bandwidth_data.pop(0)
                    self.packet_data.pop(0)
                    self.latency_data.pop(0)
                
                self.signal_curve.setData(self.signal_data)
                self.bandwidth_curve.setData(self.bandwidth_data)
                self.packet_curve.setData(self.packet_data)
                self.latency_curve.setData(self.latency_data)
                
                info = self.get_network_info()
                self.network_info.setText(info)
                
                self.devices = data['devices']
                self.update_devices_table()
                
                self.progress_bar.setValue(min(int(data['bandwidth'] / 100 * 100), 100))
                
                self.update_statistics()
                
                self.network_data['signal'].append(data['signal'])
                self.network_data['bandwidth'].append(data['bandwidth'])
                self.network_data['packet_rate'].append(data['packet_rate'])
                self.network_data['latency'].append(data['latency'])
                self.network_data['timestamp'].append(data['timestamp'])
                
        except Exception as e:
            self.log_error(str(e))

    def update_devices_table(self):
        self.devices_table.setRowCount(len(self.devices))
        for i, (mac, info) in enumerate(self.devices.items()):
            self.devices_table.setItem(i, 0, QTableWidgetItem(mac))
            self.devices_table.setItem(i, 1, QTableWidgetItem(info.get('ip', '')))
            self.devices_table.setItem(i, 2, QTableWidgetItem(info.get('last_seen', '')))
            self.devices_table.setItem(i, 3, QTableWidgetItem(info.get('vendor', '')))
        self.devices_table.resizeColumnsToContents()

    def get_network_info(self):
        try:
            info = []
            if NETIFACES_AVAILABLE:
                interfaces = netifaces.interfaces()
                for iface in interfaces:
                    if iface == self.interface:
                        addrs = netifaces.ifaddresses(iface)
                        info.append(f"{translations[self.current_language]['interface']}: {iface}")
                        if netifaces.AF_INET in addrs:
                            for addr in addrs[netifaces.AF_INET]:
                                info.append(f"{translations[self.current_language]['ip_address']}: {addr['addr']}")
                                if 'broadcast' in addr:
                                    info.append(f"Broadcast: {addr['broadcast']}")
                        if netifaces.AF_LINK in addrs:
                            info.append(f"{translations[self.current_language]['bssid']}: {addrs[netifaces.AF_LINK][0]['addr']}")
                        gateways = netifaces.gateways()
                        if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                            info.append(f"{translations[self.current_language]['gateway']}: {gateways['default'][netifaces.AF_INET][0]}")
            else:
                info.append(f"{translations[self.current_language]['interface']}: {self.interface}")
                try:
                    output = subprocess.check_output(['ipconfig']).decode('utf-8', errors='ignore')
                    for line in output.split('\n'):
                        if 'IPv4 Address' in line:
                            info.append(f"{translations[self.current_language]['ip_address']}: {line.split(':')[1].strip()}")
                        if 'Default Gateway' in line:
                            info.append(f"{translations[self.current_language]['gateway']}: {line.split(':')[1].strip()}")
                        if 'DNS Servers' in line:
                            info.append(f"{translations[self.current_language]['dns']}: {line.split(':')[1].strip()}")
                except:
                    pass
                if len(self.network_data.get('ssid', [])) > 0:
                    info.append(f"{translations[self.current_language]['ssid']}: {self.network_data['ssid'][-1]}")
                if len(self.network_data.get('channel', [])) > 0:
                    info.append(f"{translations[self.current_language]['channel']}: {self.network_data['channel'][-1]}")
                if len(self.network_data.get('security', [])) > 0:
                    info.append(f"{translations[self.current_language]['security']}: {self.network_data['security'][-1]}")
            return '\n'.join(info)
        except:
            return translations[self.current_language]['no_data']

    def update_statistics(self):
        stats = []
        if self.network_data['bandwidth']:
            stats.append(f"{translations[self.current_language]['bandwidth']}:")
            stats.append(f"  Average: {np.mean(self.network_data['bandwidth']):.2f} Mbps")
            stats.append(f"  Max: {np.max(self.network_data['bandwidth']):.2f} Mbps")
            stats.append(f"  Min: {np.min(self.network_data['bandwidth']):.2f} Mbps")
        if self.network_data['signal']:
            stats.append(f"{translations[self.current_language]['signal_strength']}:")
            stats.append(f"  Average: {np.mean(self.network_data['signal']):.2f} dBm")
        if self.network_data['packet_rate']:
            stats.append(f"{translations[self.current_language]['packet_rate']}:")
            stats.append(f"  Average: {np.mean(self.network_data['packet_rate']):.2f} packets/s")
        if self.network_data['latency']:
            stats.append(f"{translations[self.current_language]['latency']}:")
            stats.append(f"  Average: {np.mean(self.network_data['latency']):.2f} ms")
        stats.append(f"{translations[self.current_language]['connected_devices']}: {len(self.devices)}")
        self.stats_text.setText('\n'.join(stats))

    def log_error(self, error):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logs_text.append(f"[{timestamp}] {error}")

    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(translations[self.current_language]['settings'])
        layout = QFormLayout(dialog)
        
        language_combo = QComboBox()
        language_combo.addItems(['English', 'فارسی', '中文'])
        language_combo.setCurrentText({'en': 'English', 'fa': 'فارسی', 'zh': '中文'}[self.current_language])
        layout.addRow(translations[self.current_language]['language'], language_combo)
        
        theme_combo = QComboBox()
        theme_combo.addItems([translations[self.current_language]['light_theme'], 
                            translations[self.current_language]['dark_theme']])
        theme_combo.setCurrentText(translations[self.current_language][f"{self.current_theme}_theme"])
        layout.addRow(translations[self.current_language]['theme'], theme_combo)
        
        refresh_rate = QLineEdit(str(self.settings.get('refresh_rate', 1000)))
        layout.addRow(translations[self.current_language]['refresh_rate'], refresh_rate)
        
        threshold = QLineEdit(str(self.settings.get('threshold', 80)))
        layout.addRow(translations[self.current_language]['notification_threshold'], threshold)
        
        notifications = QCheckBox()
        notifications.setChecked(self.settings.get('notifications', False))
        layout.addRow(translations[self.current_language]['enable_notifications'], notifications)
        
        save_button = QPushButton(translations[self.current_language]['save_settings'])
        save_button.clicked.connect(lambda: self.save_settings(
            language_combo.currentText(),
            theme_combo.currentText(),
            refresh_rate.text(),
            threshold.text(),
            notifications.isChecked()
        ))
        layout.addWidget(save_button)
        
        dialog.exec()

    def save_settings(self, language, theme, refresh_rate, threshold, notifications):
        lang_map = {'English': 'en', 'فارسی': 'fa', '中文': 'zh'}
        self.current_language = lang_map[language]
        self.current_theme = 'light' if theme == translations[self.current_language]['light_theme'] else 'dark'
        
        try:
            refresh_rate = int(refresh_rate)
            threshold = int(threshold)
        except:
            QMessageBox.warning(self, translations[self.current_language]['error'], 
                              "Invalid input for refresh rate or threshold")
            return
        
        self.settings = {
            'language': self.current_language,
            'theme': self.current_theme,
            'refresh_rate': refresh_rate,
            'threshold': threshold,
            'notifications': notifications
        }
        
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
        
        self.update_translations()
        self.apply_theme()
        self.timer.setInterval(refresh_rate)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
            self.current_language = self.settings.get('language', 'en')
            self.current_theme = self.settings.get('theme', 'light')
        except:
            self.settings = {
                'language': 'en',
                'theme': 'light',
                'refresh_rate': 1000,
                'threshold': 80,
                'notifications': False
            }

    def update_translations(self):
        self.trans.loadFromData(json.dumps(translations[self.current_language]).encode())
        QCoreApplication.installTranslator(self.trans)
        self.setWindowTitle(translations[self.current_language]['title'])
        self.update_ui_elements()

    def update_ui_elements(self):
        self.tabs.setTabText(0, translations[self.current_language]['network_info'])
        self.tabs.setTabText(1, translations[self.current_language]['logs'])
        self.tabs.setTabText(2, translations[self.current_language]['statistics'])
        self.start_button.setText(translations[self.current_language]['start_monitor'])
        self.stop_button.setText(translations[self.current_language]['stop_monitor'])
        self.settings_button.setText(translations[self.current_language]['settings'])
        self.export_button.setText(translations[self.current_language]['export'])
        self.clear_button.setText(translations[self.current_language]['clear'])
        self.status_label.setText(translations[self.current_language]['status'] + ': ' + 
                                (translations[self.current_language]['running'] if self.monitoring 
                                 else translations[self.current_language]['stopped']))

    def apply_theme(self):
        palette = QPalette()
        if self.current_theme == 'dark':
            palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            self.signal_plot.setBackground(QColor(45, 45, 45))
            self.bandwidth_plot.setBackground(QColor(45, 45, 45))
            self.packet_plot.setBackground(QColor(45, 45, 45))
            self.latency_plot.setBackground(QColor(45, 45, 45))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
            self.signal_plot.setBackground(QColor(255, 255, 255))
            self.bandwidth_plot.setBackground(QColor(255, 255, 255))
            self.packet_plot.setBackground(QColor(255, 255, 255))
            self.latency_plot.setBackground(QColor(255, 255, 255))
        
        self.setPalette(palette)

    def export_data(self):
        dialog = QFileDialog(self)
        file_type, _ = dialog.getSaveFileName(
            self, translations[self.current_language]['export'],
            '', 'CSV Files (*.csv);;JSON Files (*.json)'
        )
        
        if not file_type:
            return
            
        df = pd.DataFrame(self.network_data)
        if file_type.endswith('.csv'):
            df.to_csv(file_type, index=False)
        else:
            df.to_json(file_type, orient='records')
            
        QMessageBox.information(self, translations[self.current_language]['export'], 
                              f"Data exported to {file_type}")

    def clear_data(self):
        self.network_data.clear()
        self.signal_data.clear()
        self.bandwidth_data.clear()
        self.packet_data.clear()
        self.latency_data.clear()
        self.devices.clear()
        self.logs_text.clear()
        self.network_info.clear()
        self.stats_text.clear()
        self.devices_table.setRowCount(0)
        self.signal_curve.setData([])
        self.bandwidth_curve.setData([])
        self.packet_curve.setData([])
        self.latency_curve.setData([])

    def closeEvent(self, event):
        # self.tray_icon.hide()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    monitor = WiFiMonitor()
    monitor.show()
    sys.exit(app.exec())
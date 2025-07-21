Wi-Fi Network Monitor
A comprehensive Wi-Fi network monitoring application built with Python and PyQt6. This tool provides real-time monitoring of network parameters including signal strength, bandwidth usage, packet rate, latency, and connected devices. It features a user-friendly interface with support for multiple languages (English, Persian, Chinese), light/dark themes, and data export capabilities.
Features

Real-time Monitoring: Tracks signal strength, bandwidth, packet rate, and latency with graphical plots.
Network Information: Displays detailed network information including SSID, BSSID, channel, security, IP address, gateway, and DNS.
Connected Devices: Lists connected devices with their MAC addresses, IP addresses, last seen time, and vendor information.
Multi-language Support: Supports English, Persian (فارسی), and Chinese (中文) with dynamic language switching.
Theming: Offers light and dark themes for better user experience.
Data Export: Export network data to CSV or JSON formats.
System Tray Integration: Minimizes to system tray for background monitoring.
Configurable Settings: Adjustable refresh rate, notification thresholds, and notification toggles.
Logging: Maintains a log of errors and system events.

Prerequisites
To run the Wi-Fi Network Monitor, ensure the following dependencies are installed:

Python: Version 3.8 or higher
PyQt6: For the graphical user interface
psutil: For system resource monitoring
pyqtgraph: For real-time data plotting
pandas: For data handling and export
numpy: For statistical calculations
scapy: For network packet analysis
ping3: For latency measurements
netifaces (optional): For enhanced network interface information (limited functionality if not installed)

Install the required packages using pip:
pip install PyQt6 psutil pyqtgraph pandas numpy scapy ping3 netifaces

Installation

Clone the repository from GitHub:
https://github.com/HamidYaraliOfficial/Wi-Fi-Network-Monitor.git
cd wifi-network-monitor


Install the dependencies:
pip install -r requirements.txt


Create a requirements.txt file with the following content:
PyQt6>=6.7.0
psutil>=5.9.8
pyqtgraph>=0.13.7
pandas>=2.2.2
numpy>=1.26.4
scapy>=2.5.0
ping3>=4.0.8
netifaces>=0.11.0


Place the logo.jpg file in the same directory as WiFi_Network_Monitor.py for the application icon. If not available, the system tray and window icon may not display properly.

Run the application:
python WiFi_Network_Monitor.py



Usage

Select Network Interface: Choose a network interface from the dropdown menu.
Start Monitoring: Click "Start Monitoring" to begin tracking network parameters.
View Data: Monitor real-time graphs for signal strength, bandwidth, packet rate, and latency on the "Network Information" tab.
Check Devices: View connected devices in the table on the right panel.
Logs and Statistics: Access logs and statistical summaries in the respective tabs.
Settings: Adjust language, theme, refresh rate, and notification settings via the "Settings" button.
Export Data: Export collected data to CSV or JSON using the "Export" button.
Clear Data: Reset all collected data with the "Clear" button.
System Tray: Minimize the application to the system tray for background monitoring.

Platform Support

Windows: Fully supported with detailed network information via netsh and arp commands.
Linux/MacOS: Limited functionality due to platform-specific commands. Signal strength and some network details may not be available without additional configuration.

Note: Some features (e.g., signal strength, connected devices) may require administrative privileges or specific network configurations.
Limitations

netifaces: If not installed, some network information (e.g., BSSID, gateway) may not be available.
scapy: Requires administrative privileges for packet sniffing on some systems.
Signal Strength: Currently implemented for Windows only; other platforms return a default value (-100 dBm).
Icon File: Requires a logo.jpg file for proper icon display. Without it, the application will still function but may lack icons.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit (git commit -m "Add feature").
Push to the branch (git push origin feature-branch).
Create a pull request.

Please ensure your code follows PEP 8 guidelines and includes appropriate documentation.
License
This project is licensed under the MIT License. See the LICENSE file for details.

نظارت بر شبکه وای‌فای
یک برنامه نظارت بر شبکه وای‌فای جامع که با Python و PyQt6 ساخته شده است. این ابزار امکان نظارت بر پارامترهای شبکه از جمله قدرت سیگنال، استفاده از پهنای باند، نرخ بسته‌ها، تأخیر و دستگاه‌های متصل را به‌صورت بلادرنگ فراهم می‌کند. این برنامه دارای رابط کاربری ساده با پشتیبانی از چند زبان (انگلیسی، فارسی، چینی)، تم‌های روشن و تیره و قابلیت export داده‌ها است.
ویژگی‌ها

نظارت بلادرنگ: ردیابی قدرت سیگنال، پ.publisherپهنای باند، نرخ بسته‌ها و تأخیر با نمودارهای گرافیکی.
اطلاعات شبکه: نمایش اطلاعات دقیق شبکه از جمله SSID، BSSID، کانال، امنیت، آدرس IP، دروازه و DNS.
دستگاه‌های متصل: نمایش دستگاه‌های متصل با آدرس MAC، آدرس IP، زمان آخرین مشاهده و اطلاعات فروشنده.
پشتیبانی از چند زبان: پشتیبانی از زبان‌های انگلیسی، فارسی و چینی با قابلیت تغییر پویا.
تم‌ها: ارائه تم‌های روشن و تیره برای تجربه کاربری بهتر.
export داده‌ها: امکان export داده‌های شبکه به فرمت‌های CSV یا JSON.
ادغام با System Tray: امکان minimize کردن برنامه در system tray برای نظارت پس‌زمینه.
تنظیمات قابل تنظیم: نرخ به‌روزرسانی، آستانه اعلان‌ها و فعال/غیرفعال کردن اعلان‌ها.
لاگ‌ها: نگهداری لاگ‌های خطاها و رویدادهای سیستم.

پیش‌نیازها
برای اجرای برنامه نظارت بر شبکه وای‌فای، اطمینان حاصل کنید که وابستگی‌های زیر نصب شده‌اند:

Python: نسخه 3.8 یا بالاتر
PyQt6: برای رابط کاربری گرافیکی
psutil: برای نظارت بر منابع سیستم
pyqtgraph: برای رسم داده‌های بلادرنگ
pandas: برای مدیریت و export داده‌ها
numpy: برای محاسبات آماری
scapy: برای تحلیل بسته‌های شبکه
ping3: برای اندازه‌گیری تأخیر
netifaces (اختیاری): برای اطلاعات پیشرفته رابط شبکه (در صورت عدم نصب، برخی قابلیت‌ها محدود می‌شوند)

نصب بسته‌های مورد نیاز با استفاده از pip:
pip install PyQt6 psutil pyqtgraph pandas numpy scapy ping3 netifaces

نصب

مخزن را از GitHub کلون کنید:
https://github.com/HamidYaraliOfficial/Wi-Fi-Network-Monitor.git
cd wifi-network-monitor


وابستگی‌ها را نصب کنید:
pip install -r requirements.txt


فایل requirements.txt را با محتوای زیر ایجاد کنید:
PyQt6>=6.7.0
psutil>=5.9.8
pyqtgraph>=0.13.7
pandas>=2.2.2
numpy>=1.26.4
scapy>=2.5.0
ping3>=4.0.8
netifaces>=0.11.0


فایل logo.jpg را در همان پوشه WiFi_Network_Monitor.py قرار دهید تا آیکون برنامه نمایش داده شود. در صورت عدم وجود، آیکون‌های system tray و پنجره ممکن است به‌درستی نمایش داده نشوند.

برنامه را اجرا کنید:
python WiFi_Network_Monitor.py



استفاده

انتخاب رابط شبکه: یک رابط شبکه را از منوی کشویی انتخاب کنید.
شروع نظارت: روی «شروع نظارت» کلیک کنید تا ردیابی پارامترهای شبکه آغاز شود.
مشاهده داده‌ها: نمودارهای بلادرنگ قدرت سیگنال، پهنای باند، نرخ بسته‌ها و تأخیر را در تب «اطلاعات شبکه» مشاهده کنید.
بررسی دستگاه‌ها: دستگاه‌های متصل را در جدول پنل سمت راست مشاهده کنید.
لاگ‌ها و آمار: لاگ‌ها و خلاصه‌های آماری را در تب‌های مربوطه مشاهده کنید.
تنظیمات: زبان، تم، نرخ به‌روزرسانی و تنظیمات اعلان‌ها را از طریق دکمه «تنظیمات» تنظیم کنید.
export داده‌ها: داده‌های جمع‌آوری‌شده را با استفاده از دکمه «export» به فرمت CSV یا JSON ذخیره کنید.
پاک کردن داده‌ها: تمام داده‌های جمع‌آوری‌شده را با دکمه «پاک کردن» بازنشانی کنید.
System Tray: برنامه را برای نظارت پس‌زمینه به system tray minimize کنید.

پشتیبانی از پلتفرم‌ها

ویندوز: کاملاً پشتیبانی می‌شود با اطلاعات شبکه دقیق از طریق دستورات netsh و arp.
لینوکس/مک‌او‌اس: قابلیت‌های محدود به دلیل دستورات خاص پلتفرم. قدرت سیگنال و برخی اطلاعات شبکه ممکن است بدون تنظیمات اضافی در دسترس نباشند.

توجه: برخی قابلیت‌ها (مانند قدرت سیگنال، دستگاه‌های متصل) ممکن است نیاز به دسترسی‌های مدیریتی یا تنظیمات شبکه خاص داشته باشند.
محدودیت‌ها

netifaces: در صورت عدم نصب، برخی اطلاعات شبکه (مانند BSSID، دروازه) ممکن است در دسترس نباشند.
scapy: نیاز به دسترسی‌های مدیریتی برای تحلیل بسته‌ها در برخی سیستم‌ها دارد.
قدرت سیگنال: در حال حاضر فقط برای ویندوز پیاده‌سازی شده است؛ سایر پلتفرم‌ها مقدار پیش‌فرض (-100 dBm) را برمی‌گردانند.
فایل آیکون: نیاز به فایل logo.jpg برای نمایش صحیح آیکون دارد. بدون آن، برنامه همچنان کار می‌کند اما ممکن است آیکون‌ها نمایش داده نشوند.

مشارکت
از مشارکت‌ها استقبال می‌شود! لطفاً مراحل زیر را دنبال کنید:

مخزن را فورک کنید.
یک شاخه جدید ایجاد کنید (git checkout -b feature-branch).
تغییرات خود را اعمال و کامیت کنید (git commit -m "Add feature").
شاخه را push کنید (git push origin feature-branch).
یک pull request ایجاد کنید.

لطفاً اطمینان حاصل کنید که کد شما از دستورالعمل‌های PEP 8 پیروی می‌کند و مستندات مناسب دارد.
مجوز
این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات، فایل LICENSE را ببینید.


Wi-Fi 网络监控
一个使用 Python 和 PyQt6 构建的全面 Wi-Fi 网络监控应用程序。该工具提供对网络参数的实时监控，包括信号强度、带宽使用量、数据包速率、延迟和连接的设备。它具有用户友好的界面，支持多种语言（英语、波斯语、汉语），提供明亮/暗黑主题以及数据导出功能。
功能

实时监控：跟踪信号强度、带宽、数据包速率和延迟，并显示图形化图表。
网络信息：显示详细的网络信息，包括 SSID、BSSID、频道、安全性、IP 地址、网关和 DNS。
连接的设备：列出连接的设备，包括其 MAC 地址、IP 地址、最后出现时间和供应商信息。
多语言支持：支持英语、波斯语（فارسی）和汉语（中文），并具有动态语言切换功能。
主题：提供明亮和暗黑主题，提升用户体验。
数据导出：将网络数据导出为 CSV 或 JSON 格式。
系统托盘集成：可最小化到系统托盘进行后台监控。
可配置设置：可调整刷新率、通知阈值和通知开关。
日志：记录错误和系统事件的日志。

前提条件
要运行 Wi-Fi 网络监控程序，请确保已安装以下依赖项：

Python：版本 3.8 或更高
PyQt6：用于图形用户界面
psutil：用于系统资源监控
pyqtgraph：用于实时数据绘图
pandas：用于数据处理和导出
numpy：用于统计计算
scapy：用于网络数据包分析
ping3：用于延迟测量
netifaces（可选）：用于增强的网络接口信息（未安装时部分功能受限）

使用 pip 安装所需包：
pip install PyQt6 psutil pyqtgraph pandas numpy scapy ping3 netifaces

安装

从 GitHub 克隆仓库：
https://github.com/HamidYaraliOfficial/Wi-Fi-Network-Monitor.git
cd wifi-network-monitor


安装依赖项：
pip install -r requirements.txt


创建一个包含以下内容的 requirements.txt 文件：
PyQt6>=6.7.0
psutil>=5.9.8
pyqtgraph>=0.13.7
pandas>=2.2.2
numpy>=1.26.4
scapy>=2.5.0
ping3>=4.0.8
netifaces>=0.11.0


将 logo.jpg 文件放置在与 WiFi_Network_Monitor.py 相同的目录中，用于应用程序图标。如果没有此文件，系统托盘和窗口图标可能无法正常显示。

运行应用程序：
python WiFi_Network_Monitor.py



使用方法

选择网络接口：从下拉菜单中选择一个网络接口。
开始监控：单击“开始监控”以开始跟踪网络参数。
查看数据：在“网络信息”选项卡中监控信号强度、带宽、数据包速率和延迟的实时图表。
检查设备：在右侧面板的表格中查看连接的设备。
日志和统计：在相应的选项卡中访问日志和统计摘要。
设置：通过“设置”按钮调整语言、主题、刷新率和通知设置。
导出数据：使用“导出”按钮将收集的数据导出为 CSV 或 JSON 格式。
清除数据：使用“清除”按钮重置所有收集的数据。
系统托盘：将应用程序最小化到系统托盘进行后台监控。

平台支持

Windows：完全支持，通过 netsh 和 arp 命令提供详细的网络信息。
Linux/MacOS：由于平台特定的命令，功能受限。信号强度和一些网络详细信息可能需要额外配置。

注意：某些功能（例如信号强度、连接的设备）可能需要管理员权限或特定的网络配置。
限制

netifaces：如果未安装，某些网络信息（例如 BSSID、网关）可能不可用。
scapy：在某些系统上需要管理员权限进行数据包嗅探。
信号强度：目前仅针对 Windows 实现；其他平台返回默认值 (-100 dBm)。
图标文件：需要 logo.jpg 文件以正确显示图标。如果没有此文件，应用程序仍可运行，但可能缺少图标。

贡献
欢迎贡献！请按照以下步骤操作：

叉取仓库。
创建一个新分支（git checkout -b feature-branch）。
进行更改并提交（git commit -m "Add feature"）。
推送到分支（git push origin feature-branch）。
创建一个拉取请求。

请确保您的代码遵循 PEP 8 准则并包含适当的文档。
许可证
本项目采用 MIT 许可证发布。有关详细信息，请参阅 LICENSE 文件。

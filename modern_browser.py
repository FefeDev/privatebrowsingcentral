import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, 
    QTabWidget, QToolBar, QAction, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QFontDatabase

class PrivacyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Privacy Browser")
        self.setGeometry(100, 100, 1200, 800)
        self.initUI()

    def initUI(self):
        self.apply_dark_theme()
        self.load_custom_font()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)

        # Back button
        back_action = QAction("Back", self)
        back_action.triggered.connect(self.navigate_back)
        self.toolbar.addAction(back_action)

        # Forward button
        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(forward_action)

        # Refresh button
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_page)
        self.toolbar.addAction(refresh_action)

        # New Tab button
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_action)

        # Clear History button
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        self.toolbar.addAction(clear_history_action)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Add initial tab
        self.add_new_tab(QUrl("https://duckduckgo.com"))

    def add_new_tab(self, qurl=None):
        if qurl is None or not isinstance(qurl, QUrl):
            qurl = QUrl("https://duckduckgo.com")  # Default to DuckDuckGo
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if url.startswith("www."):
            url = "http://" + url
        elif not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://duckduckgo.com/?q={url}"
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_urlbar(self, qurl, browser=None):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())
            self.url_bar.setCursorPosition(0)

    def navigate_back(self):
        self.tabs.currentWidget().back()

    def navigate_forward(self):
        self.tabs.currentWidget().forward()

    def refresh_page(self):
        self.tabs.currentWidget().reload()

    def apply_dark_theme(self):
        palette = QPalette()
        dark_gray = QColor(40, 40, 40)
        light_gray = QColor(200, 200, 200)
        palette.setColor(QPalette.Window, dark_gray)
        palette.setColor(QPalette.WindowText, light_gray)
        palette.setColor(QPalette.Base, dark_gray)
        palette.setColor(QPalette.AlternateBase, dark_gray)
        palette.setColor(QPalette.ToolTipBase, light_gray)
        palette.setColor(QPalette.ToolTipText, light_gray)
        palette.setColor(QPalette.Text, light_gray)
        palette.setColor(QPalette.Button, dark_gray)
        palette.setColor(QPalette.ButtonText, light_gray)
        palette.setColor(QPalette.Highlight, QColor(60, 60, 60))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282828;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #404040;
                border-radius: 10px;
                padding: 5px 15px;
                margin: 5px;
                color: #ffffff;
            }
            QTabBar::tab:selected {
                background: #606060;
            }
            QLineEdit {
                background: #404040;
                border: 1px solid #606060;
                border-radius: 10px;
                padding: 5px;
                color: #ffffff;
            }
            QToolBar {
                background: #303030;
                border: none;
            }
            QPushButton, QToolButton {
                background: #404040;
                border-radius: 10px;
                padding: 5px 10px;
                color: #ffffff;
            }
            QPushButton:hover, QToolButton:hover {
                background: #505050;
            }
        """)

    def load_custom_font(self):
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Poppins-SemiBold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            self.setFont(QFont("Poppins"))

    def clear_history(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()
        profile.cookieStore().deleteAllCookies()
        QMessageBox.information(self, "History Cleared", "Browsing history and cookies have been cleared!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = PrivacyBrowser()
    browser.show()
    sys.exit(app.exec_())

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QToolBar,
    QMenu, QMenuBar, QStatusBar, QFileDialog, QSplitter,
    QLabel, QComboBox, QMessageBox, QDialog, QLineEdit,
    QPushButton, QSpinBox, QTabWidget
)
from PyQt6.QtCore import Qt, QSettings, QSize, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QFont, QTextCursor

from src.ui.document_view import DocumentView
from src.ui.settings_dialog import SettingsDialog

import os


class MainWindow(QMainWindow):
    """
    Main application window for IlluminAI Document Reader.
    """

    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("IlluminAI Document Reader")
        self.setMinimumSize(800, 600)

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Initialize settings
        self.settings = QSettings()

        # Initialize UI components first
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()

        # Now restore window settings and apply them
        self.restore_window_settings()

        # Connect signals and slots
        self.connect_signals()

    def setup_ui(self):
        """Set up the main UI components."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create tab widget for multiple documents
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tab_widget)

        # Welcome message when no documents are open
        self.welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_widget)
        welcome_label = QLabel("Welcome to IlluminAI Document Reader")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont("Arial", 16))
        welcome_layout.addWidget(welcome_label)

        instructions_label = QLabel(
            "Open a document to get started or drag and drop a file here.")
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(instructions_label)

        self.tab_widget.addTab(self.welcome_widget, "Welcome")
        # Don't allow closing the welcome tab
        self.tab_widget.setTabsClosable(False)

    def setup_menu(self):
        """Set up the application menu bar."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")

        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Settings menu
        settings_menu = self.menuBar().addMenu("&Settings")

        preferences_action = QAction("&Preferences...", self)
        preferences_action.triggered.connect(self.show_settings)
        settings_menu.addAction(preferences_action)

        # Help menu
        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Add help action
        help_action = QAction("&User Guide", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def setup_toolbar(self):
        """Set up the application toolbar."""
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Add open document button
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_document)
        self.toolbar.addAction(open_action)

        self.toolbar.addSeparator()

        # Add LLM provider selector
        self.toolbar.addWidget(QLabel("LLM Provider: "))
        self.llm_selector = QComboBox()
        self.llm_selector.addItems(
            ["Claude (Anthropic)", "GPT (OpenAI)", "Grok (xAI)"])

        # Set default provider from settings
        default_provider = self.settings.value(
            "default_llm_provider", 0, type=int)
        self.llm_selector.setCurrentIndex(default_provider)

        self.toolbar.addWidget(self.llm_selector)

        self.toolbar.addSeparator()

        # Add token limit selector
        self.toolbar.addWidget(QLabel("Token Limit: "))
        self.token_limit = QSpinBox()
        self.token_limit.setRange(1000, 100000)
        self.token_limit.setSingleStep(1000)

        # Set default token limit from settings
        default_token_limit = self.settings.value(
            "default_token_limit", 8000, type=int)
        self.token_limit.setValue(default_token_limit)

        self.toolbar.addWidget(self.token_limit)

    def setup_statusbar(self):
        """Set up the status bar."""
        self.statusBar().showMessage("Ready")

    def connect_signals(self):
        """Connect signals and slots."""
        # Connected in their respective setup methods
        pass

    def open_document(self):
        """Open a document file dialog."""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(
            "Documents (*.pdf *.txt *.rtf *.docx *.odt *.md);;All Files (*)"
        )

        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.load_document(file_path)

    def load_document(self, file_path):
        """Load a document from the given file path."""
        try:
            # Check if the file exists
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Get file extension
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            # Check if the file type is supported
            from src.document_handlers.document_factory import DocumentFactory
            if ext not in DocumentFactory.supported_extensions():
                QMessageBox.warning(
                    self,
                    "Unsupported File Type",
                    f"The file type '{ext}' is not supported. Supported types: " +
                    ", ".join(DocumentFactory.supported_extensions())
                )
                return

            # Remove welcome tab if it's the only tab
            if self.tab_widget.count() == 1 and self.tab_widget.tabText(0) == "Welcome":
                self.tab_widget.removeTab(0)
                self.tab_widget.setTabsClosable(True)

            # Create a new document view and pass the file path
            document_view = DocumentView(self)
            document_view.load_document(file_path)

            # Add the document view as a new tab
            file_name = os.path.basename(file_path)
            tab_index = self.tab_widget.addTab(document_view, file_name)
            self.tab_widget.setCurrentIndex(tab_index)

            # Update status
            self.statusBar().showMessage(f"Loaded document: {file_path}")

            # Save to recent files
            self.add_to_recent_files(file_path)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to open document: {str(e)}")
            self.statusBar().showMessage("Error loading document")

    def close_tab(self, index):
        """Close the tab at the given index."""
        self.tab_widget.removeTab(index)

        # Show welcome tab if no tabs are left
        if self.tab_widget.count() == 0:
            self.tab_widget.addTab(self.welcome_widget, "Welcome")
            self.tab_widget.setTabsClosable(False)

    def show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        dialog.settings_changed.connect(self.apply_settings)
        dialog.exec()

    def apply_settings(self):
        """Apply settings changes."""
        # Update the LLM provider and token limit from settings
        default_provider = self.settings.value(
            "default_llm_provider", 0, type=int)
        self.llm_selector.setCurrentIndex(default_provider)

        default_token_limit = self.settings.value(
            "default_token_limit", 8000, type=int)
        self.token_limit.setValue(default_token_limit)

        # Apply font size settings
        font_size = self.settings.value("font_size", 12, type=int)
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        # Apply dark mode settings
        dark_mode = self.settings.value("dark_mode", False, type=bool)
        if dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #2d2d2d; color: #e0e0e0; }
                QTextEdit { background-color: #1e1e1e; color: #e0e0e0; border: 1px solid #3d3d3d; }
                QMenuBar, QToolBar { background-color: #2d2d2d; color: #e0e0e0; }
                QMenu { background-color: #2d2d2d; color: #e0e0e0; }
                QMenu::item:selected { background-color: #3d3d3d; }
                QTabWidget::pane { border: 1px solid #3d3d3d; }
                QTabBar::tab { background-color: #2d2d2d; color: #e0e0e0; padding: 5px; }
                QTabBar::tab:selected { background-color: #3d3d3d; }
                QPushButton { background-color: #3d3d3d; color: #e0e0e0; padding: 5px; border: 1px solid #5d5d5d; }
                QPushButton:hover { background-color: #4d4d4d; }
                QLineEdit, QSpinBox, QComboBox { background-color: #1e1e1e; color: #e0e0e0; border: 1px solid #3d3d3d; padding: 3px; }
            """)
        else:
            self.setStyleSheet("")  # Reset to default style

    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About IlluminAI",
            "IlluminAI Document Reader\n\n"
            "An open-source document reader with AI-powered interaction.\n\n"
            "Version 0.1.0"
        )

    def show_help(self):
        """Show the help dialog with usage instructions."""
        help_text = """
<h2>IlluminAI Document Reader - User Guide</h2>

<h3>Opening Documents</h3>
<ul>
<li>Use the File menu or Open button to open a document</li>
<li>You can also drag and drop files directly into the application</li>
<li>Supported formats: PDF, TXT, DOCX, RTF, ODT, MD, and more</li>
</ul>

<h3>Using AI Features</h3>
<ul>
<li>Select text in the document with your mouse</li>
<li>Right-click on the selected text to see AI options</li>
<li>Choose from:</li>
  <ul>
  <li>"Explain like I'm 5" - Get a simple explanation</li>
  <li>"Summarize this" - Get a concise summary</li>
  <li>"Ask a question..." - Ask a specific question about the text</li>
  </ul>
</ul>

<h3>Customizing Settings</h3>
<ul>
<li>In the Settings menu, choose Preferences to configure:</li>
  <ul>
  <li>LLM providers and API keys</li>
  <li>Default token limits</li>
  <li>UI preferences</li>
  </ul>
</ul>

<h3>Tips for Best Results</h3>
<ul>
<li>For large documents, select specific sections for better results</li>
<li>The token counter shows how much text will be sent to the LLM</li>
<li>Be specific with your questions to get more accurate responses</li>
</ul>
"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("User Guide")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(help_text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def restore_window_settings(self):
        """Restore saved window position and size."""
        position = self.settings.value("windowPosition", QPoint(100, 100))
        size = self.settings.value("windowSize", QSize(800, 600))
        self.move(position)
        self.resize(size)

        # Apply stored settings
        self.apply_settings()

    def closeEvent(self, event):
        """Handle window close event to save settings."""
        self.settings.setValue("windowPosition", self.pos())
        self.settings.setValue("windowSize", self.size())
        super().closeEvent(event)

    def add_to_recent_files(self, file_path):
        """Add a file to the list of recently opened files."""
        recent_files = self.settings.value("recentFiles", [], type=list)

        # Remove the file path if it already exists in the list
        if file_path in recent_files:
            recent_files.remove(file_path)

        # Add the file path to the beginning of the list
        recent_files.insert(0, file_path)

        # Keep only the 10 most recent files
        recent_files = recent_files[:10]

        # Save the updated list
        self.settings.setValue("recentFiles", recent_files)

    def dragEnterEvent(self, event):
        """Handle drag enter events for drag and drop file opening."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                # Check if the file has a supported extension
                file_path = urls[0].toLocalFile()
                _, ext = os.path.splitext(file_path)
                ext = ext.lower()

                # Import here to avoid circular imports
                from src.document_handlers.document_factory import DocumentFactory
                if ext in DocumentFactory.supported_extensions():
                    event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop events for drag and drop file opening."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                file_path = urls[0].toLocalFile()
                self.load_document(file_path)
                event.acceptProposedAction()

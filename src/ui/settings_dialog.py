from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QWidget, QFormLayout,
    QSpinBox, QComboBox, QCheckBox, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal


class APIKeyWidget(QWidget):
    """
    Widget for managing API keys for LLM providers.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings()

        # Create layout
        layout = QVBoxLayout(self)

        # Anthropic API Key
        anthropic_group = QGroupBox("Anthropic (Claude)")
        anthropic_layout = QFormLayout(anthropic_group)

        self.anthropic_api_key = QLineEdit()
        self.anthropic_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.anthropic_api_key.setText(
            self.settings.value("anthropic_api_key", ""))
        anthropic_layout.addRow("API Key:", self.anthropic_api_key)

        # Test button for Anthropic
        test_anthropic_button = QPushButton("Test Connection")
        test_anthropic_button.clicked.connect(
            lambda: self.test_connection("anthropic"))
        anthropic_layout.addRow("", test_anthropic_button)

        layout.addWidget(anthropic_group)

        # OpenAI API Key
        openai_group = QGroupBox("OpenAI (GPT)")
        openai_layout = QFormLayout(openai_group)

        self.openai_api_key = QLineEdit()
        self.openai_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_api_key.setText(self.settings.value("openai_api_key", ""))
        openai_layout.addRow("API Key:", self.openai_api_key)

        # Test button for OpenAI
        test_openai_button = QPushButton("Test Connection")
        test_openai_button.clicked.connect(
            lambda: self.test_connection("openai"))
        openai_layout.addRow("", test_openai_button)

        layout.addWidget(openai_group)

        # xAI API Key
        xai_group = QGroupBox("xAI (Grok)")
        xai_layout = QFormLayout(xai_group)

        self.xai_api_key = QLineEdit()
        self.xai_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.xai_api_key.setText(self.settings.value("xai_api_key", ""))
        xai_layout.addRow("API Key:", self.xai_api_key)

        # Test button for xAI
        test_xai_button = QPushButton("Test Connection")
        test_xai_button.clicked.connect(lambda: self.test_connection("xai"))
        xai_layout.addRow("", test_xai_button)

        layout.addWidget(xai_group)

        # Add some vertical space
        layout.addStretch()

    def save_settings(self):
        """Save API key settings."""
        self.settings.setValue("anthropic_api_key",
                               self.anthropic_api_key.text())
        self.settings.setValue("openai_api_key", self.openai_api_key.text())
        self.settings.setValue("xai_api_key", self.xai_api_key.text())

    def test_connection(self, provider):
        """Test the connection to the LLM provider."""
        # In a real application, this would make a test API call
        # For now, just show a message if the API key is set
        api_key = ""

        if provider == "anthropic":
            api_key = self.anthropic_api_key.text()
            provider_name = "Anthropic"
        elif provider == "openai":
            api_key = self.openai_api_key.text()
            provider_name = "OpenAI"
        elif provider == "xai":
            api_key = self.xai_api_key.text()
            provider_name = "xAI"

        if not api_key:
            QMessageBox.warning(
                self,
                "Connection Test",
                f"Please enter an API key for {provider_name}."
            )
        else:
            # For demonstration purposes
            QMessageBox.information(
                self,
                "Connection Test",
                f"API key for {provider_name} is set. In a real application, this would test the connection."
            )


class PreferencesWidget(QWidget):
    """
    Widget for setting application preferences.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings()

        # Create layout
        layout = QVBoxLayout(self)

        # LLM Settings
        llm_group = QGroupBox("LLM Settings")
        llm_layout = QFormLayout(llm_group)

        # Default LLM Provider
        self.default_provider = QComboBox()
        self.default_provider.addItems(
            ["Claude (Anthropic)", "GPT (OpenAI)", "Grok (xAI)"])
        default_index = self.settings.value(
            "default_llm_provider", 0, type=int)
        self.default_provider.setCurrentIndex(default_index)
        llm_layout.addRow("Default Provider:", self.default_provider)

        # Default token limit
        self.default_token_limit = QSpinBox()
        self.default_token_limit.setRange(1000, 100000)
        self.default_token_limit.setSingleStep(1000)
        self.default_token_limit.setValue(
            self.settings.value("default_token_limit", 8000, type=int))
        llm_layout.addRow("Default Token Limit:", self.default_token_limit)

        layout.addWidget(llm_group)

        # UI Settings
        ui_group = QGroupBox("UI Settings")
        ui_layout = QFormLayout(ui_group)

        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(self.settings.value("font_size", 12, type=int))
        ui_layout.addRow("Font Size:", self.font_size)

        # Dark mode
        self.dark_mode = QCheckBox("Enable Dark Mode")
        self.dark_mode.setChecked(
            self.settings.value("dark_mode", False, type=bool))
        ui_layout.addRow("", self.dark_mode)

        layout.addWidget(ui_group)

        # Add some vertical space
        layout.addStretch()

    def save_settings(self):
        """Save preference settings."""
        self.settings.setValue("default_llm_provider",
                               self.default_provider.currentIndex())
        self.settings.setValue("default_token_limit",
                               self.default_token_limit.value())
        self.settings.setValue("font_size", self.font_size.value())
        self.settings.setValue("dark_mode", self.dark_mode.isChecked())


class SettingsDialog(QDialog):
    """
    Dialog for configuring application settings.
    """

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.resize(500, 400)

        # Create layout
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Create API keys tab
        self.api_keys_widget = APIKeyWidget()
        self.tab_widget.addTab(self.api_keys_widget, "API Keys")

        # Create preferences tab
        self.preferences_widget = PreferencesWidget()
        self.tab_widget.addTab(self.preferences_widget, "Preferences")

        layout.addWidget(self.tab_widget)

        # Create buttons
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        ok_button = QPushButton("OK")
        ok_button.setDefault(True)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)

    def accept(self):
        """Save settings and close dialog."""
        self.api_keys_widget.save_settings()
        self.preferences_widget.save_settings()
        self.settings_changed.emit()
        super().accept()

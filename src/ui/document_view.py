import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QTextEdit,
    QLabel, QPushButton, QMenu, QDialog, QLineEdit,
    QMessageBox, QSizePolicy, QToolBar, QProgressBar, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QThread, QObject
from PyQt6.QtGui import QTextCursor, QColor, QAction, QContextMenuEvent, QTextCharFormat, QTextDocument

from src.document_handlers.document_factory import DocumentFactory
from src.llm_providers.llm_service import LLMService
from src.utils.token_counter import count_tokens, get_context_with_token_limit
from src.ui.pdf_view_widget import PDFViewWidget


class DocumentView(QWidget):
    """
    Widget for displaying and interacting with a document.
    Handles text selection and LLM integration.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Document properties
        self.document_content = ""
        self.current_selection = ""
        self.current_file_path = None
        self.document_handler = None
        self.is_pdf = False

        # Initialize UI components
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Set up the UI components."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a stacked widget to switch between text view and PDF view
        self.view_stack = QStackedWidget()

        # Text area for displaying document content
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.text_display.customContextMenuRequested.connect(
            self.show_context_menu)
        self.text_display.selectionChanged.connect(self.text_selection_changed)

        # Add text display to the stacked widget
        self.view_stack.addWidget(self.text_display)

        # PDF view for displaying PDF documents visually
        self.pdf_view = PDFViewWidget()
        self.pdf_view.text_selected.connect(self.pdf_text_selected)

        # Add PDF view to the stacked widget
        self.view_stack.addWidget(self.pdf_view)

        # Add the stacked widget to the layout
        layout.addWidget(self.view_stack)

        # Area for displaying LLM responses
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        self.response_area.setVisible(False)
        self.response_area.setMaximumHeight(200)
        self.response_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        # Add a header for the response area
        self.response_header = QWidget()
        response_header_layout = QHBoxLayout(self.response_header)
        response_header_layout.setContentsMargins(0, 0, 0, 0)

        self.response_label = QLabel("AI Response")
        response_header_layout.addWidget(self.response_label)

        close_button = QPushButton("×")
        close_button.setMaximumSize(20, 20)
        close_button.clicked.connect(self.hide_response_area)
        response_header_layout.addWidget(close_button)

        # Add a loading indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(0)  # Indeterminate progress bar
        self.progress_bar.setMaximumHeight(5)
        self.progress_bar.setVisible(False)

        # Add widgets to layout
        layout.addWidget(self.response_header)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.response_area)

        self.response_header.setVisible(False)

    def connect_signals(self):
        """Connect signals to methods."""
        # Context menu for PDF view is handled through the text_selected signal
        pass

    def load_document(self, file_path):
        """Load a document from the given file path."""
        try:
            # Use the document factory to create the appropriate handler
            self.document_handler = DocumentFactory.create_handler(file_path)

            if self.document_handler is None:
                raise Exception(
                    f"Unsupported file type or failed to open document")

            # Get the document content
            self.document_content = self.document_handler.get_text()

            # Get file extension
            _, ext = os.path.splitext(file_path)
            self.is_pdf = ext.lower() == ".pdf"

            # If it's a PDF and visual rendering is supported, use the PDF view
            if self.is_pdf and hasattr(self.document_handler, 'supports_visual_rendering') and self.document_handler.supports_visual_rendering():
                # Load the PDF into the PDF view widget
                pdf_document = self.document_handler.get_visual_document()
                self.pdf_view.load_document(file_path)
                self.view_stack.setCurrentWidget(self.pdf_view)
            else:
                # For non-PDF documents or if visual rendering is not supported, use text display
                self.text_display.setPlainText(self.document_content)
                self.view_stack.setCurrentWidget(self.text_display)

            # Store the file path
            self.current_file_path = file_path

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to load document: {str(e)}")

    def text_selection_changed(self):
        """Handle selection change in the text display."""
        cursor = self.text_display.textCursor()
        if cursor.hasSelection():
            self.current_selection = cursor.selectedText()
        else:
            self.current_selection = ""

    def pdf_text_selected(self, text):
        """Handle text selection from the PDF view."""
        self.current_selection = text

        # Show context menu if there's a selection
        if text:
            # Create and show the context menu
            menu = QMenu(self)

            explain_action = QAction("Explain like I'm 5", self)
            explain_action.triggered.connect(
                lambda: self.process_with_llm("explain"))
            menu.addAction(explain_action)

            summarize_action = QAction("Summarize this", self)
            summarize_action.triggered.connect(
                lambda: self.process_with_llm("summarize"))
            menu.addAction(summarize_action)

            ask_action = QAction("Ask a question...", self)
            ask_action.triggered.connect(self.ask_question)
            menu.addAction(ask_action)

            # Add token count info
            token_count = count_tokens(self.current_selection)
            menu.addSeparator()
            token_info_action = QAction(
                f"Selection: ~{token_count} tokens", self)
            token_info_action.setEnabled(False)
            menu.addAction(token_info_action)

            # Show the menu at the cursor position
            cursor_pos = self.pdf_view.cursor().pos()
            menu.exec(cursor_pos)

    def show_context_menu(self, position):
        """Show custom context menu when right-clicking in text display."""
        cursor = self.text_display.textCursor()
        if not cursor.hasSelection():
            # If no selection, show the default context menu
            default_menu = self.text_display.createStandardContextMenu()
            default_menu.exec(self.text_display.mapToGlobal(position))
            return

        # Create custom context menu for LLM interactions
        menu = QMenu(self)

        explain_action = QAction("Explain like I'm 5", self)
        explain_action.triggered.connect(
            lambda: self.process_with_llm("explain"))
        menu.addAction(explain_action)

        summarize_action = QAction("Summarize this", self)
        summarize_action.triggered.connect(
            lambda: self.process_with_llm("summarize"))
        menu.addAction(summarize_action)

        ask_action = QAction("Ask a question...", self)
        ask_action.triggered.connect(self.ask_question)
        menu.addAction(ask_action)

        # Add token count info
        if self.current_selection:
            token_count = count_tokens(self.current_selection)
            menu.addSeparator()
            token_info_action = QAction(
                f"Selection: ~{token_count} tokens", self)
            token_info_action.setEnabled(False)
            menu.addAction(token_info_action)

        menu.exec(self.text_display.mapToGlobal(position))

    def process_with_llm(self, action_type, question=None):
        """Process selected text with LLM based on the action type."""
        # Get the current LLM provider and token limit from the parent MainWindow
        parent = self.parent()
        while parent and not hasattr(parent, 'llm_selector'):
            parent = parent.parent()

        if not parent:
            QMessageBox.warning(
                self, "Error", "Could not access LLM settings.")
            return

        # Get current provider and token limit
        provider_index = parent.llm_selector.currentIndex()
        provider_name = parent.llm_selector.currentText()
        token_limit = parent.token_limit.value()

        # Get context (current selection + surrounding text if needed)
        context = self.get_context_with_surroundings(
            token_limit, provider_name)

        # Prepare prompt based on action type
        if action_type == "explain":
            prompt = f"Explain the following text as if I'm 5 years old:\n\n{context}"
        elif action_type == "summarize":
            prompt = f"Summarize the following text concisely:\n\n{context}"
        elif action_type == "ask":
            if not question:
                return
            prompt = f"Answer this question about the following text: '{question}'\n\n{context}"

        # Show loading indicator
        self.show_loading()

        # Initialize LLM service
        llm_service = LLMService(provider_name)

        # Create a worker thread for the API call
        self.llm_thread = LLMThread(llm_service, prompt)
        self.llm_thread.response_ready.connect(self.handle_llm_response)
        self.llm_thread.error_occurred.connect(self.handle_llm_error)
        self.llm_thread.start()

    def get_context_with_surroundings(self, token_limit, provider_name):
        """
        Get the selected text with surrounding context up to the token limit.
        For large documents, include context before and after selection.
        Uses the token counter utility for accurate token counting.
        """
        # If we're in PDF view, just use the current selection
        if self.view_stack.currentWidget() == self.pdf_view:
            return self.current_selection

        # For text display
        cursor = self.text_display.textCursor()
        if not cursor.hasSelection():
            return ""

        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()

        # Use the utility function to get context with token limits
        return get_context_with_token_limit(
            self.document_content,
            selection_start,
            selection_end,
            token_limit,
            provider_name
        )

    def ask_question(self):
        """Show dialog to ask a question about the selected text."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ask a Question")

        layout = QVBoxLayout(dialog)

        question_edit = QLineEdit()
        question_edit.setPlaceholderText(
            "Enter your question about the selected text...")
        layout.addWidget(question_edit)

        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)

        ask_button = QPushButton("Ask")
        ask_button.setDefault(True)
        ask_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ask_button)

        layout.addLayout(button_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            question = question_edit.text().strip()
            if question:
                self.process_with_llm("ask", question)

    def show_loading(self):
        """Show loading indicator while waiting for LLM response."""
        self.response_header.setVisible(True)
        self.response_area.setVisible(True)
        self.response_area.setPlainText("Processing your request...")
        self.progress_bar.setVisible(True)

    def handle_llm_response(self, response):
        """Handle the LLM response when it's ready."""
        self.progress_bar.setVisible(False)
        self.response_area.setPlainText(response)

    def handle_llm_error(self, error_message):
        """Handle errors in LLM processing."""
        self.progress_bar.setVisible(False)
        self.response_area.setPlainText(f"Error: {error_message}")

    def hide_response_area(self):
        """Hide the response area."""
        self.response_header.setVisible(False)
        self.response_area.setVisible(False)
        self.progress_bar.setVisible(False)


class LLMThread(QThread):
    """
    Worker thread for LLM API calls to prevent UI freezing.
    """
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, llm_service, prompt):
        super().__init__()
        self.llm_service = llm_service
        self.prompt = prompt

    def run(self):
        """Run the LLM request in a separate thread."""
        try:
            response = self.llm_service.process(self.prompt)
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))

"""
PDF View Widget for rendering PDFs visually.

This widget provides a macOS Preview-like experience for PDF files,
showing the full visual layout including text formatting, images, and figures.
"""

from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QToolBar, QSplitter,
    QSlider, QComboBox, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QRectF, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QImage, QKeySequence, QAction

# Try to import fitz (PyMuPDF) for PDF rendering
try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available. Install with: pip install pymupdf")


class PDFPageWidget(QWidget):
    """Widget for displaying a single PDF page."""

    text_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.page_image = None
        self.page_number = 0
        self.zoom_factor = 1.0
        self.setMinimumSize(600, 800)

        # Text blocks for selection
        self.text_blocks = []
        self.selected_blocks = []

        # Mouse selection tracking
        self.selection_start_pos = None
        self.selection_current_pos = None
        self.is_selecting = False

        print("PDFPageWidget initialized")

    def load_page(self, pdf_document, page_number, zoom_factor=1.0):
        """
        Load and render a page from the PDF document.

        Args:
            pdf_document: The fitz PDF document
            page_number: Page number to render (0-indexed)
            zoom_factor: Zoom level
        """
        if not PYMUPDF_AVAILABLE:
            self.render_placeholder()
            return

        self.page_number = page_number
        self.zoom_factor = zoom_factor

        try:
            # Get the page
            page = pdf_document[page_number]

            # Render to pixmap at desired zoom level with higher DPI
            # Use a higher resolution matrix for better quality
            matrix = fitz.Matrix(zoom_factor, zoom_factor)

            # Set the DPI to 150 (good quality but not extreme) for rendering
            # The default is 72 DPI which can look low-resolution
            pixmap = page.get_pixmap(matrix=matrix, alpha=False, dpi=150)

            # Convert to QImage with RGB format
            img_data = pixmap.samples
            img_format = QImage.Format.Format_RGB888
            image = QImage(img_data, pixmap.width, pixmap.height,
                           pixmap.stride, img_format)

            # Convert to QPixmap for display, setting high-quality conversion
            self.page_image = QPixmap.fromImage(
                image, Qt.ImageConversionFlag.AutoColor)

            print(
                f">>> Loaded page {page_number + 1} at zoom factor {zoom_factor}, size: {self.page_image.width()}x{self.page_image.height()}")

            # Extract text blocks for selection
            self.text_blocks = []
            for block in page.get_text("blocks"):
                self.text_blocks.append({
                    "rect": QRectF(
                        block[0] * zoom_factor,
                        block[1] * zoom_factor,
                        (block[2] - block[0]) * zoom_factor,
                        (block[3] - block[1]) * zoom_factor
                    ),
                    "text": block[4]
                })

            print(f">>> Found {len(self.text_blocks)} text blocks in the page")

            # Update widget size
            self.setMinimumSize(self.page_image.size())
            self.resize(self.page_image.size())
            self.update()

        except Exception as e:
            print(f"Error rendering PDF page: {e}")
            self.render_placeholder()

    def render_placeholder(self):
        """Render a placeholder when PDF can't be displayed."""
        width, height = 600, 800
        self.page_image = QPixmap(width, height)
        self.page_image.fill(QColor(240, 240, 240))

        painter = QPainter(self.page_image)
        painter.setPen(QColor(120, 120, 120))
        painter.drawText(
            QRectF(0, 0, width, height),
            Qt.AlignmentFlag.AlignCenter,
            "PDF rendering not available.\nPlease install PyMuPDF:\npip install pymupdf"
        )
        painter.end()

        self.setMinimumSize(width, height)
        self.resize(width, height)
        self.update()

    def paintEvent(self, event):
        """Handle paint events to draw the PDF page."""
        if not self.page_image:
            return

        painter = QPainter(self)

        # Enable antialiasing for smoother rendering
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # Draw the page image
        painter.drawPixmap(0, 0, self.page_image)

        # Draw selected text blocks with highlight
        painter.setBrush(QColor(100, 155, 255, 80))  # Semi-transparent blue
        painter.setPen(Qt.PenStyle.NoPen)

        for block_idx in self.selected_blocks:
            if 0 <= block_idx < len(self.text_blocks):
                rect = self.text_blocks[block_idx]["rect"]
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        """Handle mouse press for text selection."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Start new selection
            self.selected_blocks = []
            self.is_selecting = True
            self.selection_start_pos = event.position()

            # Find the block under the cursor
            pos = event.position()
            for i, block in enumerate(self.text_blocks):
                if block["rect"].contains(pos):
                    self.selected_blocks.append(i)
                    print(
                        f">>> Started selection on block {i}: {self.text_blocks[i]['text'][:30]}...")
                    break

            self.update()

    def mouseMoveEvent(self, event):
        """Handle mouse movement for extending text selection."""
        if self.is_selecting:
            self.selection_current_pos = event.position()

            # Find blocks that intersect with the selection rectangle
            selection_rect = QRectF(
                min(self.selection_start_pos.x(),
                    self.selection_current_pos.x()),
                min(self.selection_start_pos.y(),
                    self.selection_current_pos.y()),
                abs(self.selection_current_pos.x() -
                    self.selection_start_pos.x()),
                abs(self.selection_current_pos.y() -
                    self.selection_start_pos.y())
            )

            # Debug the selection rectangle
            print(
                f">>> Selection rectangle: {selection_rect.x():.1f},{selection_rect.y():.1f} - {selection_rect.width():.1f}x{selection_rect.height():.1f}")

            # Update selection to include all blocks that intersect with the selection rectangle
            self.selected_blocks = []
            for i, block in enumerate(self.text_blocks):
                if selection_rect.intersects(block["rect"]):
                    self.selected_blocks.append(i)

            print(
                f">>> Selected {len(self.selected_blocks)} blocks during drag")
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release after selection."""
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.is_selecting = False

            print(
                f">>> Mouse released, finalizing selection of {len(self.selected_blocks)} blocks")

            # Combine text from selected blocks
            selected_text = ""
            for block_idx in sorted(self.selected_blocks):
                if 0 <= block_idx < len(self.text_blocks):
                    selected_text += self.text_blocks[block_idx]["text"] + " "

            # Emit signal with selected text
            if selected_text.strip():
                print(f">>> FINAL TEXT SELECTED: {selected_text[:50]}...")
                self.text_selected.emit(selected_text.strip())

                # Show a temporary message to confirm text was selected
                print(">>> Signal was emitted for selected text")

            # Even if no text is selected, update UI
            self.update()


class PDFViewWidget(QScrollArea):
    """
    Widget for displaying PDF documents with visual rendering.

    This provides a Preview-like experience with:
    - Visual rendering of PDF pages
    - Zoom controls
    - Page navigation
    - Text selection
    """

    text_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the scroll area
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the container widget
        self.container = QWidget()
        self.setWidget(self.container)

        # Set up layout
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # PDF document and current state
        self.document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_factor = 1.2  # Reasonable default zoom

        # Create the page widget
        self.page_widget = PDFPageWidget()
        self.page_widget.text_selected.connect(self.on_text_selected)
        self.layout.addWidget(self.page_widget, 1,
                              Qt.AlignmentFlag.AlignCenter)

        # Add navigation controls
        self.create_navigation_controls()

        print(">>> PDFViewWidget fully initialized")

    def create_navigation_controls(self):
        """Create navigation controls for the PDF viewer."""
        controls_layout = QHBoxLayout()

        # Previous page button
        self.prev_button = QPushButton("◀ Previous")
        self.prev_button.clicked.connect(self.previous_page)
        controls_layout.addWidget(self.prev_button)

        # Page indicator
        self.page_label = QLabel("Page 0 of 0")
        controls_layout.addWidget(self.page_label)

        # Next page button
        self.next_button = QPushButton("Next ▶")
        self.next_button.clicked.connect(self.next_page)
        controls_layout.addWidget(self.next_button)

        # Zoom controls
        controls_layout.addSpacing(20)

        # Create a separate direct function for zoom out to avoid lambda issues
        def do_zoom_out():
            print(">>> ZOOM OUT BUTTON CLICKED!")
            self.zoom_out()

        # Create a separate direct function for zoom in to avoid lambda issues
        def do_zoom_in():
            print(">>> ZOOM IN BUTTON CLICKED!")
            self.zoom_in()

        # Zoom out button - now with direct function connection
        self.zoom_out_button = QPushButton("− Zoom Out")
        self.zoom_out_button.setToolTip("Decrease zoom level")
        self.zoom_out_button.clicked.connect(do_zoom_out)
        controls_layout.addWidget(self.zoom_out_button)

        # Add zoom level indicator
        self.zoom_label = QLabel(f"Zoom: {int(self.zoom_factor * 100)}%")
        controls_layout.addWidget(self.zoom_label)

        # Zoom in button - now with direct function connection
        self.zoom_in_button = QPushButton("+ Zoom In")
        self.zoom_in_button.setToolTip("Increase zoom level")
        self.zoom_in_button.clicked.connect(do_zoom_in)
        controls_layout.addWidget(self.zoom_in_button)

        print(">>> Navigation controls created with direct function connections")

        self.layout.addLayout(controls_layout)

    def load_document(self, file_path):
        """
        Load a PDF document and display it.

        Args:
            file_path (str): Path to the PDF file

        Returns:
            bool: Whether the document was successfully loaded
        """
        if not PYMUPDF_AVAILABLE:
            print(">>> PyMuPDF not available, cannot load document visually")
            QMessageBox.warning(
                self,
                "PDF Rendering Not Available",
                "PyMuPDF is not installed. Please install it for visual PDF rendering:\n\npip install pymupdf"
            )
            return False

        try:
            print(f">>> Loading PDF document: {file_path}")
            # Open the PDF document
            self.document = fitz.open(file_path)
            self.total_pages = len(self.document)
            self.current_page = 0

            print(f">>> PDF loaded successfully with {self.total_pages} pages")

            # Update the display
            self.update_page_display()
            return True

        except Exception as e:
            print(f">>> Error loading PDF document: {e}")
            QMessageBox.critical(
                self,
                "Error Loading PDF",
                f"Could not load the PDF document:\n\n{str(e)}"
            )
            return False

    def update_page_display(self):
        """Update the page display with current settings."""
        if not self.document:
            print(">>> No document loaded, cannot update display")
            return

        print(
            f">>> Updating page display: page {self.current_page + 1}/{self.total_pages}, zoom {self.zoom_factor:.2f}")

        # Update page widget
        self.page_widget.load_page(
            self.document, self.current_page, self.zoom_factor)

        # Update navigation controls
        self.page_label.setText(
            f"Page {self.current_page + 1} of {self.total_pages}")
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

        # Update zoom label
        self.zoom_label.setText(f"Zoom: {int(self.zoom_factor * 100)}%")

    def next_page(self):
        """Go to the next page."""
        if self.document and self.current_page < self.total_pages - 1:
            print(f">>> Moving to next page: {self.current_page + 2}")
            self.current_page += 1
            self.update_page_display()

    def previous_page(self):
        """Go to the previous page."""
        if self.document and self.current_page > 0:
            print(f">>> Moving to previous page: {self.current_page}")
            self.current_page -= 1
            self.update_page_display()

    def go_to_page(self, page_number):
        """Go to a specific page."""
        if self.document and 0 <= page_number < self.total_pages:
            print(f">>> Going to page: {page_number + 1}")
            self.current_page = page_number
            self.update_page_display()

    def zoom_in(self):
        """Increase the zoom factor."""
        print(
            f">>> ZOOM IN FUNCTION: changing zoom from {self.zoom_factor:.2f} to {self.zoom_factor * 1.2:.2f}")
        self.zoom_factor *= 1.2
        self.update_page_display()

        # Temporary visual feedback that zoom happened
        old_text = self.zoom_label.text()
        self.zoom_label.setText(f"✓ {old_text}")

        # Schedule a timer to reset the label
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.zoom_label.setText(old_text))

    def zoom_out(self):
        """Decrease the zoom factor."""
        print(
            f">>> ZOOM OUT FUNCTION: changing zoom from {self.zoom_factor:.2f} to {self.zoom_factor / 1.2:.2f}")
        self.zoom_factor /= 1.2
        self.update_page_display()

        # Temporary visual feedback that zoom happened
        old_text = self.zoom_label.text()
        self.zoom_label.setText(f"✓ {old_text}")

        # Schedule a timer to reset the label
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.zoom_label.setText(old_text))

    def on_text_selected(self, text):
        """Handle text selection from the page widget."""
        if text:
            print(f">>> Text selected in PDFViewWidget: {text[:50]}...")

            # Emit the signal to the parent
            self.text_selected.emit(text)

            # Show visual feedback that text was selected
            QMessageBox.information(
                self,
                "Text Selected",
                f"Selected text: {text[:100]}{'...' if len(text) > 100 else ''}"
            )

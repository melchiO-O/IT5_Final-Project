# Melchizideck S. Osorno
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QStackedWidget,
    QListWidgetItem,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MHIE-ni Mart (POINT OF SALE)")

        # Central container
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(container)

        # Left sidebar with image
        left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(left_sidebar)

        # Right side (navigation + content)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Top navigation bar
        self.sidebar = QListWidget()
        self.sidebar.setFlow(QListWidget.Flow.LeftToRight)
        self.sidebar.setWrapping(False)
        self.sidebar.setFixedHeight(60)
        self.sidebar.setSpacing(10)
        right_layout.addWidget(self.sidebar)

        # Main content area (stack of pages)
        self.stack = QStackedWidget()
        right_layout.addWidget(self.stack)

        main_layout.addWidget(right_container, 1)

        # Map feature names to widgets
        self.features = {}

        # Handle sidebar selection
        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

    def create_left_sidebar(self) -> QFrame:
        """Create left sidebar with full-size image/logo"""
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #800080;
                border-right: 3px solid #B57EDC;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins( 0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Logo/Image section ---
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(True)  # allow scaling to fit available space
        layout.addWidget(image_label)

        # 🖼️ Path to your image file
        image_path = r"C:\Users\User\OneDrive\Desktop\mhie.png"

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale image to fit nicely
                scaled_pixmap = pixmap.scaled(
                    sidebar.width(),
                    sidebar.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
            else:
                image_label.setText("🏪")
                image_label.setStyleSheet("font-size: 80px; color: white;")
        else:
            # Fallback placeholder if image not found
            image_label.setText("🏪")
            image_label.setStyleSheet("""
                QLabel {
                    font-size: 100px;
                    color: white;
                    background-color: rgba(255, 255, 255, 0.05);
                }
            """)

        return sidebar

    def add_feature(self, name: str, factory):
        # Create widget for feature
        widget = factory()
        self.features[name] = widget

        # Add to navigation bar
        item = QListWidgetItem(name)
        self.sidebar.addItem(item)

        # Add to stacked widget
        self.stack.addWidget(widget)
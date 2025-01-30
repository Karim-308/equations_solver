from PySide2.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox,
    QGroupBox, QSplitter
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QPixmap
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from ..models.equation import Equation  
from ..services.solver_service import SolverService


class EquationSolverView(QMainWindow):
    """GUI for solving and plotting two equations."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the GUI layout and elements."""
        # Disable maximize button while keeping minimize and close buttons
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        
        self.setWindowTitle("Functions Solver")
        self.setMinimumSize(1000, 600)
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #EDE4C7;")

        # Root widget & layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        root_layout = QVBoxLayout(main_widget)
        root_layout.setContentsMargins(5, 5, 5, 5)
        root_layout.setSpacing(5)

        # HEADER: Logo (left), Title (center)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.abspath("src/assets/Master Micro.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(180, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("Master Micro Logo Missing")
            logo_label.setStyleSheet("background-color: white; border: 1px solid #000;")

        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Title
        title_label = QLabel("Functions Solver")
        title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)

        header_layout.addStretch()
        header_layout.addWidget(title_label, alignment=Qt.AlignTop)
        header_layout.addStretch()

        root_layout.addLayout(header_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._create_input_group())
        splitter.addWidget(self._create_plot_section())
        splitter.setSizes([300, 700])

        root_layout.addWidget(splitter)

    def _create_input_group(self) -> QGroupBox:
        """Create a group box containing input fields and a solve button."""
        group_box = QGroupBox("Equation Inputs")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                margin-top: 5px;
                padding: 10px;
                padding-top: 40px;
                border: 1px solid #A0A0A0;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(group_box)
        layout.setSpacing(8)

        # Styling
        label_style = "font-weight: normal; font-size: 14px;"
        input_style = """
            QLineEdit {
                padding: 6px;
                background-color: #F5F5F5;
                border: 1px solid #A0A0A0;
                border-radius: 4px;
                font-size: 14px;
            }
        """

        # Function 1
        eq1_label = QLabel("Function 1 Equation:")
        eq1_label.setStyleSheet(label_style)
        self.eq1_input = QLineEdit()
        self.eq1_input.setStyleSheet(input_style)
        self.eq1_input.setPlaceholderText("e.g. 5*x^3 + 2*x")

        # Function 2
        eq2_label = QLabel("Function 2 Equation:")
        eq2_label.setStyleSheet(label_style)
        self.eq2_input = QLineEdit()
        self.eq2_input.setStyleSheet(input_style)
        self.eq2_input.setPlaceholderText("e.g. log10(x) + 3")

        # Solve button
        solve_button = QPushButton("Solve and Plot")
        solve_button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #536279;
                color: white;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #405060;
            }
        """)
        solve_button.clicked.connect(self.solve_and_plot)

        layout.addWidget(eq1_label)
        layout.addWidget(self.eq1_input)
        layout.addWidget(eq2_label)
        layout.addWidget(self.eq2_input)
        layout.addSpacing(5)
        layout.addWidget(solve_button)
        layout.addStretch()

        return group_box

    def _create_plot_section(self) -> QWidget:
        """Create a widget containing the Matplotlib plot + toolbar."""
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        plot_layout.setContentsMargins(5, 5, 5, 5)
        plot_layout.setSpacing(5)

        # Figure & Canvas
        self.figure = plt.Figure(figsize=(6, 5))
        self.canvas = FigureCanvasQTAgg(self.figure)

        # Toolbar wrapped in horizontal layout for centering
        toolbar_layout = QHBoxLayout()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setStyleSheet("background-color: #DED3B5; border-radius: 4px;")
        
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.toolbar)
        toolbar_layout.addStretch()

        plot_layout.addWidget(self.canvas)
        plot_layout.addLayout(toolbar_layout)

        return plot_widget

    def solve_and_plot(self):
        """Solve and plot two equations with intersection points."""
        try:
            # Get user input
            raw_eq1 = self.eq1_input.text().strip()
            raw_eq2 = self.eq2_input.text().strip()

            # Validate & Parse Equations
            eq1 = Equation(raw_eq1)
            eq2 = Equation(raw_eq2)

            if eq1.error_message or eq2.error_message:
                QMessageBox.warning(
                    self, "Invalid Input",
                    f"Equation 1 Error: {eq1.error_message}\nEquation 2 Error: {eq2.error_message}"
                )
                return

            # Solve and get plot data
            solver = SolverService(eq1, eq2)
            intersections = solver.solve()
            x_vals, y1_vals, y2_vals = solver.get_plot_data()

            # Clear previous plot
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            # Plot the user-defined functions
            ax.plot(x_vals, y1_vals, label=f'Function 1: {raw_eq1}', color='blue')
            ax.plot(x_vals, y2_vals, label=f'Function 2: {raw_eq2}', color='green')

            # Plot intersection points
            if intersections:
                x_int, y_int = zip(*intersections)
                ax.scatter(x_int, y_int, color='red', s=100, zorder=5, label='Intersections')
                for x_i, y_i in intersections:
                    ax.annotate(f'({x_i:.2f}, {y_i:.2f})', (x_i, y_i),
                                xytext=(10, 10), textcoords='offset points',
                                fontsize=12, fontweight='bold', color='red')

            ax.grid(True)
            ax.legend()
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Function Intersection Points")

            # Update canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

import sys
from PySide2.QtWidgets import QApplication
from src.views.equation_view import EquationSolverView

def main():
    app = QApplication(sys.argv)
    window = EquationSolverView()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
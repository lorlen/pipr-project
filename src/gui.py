from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

back_color = QColor('#6bb9a9')
fore_color = QColor('#ffd61d')


class GridCell(QWidget):
    def __init__(self, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = pos.x
        self.y = pos.y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = event.rect()

        painter.fillRect(rect, fore_color)
        center = QPoint(rect.x() + rect.width() // 2, rect.y() + rect.height() // 2)
        radius = min(rect.width(), rect.height()) - 5
        painter.drawEllipse(center, radius, radius)


class GameWindow(QWidget):
    def __init__(self, board, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.board = board

        self.layout = QGridLayout()
        self.layout.setSpacing(5)



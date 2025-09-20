from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QGraphicsItemGroup
import sys
import os
import math
import time

# 打包资源用
def resource_path(relative_path):
    """打包后正确找到资源路径"""
    if hasattr(sys, "_MEIPASS"):  # PyInstaller 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class PetView(QGraphicsView):
    def __init__(self):
        self.direction = 1  # 1 表示向右，-1 表示向左
        self.move_speed = 0.7
        self.action_speed=10


        super().__init__()

        self.setWindowIcon(QIcon("assets/head.png"))

        # 创建场景
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint  # 置顶
        )
        self.setFixedSize(160, 150)
        self.scene.setSceneRect(0, 0, 160, 150)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)

        # 关闭滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")

        # 加载部件
        left_leg = QPixmap(resource_path("assets/left_leg.png")).scaled(
            34, 41, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.left_leg = self.scene.addPixmap(left_leg)
        self.left_leg.setZValue(0)
        self.left_leg_direction=1


        right_leg = QPixmap(resource_path("assets/right_leg.png")).scaled(
            23, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.right_leg = self.scene.addPixmap(right_leg)
        self.right_leg.setZValue(0)

        skirt = QPixmap(resource_path("assets/skirt.png")).scaled(
            52, 54, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.skirt = self.scene.addPixmap(skirt)
        self.skirt.setZValue(1)

        body = QPixmap(resource_path("assets/body.png")).scaled(
            60, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.body = self.scene.addPixmap(body)
        self.body.setZValue(2)

        left_arm = QPixmap(resource_path("assets/left_arm.png")).scaled(
            27, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.left_arm = self.scene.addPixmap(left_arm)
        self.left_arm.setZValue(3)

        right_arm = QPixmap(resource_path("assets/right_arm.png")).scaled(
            36, 58, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.right_arm = self.scene.addPixmap(right_arm)
        self.right_arm.setZValue(1)
        self.right_arm_direction=1

        head1 = QPixmap(resource_path("assets/head1.png")).scaled(
            115, 76, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.head1 = self.scene.addPixmap(head1)
        self.head1.setZValue(6)


        tongue = QPixmap(resource_path("assets/tongue.png")).scaled(
            18, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.tongue = self.scene.addPixmap(tongue)
        self.tongue.setZValue(5)
        # 初始隐藏
        self.tongue.setVisible(False)
        # 设置旋转中心为上边缘终点，默认为左上角
        rect = self.tongue.boundingRect()
        self.tongue.setTransformOriginPoint(rect.center().x(), rect.top())


        # 位置调整
        self.left_leg.setPos(10, 105)
        self.right_leg.setPos(45, 115)
        self.skirt.setPos(13, 70)
        self.body.setPos(45, 73)
        self.left_arm.setPos(65, 97)
        self.right_arm.setPos(85, 90)
        self.head1.setPos(40, 25)
        self.tongue.setPos(100,80)

        self.setRenderHint(QPainter.Antialiasing)  # 平滑渲染

        # 把noen的身体各部分放到一个组里，实现转身用
        self.noen_group = QGraphicsItemGroup()
        for part in [self.left_leg, self.right_leg, self.skirt,
                     self.body, self.left_arm, self.right_arm, self.head1,
                     self.tongue]:
            self.noen_group.addToGroup(part)
        self.scene.addItem(self.noen_group)

        # 初始化桌宠位置
        screen = QApplication.primaryScreen().availableGeometry()
        self.x = 50
        self.y = screen.bottom() - self.height() + 10
        self.move(self.x, self.y + 10)

        # 计时器，控制移动
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_noen)
        self.timer.start(5)

    def move_noen(self):
        t=time.time()
        screen = QApplication.primaryScreen().availableGeometry()
        # 爬
        self.x += self.move_speed * self.direction  # 根据方向移动

        # 转向
        if self.x + self.width() >= screen.right():
            self.direction = -1  # 改变方向
            self.flip_noen()  # 翻转图片
            self.x = screen.right() - self.width()
        elif self.x <= screen.left():
            self.direction = 1
            self.flip_noen()
            self.x = screen.left()

        self.move(self.x, self.y)

        self.head1.setPos(40, 25+math.sin(t*self.action_speed))

        self.body.setPos(45, 73+math.sin(t*self.action_speed))

        self.skirt.setPos(13+math.sin(t*self.action_speed), 70+math.sin(t*self.action_speed))

        self.left_leg.setRotation(15 * math.sin(t * self.action_speed+ math.pi))

        self.right_leg.setRotation(15 * math.sin(t * self.action_speed ))

        self.left_arm.setRotation(12 * math.sin(t * self.action_speed))

        self.right_arm.setRotation(12 * math.sin(t * self.action_speed+math.pi))

        self.tongue.setPos(100,80)
        self.tongue.setRotation(7.5 * math.sin(t * self.action_speed))


    def flip_noen(self):
        center_x = self.noen_group.boundingRect().center().x()
        transform = QtGui.QTransform()
        transform.translate(center_x, 0)
        if self.direction == -1:  # 向左时翻转
            transform.scale(-1, 1)
        else:
            transform.scale(1, 1)
        transform.translate(-center_x, 0)
        self.noen_group.setTransform(transform)

    # 不知道为什么可以用滚轮小幅度滚动，所以干脆ban了滚轮
    def wheelEvent(self, event):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.noen_fast_run()

    def noen_fast_run(self):
        self.move_speed = 1.4
        self.action_speed = 20
        # 显示舌头
        self.tongue.setVisible(True)
        QTimer.singleShot(3000,self.re_noen_speed)

    def re_noen_speed(self):
        self.move_speed = 0.7
        self.action_speed = 10
        # 藏舌头
        self.tongue.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets/head.ico")))
    view = PetView()
    view.show()
    sys.exit(app.exec())

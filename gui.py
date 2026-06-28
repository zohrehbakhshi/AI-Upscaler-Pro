from PySide6.QtWidgets import *

from PySide6.QtCore import *

from PySide6.QtGui import *

import os

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("AI Upscaler Pro")

        self.resize(900,650)

        self.input_folder=""

        self.output_folder=""

        self.build_ui()

    def build_ui(self):

        widget=QWidget()

        self.setCentralWidget(widget)

        layout=QVBoxLayout()

        widget.setLayout(layout)

        title=QLabel("AI Upscaler Pro")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

        font-size:28px;

        font-weight:bold;

        color:white;

        """)

        layout.addWidget(title)

        form=QFormLayout()

        self.inputEdit=QLineEdit()

        self.outputEdit=QLineEdit()

        btnInput=QPushButton("Browse")

        btnOutput=QPushButton("Browse")

        btnInput.clicked.connect(self.select_input)

        btnOutput.clicked.connect(self.select_output)

        h1=QHBoxLayout()

        h1.addWidget(self.inputEdit)

        h1.addWidget(btnInput)

        h2=QHBoxLayout()

        h2.addWidget(self.outputEdit)

        h2.addWidget(btnOutput)

        form.addRow("Input Folder",h1)

        form.addRow("Output Folder",h2)

        layout.addLayout(form)

        self.modelBox=QComboBox()

        self.modelBox.addItems([

            "RealESRGAN x4+",

            "UltraSharp",

            "SwinIR"

        ])

        layout.addWidget(self.modelBox)

        self.fast=QRadioButton("Fast")

        self.balance=QRadioButton("Balanced")

        self.ultra=QRadioButton("Ultra Quality")

        self.ultra.setChecked(True)

        quality=QGroupBox("Quality")

        qlayout=QHBoxLayout()

        qlayout.addWidget(self.fast)

        qlayout.addWidget(self.balance)

        qlayout.addWidget(self.ultra)

        quality.setLayout(qlayout)

        layout.addWidget(quality)

        self.cb8k=QCheckBox("Upscale to 8K")

        self.cb8k.setChecked(True)

        self.cb300=QCheckBox("300 DPI")

        self.cb300.setChecked(True)

        self.cbAlpha=QCheckBox("Keep Transparency")

        self.cbAlpha.setChecked(True)

        layout.addWidget(self.cb8k)

        layout.addWidget(self.cb300)

        layout.addWidget(self.cbAlpha)

        self.progress=QProgressBar()

        layout.addWidget(self.progress)

        self.log=QTextEdit()

        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        buttons=QHBoxLayout()

        self.startBtn=QPushButton("START")

        self.stopBtn=QPushButton("STOP")

        buttons.addWidget(self.startBtn)

        buttons.addWidget(self.stopBtn)

        layout.addLayout(buttons)

        self.setStyleSheet("""

        QWidget{

        background:#1e1e1e;

        color:white;

        }

        QPushButton{

        background:#00b894;

        color:white;

        font-size:15px;

        border-radius:6px;

        padding:8px;

        }

        QPushButton:hover{

        background:#00d8a8;

        }

        QLineEdit{

        background:#333;

        border:1px solid #666;

        padding:6px;

        }

        QTextEdit{

        background:#2d2d2d;

        }

        """)

    def select_input(self):

        folder=QFileDialog.getExistingDirectory(self,"Input Folder")

        if folder:

            self.input_folder=folder

            self.inputEdit.setText(folder)

    def select_output(self):

        folder=QFileDialog.getExistingDirectory(self,"Output Folder")

        if folder:

            self.output_folder=folder

            self.outputEdit.setText(folder)
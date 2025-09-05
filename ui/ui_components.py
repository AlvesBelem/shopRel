from PyQt5.QtWidgets import (
    QFormLayout, QDateEdit, QComboBox, QMessageBox,
    QTreeWidget, QHeaderView, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import QDate, Qt


def build_filters_section(db):
    date_start = QDateEdit(QDate.currentDate())
    date_end = QDateEdit(QDate.currentDate())
    date_start.setCalendarPopup(True)
    date_end.setCalendarPopup(True)
    date_start.setFixedWidth(150)
    date_end.setFixedWidth(150)

    status_combo = QComboBox()
    status_combo.setFixedWidth(150)
    status_combo.addItems(["Todos", "Finalizado", "Em andamento"])

    entregador_combo = QComboBox()
    entregador_combo.setFixedWidth(150)
    entregador_combo.addItem("Todos", None)

    try:
        df = db.query("SELECT identregador, nmentregador FROM wshop.delivery_entregador WHERE inativo = false OR inativo IS NULL")
        for _, row in df.iterrows():
            entregador_combo.addItem(row['nmentregador'], row['identregador'])
    except Exception as e:
        QMessageBox.critical(None, "Erro ao carregar entregadores", str(e))

    layout = QFormLayout()
    layout.addRow("Data Início:", date_start)
    layout.addRow("Data Fim:", date_end)
    layout.addRow("Status:", status_combo)
    layout.addRow("Entregador:", entregador_combo)

    return date_start, date_end, status_combo, entregador_combo, layout


def build_button_section(gerar_func, excel_func, pdf_func, email_func):
    gerar_btn = QPushButton("Gerar Relatório")
    gerar_btn.clicked.connect(gerar_func)

    excel_btn = QPushButton("Exportar Excel")
    excel_btn.clicked.connect(excel_func)

    pdf_btn = QPushButton("Exportar PDF")
    pdf_btn.clicked.connect(pdf_func)

    email_btn = QPushButton("Enviar por Email")
    email_btn.clicked.connect(email_func)

    layout = QHBoxLayout()
    layout.addWidget(gerar_btn)
    layout.addStretch()
    layout.addWidget(excel_btn)
    layout.addWidget(pdf_btn)
    layout.addWidget(email_btn)

    return layout


def build_tree_widget():
    tree = QTreeWidget()
    tree.setHeaderLabels([
        "Carregamento", "Entregador", "Data Saída", "Data Retorno",
        "Status", "Clientes", "Documentos"
    ])
    tree.setColumnCount(7)

    header = tree.header()
    header.setDefaultAlignment(Qt.AlignCenter) # type: ignore
    header.setSectionResizeMode(QHeaderView.Fixed) # type: ignore

    tree.setAlternatingRowColors(True)
    tree.setStyleSheet("""
        QTreeWidget::item:alternate {
                background-color: #d0d0d0;
                color: black;    
            }
            QTreeWidget::item {
                background-color: white;
            }
            QTreeWidget::item:selected {
                background-color: #B9D9EB;  /* fundo azul escuro ou cor que preferir */
                color: black;               /* texto preto para ficar visível */
            }
            QTreeWidget::item:selected:active {
                background-color: #B9D9EB;
                color: black;
            }
            QTreeWidget::item:selected:!active {
                background-color: #a0c4ff;
                color: black;
            }
    """)

    widths = [100, 200, 150, 150, 120, 250, 250]
    for i, width in enumerate(widths):
        tree.setColumnWidth(i, width)

    return tree


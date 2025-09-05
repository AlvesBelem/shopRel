from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtGui import QFont
from ui.ui_components import (
    build_filters_section,
    build_button_section,
    build_tree_widget
)
from core.report_logic import generate_report_data, preencher_tree_widget
from core.exporters import exportar_excel, exportar_pdf
from core.email_sender import enviar_email
import pandas as pd


class MainApp(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("ShopRel - CONECTADO")
        self.setMinimumSize(900, 600)

        # Seções da UI
        self.date_start, self.date_end, self.status_combo, self.entregador_combo, filtros_layout = build_filters_section(
            self.db)
        self.tree = build_tree_widget()
        self.total_label = QLabel("Total de carregamentos: 0")
        
        # Aqui você configura a fonte da label
            
        fonte = QFont()
        fonte.setPointSize(12)   # aumenta o tamanho
        fonte.setBold(True)      # deixa em negrito
        self.total_label.setFont(fonte)

        botoes_layout = build_button_section(
            self.carregar_dados,
            lambda: self.exportar_excel_ui(),
            lambda: self.exportar_pdf_ui(),
            lambda: self.enviar_email_ui()
        )

        # Layout principal
        layout = QVBoxLayout()
        layout.addLayout(filtros_layout)
        layout.addWidget(self.total_label)
        layout.addWidget(self.tree)
        layout.addLayout(botoes_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Janela principal
        self.setGeometry(100, 100, 1000, 600)
        self.raise_()
        self.activateWindow()

    def carregar_dados(self):
        try:
            filtros = {
                "data_inicio": self.date_start.date().toString("yyyy-MM-dd"),
                "data_fim": self.date_end.date().toString("yyyy-MM-dd"),
                "status": self.status_combo.currentText(),
                "entregador_id": self.entregador_combo.currentData(),
            }

            df = generate_report_data(filtros, self.db)
            self.df = df
            preencher_tree_widget(self, df)

            total = df["cdcarregamento"].nunique()
            self.total_label.setText(f"Total de carregamentos: {total}")
            

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados:\n{e}")

    def exportar_excel_ui(self):
        if not hasattr(self, 'df') or self.df.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado para exportar.")
            return

        caminho, _ = QFileDialog.getSaveFileName(
            self, "Salvar Excel", "relatorio.xlsx", "Excel Files (*.xlsx)")
        if caminho:
            try:
                exportar_excel(self, caminho)
                QMessageBox.information(
                    self, "Sucesso", "Arquivo Excel exportado com sucesso!")
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao exportar Excel:\n{e}")

    def exportar_pdf_ui(self):
        if not hasattr(self, 'df') or self.df.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado para exportar.")
            return

        caminho, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", "relatorio.pdf", "PDF Files (*.pdf)")
        if caminho:
            try:
                exportar_pdf(self, caminho)
                QMessageBox.information(
                    self, "Sucesso", "Arquivo PDF exportado com sucesso!")
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao exportar PDF:\n{e}")

    def enviar_email_ui(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo para Enviar", "", "Todos os Arquivos (*)")
        if not caminho:
            return

        try:
            enviar_email(
                destinatario="destinatario@exemplo.com",
                assunto="Relatório Solicitado",
                corpo_texto="Segue em anexo o relatório solicitado.",
                caminho_anexo=caminho
            )
            QMessageBox.information(
                self, "Sucesso", "E-mail enviado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar e-mail:\n{e}")

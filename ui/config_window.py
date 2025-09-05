from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
import json
import os
import psycopg2


class ConfigWindow(QWidget):
    def __init__(self, on_success=None):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("Configuração do Sistema")
        self.setMinimumWidth(400)

        # --- Campos de banco de dados ---
        self.host_input = QLineEdit()
        self.dbname_input = QLineEdit()
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # --- Campos de e-mail ---
        self.smtp_input = QLineEdit()
        self.port_input = QLineEdit()
        self.email_input = QLineEdit()
        self.email_password_input = QLineEdit()
        self.email_password_input.setEchoMode(QLineEdit.Password)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🗄️ Banco de Dados"))
        layout.addWidget(QLabel("Host:"))
        layout.addWidget(self.host_input)
        layout.addWidget(QLabel("Nome do Banco:"))
        layout.addWidget(self.dbname_input)
        layout.addWidget(QLabel("Usuário:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(self.password_input)

        layout.addWidget(QLabel("📧 Configuração de E-mail (SMTP)"))
        layout.addWidget(QLabel("SMTP Host:"))
        layout.addWidget(self.smtp_input)
        layout.addWidget(QLabel("Porta:"))
        layout.addWidget(self.port_input)
        layout.addWidget(QLabel("E-mail Remetente:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Senha de App:"))
        layout.addWidget(self.email_password_input)

        # Botões
        self.test_button = QPushButton("Testar Conexão")
        self.save_button = QPushButton("Salvar Configuração")

        self.test_button.clicked.connect(self.testar_conexao)
        self.save_button.clicked.connect(self.salvar_configuracoes)

        layout.addWidget(self.test_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def testar_conexao(self):
        try:
            conn = psycopg2.connect(
                host=self.host_input.text(),
                database=self.dbname_input.text(),
                user=self.user_input.text(),
                password=self.password_input.text()
            )
            conn.close()
            QMessageBox.information(self, "Sucesso", "Conexão com o banco de dados bem-sucedida!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar:\n{e}")

    def salvar_configuracoes(self):
        try:
            os.makedirs("config", exist_ok=True)

            db_config = {
                "host": self.host_input.text(),
                "database": self.dbname_input.text(),
                "user": self.user_input.text(),
                "password": self.password_input.text()
            }
            with open("config/db_config.json", "w", encoding="utf-8") as f:
                json.dump(db_config, f, indent=2)

            email_config = {
                "host": self.smtp_input.text(),
                "port": int(self.port_input.text()),
                "username": self.email_input.text(),
                "password": self.email_password_input.text()
            }
            with open("config/email_config.json", "w", encoding="utf-8") as f:
                json.dump(email_config, f, indent=2)

            QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")

            if self.on_success:
                self.close()
                self.on_success()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configurações:\n{e}")

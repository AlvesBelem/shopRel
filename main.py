import sys
import os
import json
import traceback
from PyQt5.QtWidgets import QApplication, QLabel
from ui.main_window import MainApp
from ui.config_window import ConfigWindow
from core.db import DBConnection

# ✅ Variáveis globais para manter janelas vivas
main_window = None
config_window = None

def iniciar_app():
    print("🔵 Iniciando aplicação...")
    app = QApplication(sys.argv)

    def abrir_main_window():
        print("🔄 Tentando abrir janela principal...")
        try:
            db = DBConnection()
            db.connect()
            print("✅ Conexão com banco de dados bem-sucedida.")

            global main_window
            main_window = MainApp(db)
            main_window.show()
            print("🟢 Janela principal exibida com sucesso.")
        except Exception as e:
            print("❌ Erro ao iniciar o sistema:", e)
            traceback.print_exc()

            # ✅ Armazenar instância no escopo global
            global config_window
            config_window = ConfigWindow(on_success=abrir_main_window)
            config_window.show()
            print("⚠️ Exibindo janela de configuração do banco.")

    try:
        if not os.path.exists("config/db_config.json"):
            print("⚠️ Arquivo de configuração não encontrado.")
            global config_window
            config_window = ConfigWindow(on_success=abrir_main_window)
            config_window.show()
        else:
            print("📁 Arquivo de configuração encontrado.")
            abrir_main_window()
    except Exception as e:
        print("❌ Erro ao carregar aplicação:", e)
        traceback.print_exc()
        # Exibe uma janela básica com erro
        error_label = QLabel("Erro ao carregar aplicação. Verifique o terminal.")
        error_label.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    iniciar_app()

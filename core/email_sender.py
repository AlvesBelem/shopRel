import smtplib
from email.message import EmailMessage
import os
import json

def carregar_config_email(caminho_arquivo="config/email_config.json"):
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError("Arquivo de configuração de e-mail não encontrado.")

    with open(caminho_arquivo, "r") as f:
        config = json.load(f)

    campos_obrigatorios = ["host", "port", "username", "password"]
    for campo in campos_obrigatorios:
        if campo not in config or not config[campo]:
            raise ValueError(f"Campo obrigatório '{campo}' ausente na configuração.")

    return config

def enviar_email(destinatario, assunto, corpo_texto, caminho_anexo=None):
    config = carregar_config_email()

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = config["username"]
    msg["To"] = destinatario
    msg.set_content(corpo_texto)

    if caminho_anexo:
        if not os.path.exists(caminho_anexo):
            raise FileNotFoundError("Arquivo de anexo não encontrado.")
        with open(caminho_anexo, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(caminho_anexo)
            )

    try:
        with smtplib.SMTP(config["host"], config["port"]) as smtp:
            smtp.starttls()
            smtp.login(config["username"], config["password"])
            smtp.send_message(msg)
        print("✅ E-mail enviado com sucesso.")
    except Exception as e:
        print("❌ Erro ao enviar e-mail:", e)
        raise e

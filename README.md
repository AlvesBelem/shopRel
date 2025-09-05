# ShopRel

Aplicação desktop desenvolvida com **PyQt5** para geração e gerenciamento de relatórios de carregamentos.

---

##  Descrição

O **ShopRel** permite:

- Filtrar registros por **data inicial/final**, **status** e **entregador**
- Visualizar resultados em uma **árvore hierárquica**
- Exportar relatórios para **Excel (.xlsx)** e **PDF (.pdf)**
- Enviar relatórios por **e-mail**
- Exibir o **total de carregamentos** de forma clara na interface

---

##  Estrutura do projeto

.
├── core/
│ ├── report_logic.py — Geração e processamento dos dados do relatório
│ ├── exporters.py — Exportação para Excel e PDF
│ └── email_sender.py — Envio de relatórios por e-mail
│
├── ui/
│ ├── ui_components.py — Componentes reutilizáveis da interface (filtros, botões, árvore)
│ └── config_window.py — Janela de configuração (ex: configuração de banco de dados)
│
├── main.py — Ponto de entrada da aplicação, controla fluxo e janelas
└── requirements.txt — Dependências do projeto


---

##  Tecnologias e dependências

- **Python** 3.8+
- **PyQt5** – Interface gráfica
- **pandas** – Manipulação de dados
- **openpyxl** – Exportação para Excel
- **reportlab** – Geração de arquivos PDF
- (Possivelmente) **smtplib** ou similar – Envio de e-mail

Você pode ajustar essas dependências conforme estiver usando no seu projeto.

---

##  Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/AlvesBelem/shopRel.git
   cd shopRel

## (Recomendado) Crie um ambiente virtual:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

## Instale as dependências:

pip install -r requirements.txt

## Execute a aplicação:

python main.py

## Funcionalidades-chave

Filtros por datas, status e entregador para refinar relatórios

Visualização em árvore com total de carregamentos destacando a análise

Exportação de resultados em Excel e PDF

Envio direto de relatórios por e-mail

Mensagens de erro e sucesso integradas à interface (via QMessageBox)

## Contribuições

Contribuições são bem-vindas! Se quiser colaborar:

Abra um Issue com uma descrição detalhada

Ou envie um Pull Request com melhorias ou correções

## Contato

Desenvolvido por Alves Belem
📩 E-mail: marcelo.alves28@gmail.com

🔗 GitHub: github.com/AlvesBelem


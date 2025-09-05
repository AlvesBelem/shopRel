import traceback
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd


def generate_report_data(filtros, db):
    data_inicio = filtros["data_inicio"]
    data_fim = filtros["data_fim"]
    status = filtros["status"]
    entregador_id = filtros["entregador_id"]

    sql = '''
        SELECT
            c.cdcarregamento,
            e.nmentregador,
            TO_CHAR(c.dtsaida, 'DD/MM/YYYY HH24:MI') AS data_saida,
            TO_CHAR(c.dtretorno, 'DD/MM/YYYY HH24:MI') AS data_retorno,
            CASE WHEN c.dtretorno IS NULL THEN 'Em andamento' ELSE 'Finalizado' END AS status_entrega,
            p.nmpessoa,
            string_agg(DISTINCT d2.nrdocumento, ', ') AS documentos
        FROM wshop.carregamento c
        LEFT JOIN wshop.delivery_entregador e ON c.identregador = e.identregador
        LEFT JOIN wshop.carregamentoitem ci ON c.idcarregamento = ci.idcarregamento
        LEFT JOIN wshop.pessoas p ON ci.idpessoa = p.idpessoa
        LEFT JOIN LATERAL (
            SELECT d2.nrdocumento
            FROM unnest(string_to_array(c.listadocumentos, ',')) AS doc_id
            JOIN wshop.documen d2 ON d2.iddocumento = doc_id
        ) d2 ON TRUE
        WHERE DATE(c.dtsaida) BETWEEN %s AND %s
    '''

    params = [data_inicio, data_fim]

    if status == "Finalizado":
        sql += " AND c.dtretorno IS NOT NULL"
    elif status == "Em andamento":
        sql += " AND c.dtretorno IS NULL"

    if entregador_id:
        sql += " AND c.identregador = %s"
        params.append(entregador_id)

    sql += " GROUP BY c.cdcarregamento, e.nmentregador, c.dtsaida, c.dtretorno, p.nmpessoa"
    sql += " ORDER BY c.dtsaida DESC"

    return db.query(sql, params).fillna("")


def preencher_tree_widget(main_window, df: pd.DataFrame):
    main_window.tree.clear()

    if df.empty:
        QMessageBox.information(main_window, "Relatório", "Nenhum registro encontrado com os filtros selecionados.")
        main_window.total_label.setText("Total de carregamentos: 0")
        return

    grouped = df.groupby([
        'cdcarregamento', 'nmentregador', 'data_saida', 'data_retorno', 'status_entrega', 'documentos'])

    for (cdcarregamento, entregador, data_saida, data_retorno, status_entrega, documentos), group in grouped:
        clientes = group['nmpessoa'].unique()
        clientes_texto = '' if len(clientes) > 1 else clientes[0]

        item = QTreeWidgetItem([
            cdcarregamento, entregador, data_saida, data_retorno, status_entrega, clientes_texto, documentos
        ])
        for i in range(item.columnCount()):
            item.setTextAlignment(i, Qt.AlignCenter)

        if len(clientes) > 1:
            for cliente in clientes:
                child = QTreeWidgetItem(["", "", "", "", "", cliente, ""])
                for i in range(child.columnCount()):
                    child.setTextAlignment(i, Qt.AlignCenter)
                item.addChild(child)

        main_window.tree.addTopLevelItem(item)

    main_window.total_label.setText(f"Total de carregamentos: {df['cdcarregamento'].nunique()}")

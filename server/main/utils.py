"""Скрипт для ввода данных в elasticsearch с исходного csv"""

import csv
import json

import pandas as pd
import psycopg2
from elasticsearch import Elasticsearch

INDEX = "posts"


def df2elastic_converter(df):
    """Конвертация df в формат elastic'а"""
    for record in df.to_dict(orient="records"):
        yield '{ "index" : { "_index" : "%s", "_type" : "%s" }}' % (INDEX, "record")
        yield json.dumps(record, default=int)


def elastic_insert_logic(file_name: str):
    """Добавление данных в Elastic"""
    # Читаем csv и проставляем колонки и id
    df = pd.read_csv(file_name, usecols=[0])
    df["id"] = df.index + 1
    print(df)

    # Добавляем все в новый индекс INDEX
    e = Elasticsearch("http://127.0.0.1:9200")
    if e.indices.exists(INDEX):
        e.indices.delete(index=INDEX)
    e.indices.create(index=INDEX)

    r = e.bulk(df2elastic_converter(df))
    if not r["errors"]:
        print("Успешно записал данные в elastic")
    else:
        print("Не удалось записать данные в elastic")


elastic_insert_logic("posts.csv")
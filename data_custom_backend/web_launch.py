# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： web_launch
Description :
Author : 'li'
date： 2020/10/21
-------------------------------------------------
Change Activity:
2020/10/21:
-------------------------------------------------
"""
import json

from flask import Flask, request, send_file, make_response
from flask_cors import cross_origin, CORS

from interface.data_inference import DataInterface
from interface.download_inference import DownloadInference
from interface.table_inference import TableInterface
from llib.file_utility.file_path_utility import combine_file_path

app = Flask(__name__)
CORS(app, supports_credentials=True)


@cross_origin()
@app.route("/create_table", methods=["POST"])
def create_table():
    data = str(request.data, encoding='utf8')
    return TableInterface.create_table(json.loads(data))


@cross_origin()
@app.route("/search_table_info", methods=["POST"])
def search_table_info():
    data = dict(request.form)
    if len(data) == 0:
        data = dict(request.json)
    return TableInterface.search_table(data)


@cross_origin()
@app.route("/get_table_comment", methods=["POST"])
def get_table_comment():
    data = dict(request.form)
    if len(data) == 0:
        data = dict(request.json)
    return TableInterface.get_table_comment(data)


@cross_origin()
@app.route("/alter_table_name", methods=["POST"])
def alter_table_name():
    data = str(request.data, encoding='utf8')
    return TableInterface.alter_table_name(json.loads(data))


@cross_origin()
@app.route("/alter_column_name", methods=["POST"])
def alter_column_name():
    data = str(request.data, encoding='utf8')
    return TableInterface.alter_column_name(json.loads(data))


@cross_origin()
@app.route("/get_column_info", methods=["POST"])
def get_column_info():
    data = str(request.data, encoding='utf8')
    return TableInterface.get_column_info(json.loads(data))


@cross_origin()
@app.route("/add_column_name", methods=["POST"])
def add_column_name():
    data = str(request.data, encoding='utf8')
    return TableInterface.add_column_name(json.loads(data))


@cross_origin()
@app.route("/delete_column", methods=["POST"])
def delete_column():
    data = str(request.data, encoding='utf8')
    return TableInterface.delete_column(json.loads(data))


@cross_origin()
@app.route("/add_data", methods=["POST"])
def add_data():
    data = str(request.data, encoding='utf8')
    return DataInterface.add_data(json.loads(data))


@cross_origin()
@app.route("/update_data", methods=["POST"])
def update_data():
    data = str(request.data, encoding='utf8')
    return DataInterface.update_data(json.loads(data))


@cross_origin()
@app.route("/query_data_from_db", methods=["POST"])
def query_data_from_db():
    data = dict(request.form)
    data = data['data']
    return DataInterface.query_data(json.loads(data))


@cross_origin()
@app.route("/query_data_by_unique_id", methods=["POST"])
def query_data_by_unique_id():
    data = dict(request.json)
    return DataInterface.query_data_by_unique_id(data)


@cross_origin()
@app.route("/alter_table_info", methods=["POST"])
def alter_table_info():
    data = str(request.data, encoding='utf8')
    return TableInterface.alter_table_info(json.loads(data))


@cross_origin()
@app.route("/delete_table", methods=["POST"])
def delete_table():
    data = str(request.data, encoding='utf8')
    return TableInterface.delete_table(json.loads(data))


@cross_origin()
@app.route("/delete_data_post", methods=["POST"])
def delete_data_post():
    data = str(request.data, encoding='utf8')
    return DataInterface.delete_data_post(json.loads(data))


@cross_origin()
@app.route("/gen_excel_data_post", methods=['POST'])
def gen_excel_data_post():
    is_success = DownloadInference.gen_excel(request.json)
    return is_success


@cross_origin()
@app.route("/download_file", methods=['GET'])
def file_download():
    file_name = request.args.get("fileName")
    response = make_response(send_file(combine_file_path('gen/' + file_name)))
    response.headers["Content-Disposition"] = "attachment; filename={};".format('export.' + 'xls')
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3344)

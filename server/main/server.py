import crud
from flask import Flask, jsonify, make_response, request, abort
from DBlib import DataBase as DB

DataBase = DB("lanhelen.asuscomm.com", "daniel", "Daniel123!", "python_intern")


app = Flask(__name__)



@app.route("/add_comment", methods=["POST"])
def create_comment():
    """Поиск постов по тексту"""
    print(" ========================= We come here ========================= ")
    if not request.json:
        abort(400)
    Text = request.json.get("text")
    print(" ========================= We come here again ========================= ")
    results_list = crud.search_post_by_text(DataBase=DataBase, search_text=Text)
    return jsonify(results_list)
    #return jsonify({"res": "hygt6"})


@app.route("/posts/delete", methods=["DELETE"])
def remove_post():
    """Удаление документов из БД и индекса по полю id"""
    print(" ========================= We come here ========================= ")
    if not request.json:
        abort(400)
    id = request.json.get("id")
    if not id:
        return jsonify({"result": "no id"})
    result = crud.delete_by_id(DataBase=DataBase, id=id)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(port = 3444, debug = True)
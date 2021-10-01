from DBlib import DataBase as DB
from elastic import MyElastic


my_elastic = MyElastic()


def search_post_by_text(DataBase, search_text: str):
    """Поиск по тексту документа и возврат первых 20 документов со всем полями, упорядоченные по дате создания"""
    # Поиск в elastic
    id_list = [item["id"] for item in my_elastic.search_by_text(search_text)]
    que = f"SELECT * FROM test_data WHERE id IN{id_list} GROUP BY date LIMIT 20;"
    que = que.replace("[", "(").replace("]", ")")
    #print(id_list)
    # Получение полей СУБД с id, которые отдал нам elastic
    DBColData = DataBase.ExecuteReadQuery("DESCRIBE test_data")
    result = {"documents" : []}
    #print(que)
    full_data = DataBase.ExecuteReadQuery(que)
    for data in full_data:
        line = {}
        for field, name in zip(data, DBColData):
            line.update({name[0] : field})
        result["documents"].append(line)
    return result


def delete_by_id(DataBase, id: int) -> bool:
    """Удаление поста по переданному id"""
    # Удаление из elastic
    delete_item = my_elastic.search_by_id(id)
    # Если в elastic есть такой id
    if delete_item is not None:
        # Удаляем по внутреннему id в elastic
        elastic_result = my_elastic.delete_by_id(delete_item[0]["_id"])
        # Удаляем по id СУБД в Postgre
        DataBase.ExecuteQuery(f"DELETE FROM test_data WHERE id = {id};")
        return elastic_result
    return False
import sqlite3
import json


def new_category(request_body):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        INSERT INTO Categories(label)
        VALUES (?)  

        """,
            (request_body["label"],),
        )
        id = db_cursor.lastrowid

        return json.dumps({"id": id, "label": request_body["label"]})


def list_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            id,
            label
        FROM Categories
        ORDER BY label ASC
        """
        )
        query_results = db_cursor.fetchall()

        allCategories = []
        for row in query_results:
            allLabels.append({'id': row[0], 'label': row[1]})
        
        serialized_Labels = json.dumps(allLabels)

    return serialized_Labels

def retrieve_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            id,
            label
        FROM Categories 
        WHERE id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()      
        dictionary_version_of_object = dict(query_results)
        serialized_tag = json.dumps(dictionary_version_of_object)

    return serialized_tag

def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount
    return True if number_of_rows_deleted > 0 else False


def update_category(pk, updated_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
        SET label = ?
        WHERE id = ?
        """, (
            updated_category['label'],
            pk
        ))

        rows_updated = db_cursor.rowcount

        if rows_updated == 0:
            return json.dumps({
                'message': 'Tag not found',
                'valid': False
            })
        else:
            return json.dumps({
                'message': 'Tag updated successfully',
                'valid': True
            })
            category = {"id": row[0], "label": row[1]}
            allCategories.append(category)

        serialized_categories = json.dumps(allCategories)

    return serialized_categories


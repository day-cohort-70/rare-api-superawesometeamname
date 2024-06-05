import sqlite3
import json
from datetime import datetime


def new_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        INSERT INTO Posts(user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES (?,?,?,?,?,?,?)  

        """,
            (
                post_data["user_id"],
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
            ),
        )
        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})

def view_all_posts(all_posts):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                Posts.id,
                Posts.user_id,
                Posts.category_id,
                Posts.title,
                Posts.publication_date,
                Posts.image_url,
                Posts.content,
                Posts.approved
        """)
        query_results = db_cursor.fetchall()
        allPosts = []
        for row in query_results:
            allPosts.append(dict(row))

        serialized_allPosts = json.dumps(allPosts)

    return serialized_allPosts

def get_post_by_id(post_id):
    try:
        # Open a connection to the database
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the post by ID
            db_cursor.execute(
                """
                SELECT
                    p.id,
                    p.category_id,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved,
                    p.user_id,
                    u.first_name,
                    u.last_name
                FROM Posts p
                JOIN Users u ON p.user_id = u.id
                WHERE p.id = ?
                """,
                (post_id,),
            )

            # Fetch the query result
            row = db_cursor.fetchone()
            db_cursor.close()

            # If no post is found, return None or raise an error
            if row is None:
                return json.dumps({"error": "Post not found"})

            # Structure the post data
            post = {
                "id": row["id"],
                "category_id": row["category_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
                "user": {
                    "id": row["user_id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                },
            }

            # Serialize the dictionary to JSON
            serialized_post = json.dumps(post)
            return serialized_post

    except sqlite3.Error as e:
        # Handle any database errors
        return json.dumps({"error": str(e)})


# Example usage
# print(get_post_by_id(1))


def get_user_posts(user_id):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            p.id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            p.user_id,
            u.first_name,
            u.last_name,
            c.label
        FROM Posts p
        JOIN Users u ON p.user_id = u.id
        JOIN Categories c ON p.category_id = c.id
        WHERE p.user_id = ?             
        """,
            (user_id,),
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "category_id": row["category_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
                "user": {
                    "id": row["user_id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                },
                "categories": {
                    "id": row["category_id"],
                    "label": row["label"],
                },
            }
            posts.append(post)
        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

        return serialized_posts


def list_posts(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            p.id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved            
        FROM Posts p
        """,
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "category_id": row["category_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }
            posts.append(post)
        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

        return serialized_posts


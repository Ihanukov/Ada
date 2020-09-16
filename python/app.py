from flask import Flask, request, jsonify
import sqlite3
import json
import re # regular expressions
from pprint import pprint
import os.path

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db") 

@app.route("/messages", methods=["GET"])
def messages():
    """
    Return all the messages
    """

    
   
    with sqlite3.connect(db_path) as conn:
        messages_res = conn.execute("select body from messages")
        messages = [replacemet(m[0]) for m in messages_res]
        return jsonify(list(messages)), 200


@app.route("/search", methods=["POST"])
def search_route():
    """
    Search for answers!

    Accepts a 'query' as JSON post, returns the full answer.

    curl -d '{"query":"Star Trek"}' -H "Content-Type: application/json" -X POST http://localhost:5000/search
    """

    with sqlite3.connect(DBPATH) as conn:
        query = request.get_json().get("query")
        res = conn.execute(
            "select id, title from answers where title like ? ", [f"%{query}%"],
        )
        answers = [{"id": r[0], "title": r[1]} for r in res]
        print(query, "--> ")
        pprint(answers)
        return jsonify(answers), 200
    
 
def replacemet(k):
    data_list = []
    newstreing = str(k)

    data_list = re.findall(r'{.*?}', newstreing)
    for match in data_list: # iterate through all matches and create pairs of <id, string>)
        idword = match.replace("{", "") # we are not interested in the curly brackets
        idword = idword.replace("}", "")
        idword = idword.split("|")
        with sqlite3.connect(db_path) as conn:
            rep_value = conn.execute("select value from state WHERE id=?", (idword[0],))
            for row in rep_value:
             if row[0] != "":
                newstreing =  newstreing.replace(match, row[0])
            else:
                newstreing =  newstreing.replace(match, idword[1])
    return newstreing


if __name__ == "__main__":
    app.run(debug=True)

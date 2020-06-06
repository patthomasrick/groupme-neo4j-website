# Patrick Thomas

import os, pprint

from flask import Flask, render_template

from groupme import GroupMe
from graph import DRUMLINE_GC, Neo4jConnector

app = Flask(__name__)

gm = GroupMe(api_token=os.environ["GROUPME_ACCESS_TOKEN"])
gm.set_group(DRUMLINE_GC)

neo4j = Neo4jConnector("localhost", "7687", "neo4j", "groupme")
neo4j.update_user_nodes(gm)
neo4j.update_messages_nodes(gm)
neo4j.make_relationships()

@app.route("/")
def index():
    user_dict = neo4j.get_all_users()
    return render_template('index.html', users=user_dict)

@app.route("/user/<int:userID>")
def user(userID):
    return gm.get_latest_message()

if __name__ == "__main__":
    app.run()

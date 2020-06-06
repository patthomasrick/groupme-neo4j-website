# Patrick Thomas

import os, pprint

from flask import Flask

from groupme import GroupMe
from graph import DRUMLINE_GC, Neo4jConnector

app = Flask(__name__)

gm = GroupMe(api_token=os.environ["GROUPME_ACCESS_TOKEN"])
gm.set_group(DRUMLINE_GC)

neo4j = Neo4jConnector("localhost", "7687", "neo4j", "groupme")
neo4j.update_user_nodes(gm)
neo4j.update_messages_nodes(gm)

@app.route("/")
def hello_world():
    groups = gm.get_groups_index()
    drumline_2019 = None
    for group in groups:
        if int(group["id"]) == DRUMLINE_GC:
            pprint.pprint(group["members"])
    return gm.get_latest_message()

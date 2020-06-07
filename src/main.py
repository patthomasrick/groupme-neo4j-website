# Patrick Thomas

"""
settings
group
    messages
        message
    users
    hall of fame
user
    by group
"""

import os
from datetime import datetime

from flask import Flask, render_template

from groupme import GroupMe
from graph import DRUMLINE_GC, Neo4jConnector

app = Flask(__name__)


neo4j = Neo4jConnector("localhost", "7687", "neo4j", "groupme")
# neo4j.update_user_nodes(gm)
# neo4j.update_messages_nodes(gm)
# neo4j.make_relationships()


@app.template_filter("datetime")
def _jinja2_filter_datetime(value):
    dt = datetime.fromtimestamp(int(value))
    return dt.strftime("%A, %B %d at %I:%M %p")


@app.route("/")
def index():
    gm = GroupMe(api_token=os.environ["GROUPME_ACCESS_TOKEN"])
    groups = gm.get_groups_index()
    return render_template("index.html", groups=groups)
    # user_dict = neo4j.get_all_users()
    # return render_template('index.html', users=user_dict)


@app.route("/group/<int:groupID>")
def group(groupID):
    gm = GroupMe(api_token=os.environ["GROUPME_ACCESS_TOKEN"])
    group = gm.get_group_info(groupID)
    members = group["members"]
    members.sort(key=lambda x: x["name"])
    messages = gm.get_messages(groupID, limit=25)
    return render_template(
        "group.html", group=group, messages=messages, members=members
    )


@app.route("/user/<int:userID>")
def user(userID):
    return gm.get_latest_message()

if __name__ == "__main__":
    app.run()

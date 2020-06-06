import os
import pickle
from datetime import datetime

import py2neo

from groupme import GroupMe

LAST_MESSAGE_FILE = "settings/last_message.pkl"
DRUMLINE_GC = 51300304


class Neo4jConnector:
    def __init__(self, address: str, port: int, username: str, password: str):
        self.graph = py2neo.Graph(host=address, port=port, auth=(username, password))

        try:
            with open(LAST_MESSAGE_FILE, "rb") as f:
                self.last_message = pickle.load(f)
        except FileNotFoundError:
            self.last_message = -1

        try:
            self.graph.run(cypher="create constraint on (u:User) assert u.id IS UNIQUE")
            self.graph.run(cypher="create constraint on (m:Message) assert m.id IS UNIQUE")
        except py2neo.database.ClientError:
            pass
        except ConnectionRefusedError:
            pass

    def update_user_nodes(self, groupme: GroupMe):
        groups = groupme.get_groups_index()
        members = None
        for group in groups:
            if int(group["id"]) == groupme.get_group():
                members = group["members"]
        for member in members:
            properties = "{"
            for key, value in member.items():
                if value is not None:
                    properties += f"{key}: {repr(value)}, "
            properties = properties[:-2] + "}"
            query = f"merge (u:User {properties})"
            self.graph.run(cypher=query)

    def update_messages_nodes(self, groupme: GroupMe):
        before_id = -1
        new_last_message = -1
        print('Updating messages', end='')
        messages = groupme.get_messages()
        while messages is not None:
            for message in messages:
                properties = "{"
                for key, value in message.items():
                    if key != "attachments" and key != "event" and value is not None:
                        properties += f"{key}: {repr(value)}, "
                properties = properties[:-2] + "}"
                query = f"merge (m:Message {properties})"
                self.graph.run(cypher=query)
                new_last_message = max(new_last_message, int(message["id"]))
            before_id = int(messages[-1]["id"])
            if int(messages[-1]["id"]) < self.last_message:
                break
            print('.', end='', flush=True)
            messages = groupme.get_messages(before_id=before_id)
        print(flush=True)

        self.last_message = new_last_message
        with open(LAST_MESSAGE_FILE, "wb") as f:
            pickle.dump(self.last_message, f)

    def make_relationships(self):
        q = """
        match (m:Message)
        match (u:User) where m.sender_id =~ u.user_id
        unwind m.favorited_by as f
        match (u2:User) where u2.user_id =~ f
        merge (m)-[:FAVORITED_BY]->(u2)
        merge (m)-[:SENT_BY]->(u)
        """

        self.graph.run(cypher=q)

    def get_all_users(self) -> dict:
        output = {}
        q = f'match (n:User) return n.user_id, n.name, n.image_url order by n.name'
        result = self.graph.run(cypher=q)
        for user in result.data():
            user_id, name, avatar = user.values()
            output[int(user_id)] = (name, avatar)
        return output

    def get_user_by_id(self, user_id:int) -> dict:
        q = f'match (n:User) where n.user_id =~ "{user_id}" return n'
        result = self.graph.run(cypher=q)
        user = result.evaluate()
        return user

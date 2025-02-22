from simplegmail import Gmail
from simplegmail.query import construct_query

gmail = Gmail()

messages = gmail.get_unread_inbox()


query_params = {
    "newer_than": (1,"day"),
    "unread": True
}

messages = gmail.get_messages(query=construct_query(query_params))

print(messages)
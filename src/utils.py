import hashlib
import json

import numpy as np


def load_data(name):
    with open(name, "r") as f:
        return json.loads(f.read())


def get_chat_data(name):
    data = load_data(name)
    bots = data.keys()
    teams = []
    for bot in bots:
        chats = np.array([(int(message['timestamp']),
                           int(hashlib.sha1(message['msgSenderName'].encode("utf-8")).hexdigest(), 16) % (10 ** 8)) for
                          message in data[bot].values() if
                          type(message) == dict and 'timestamp' in message and 'msgSenderName' in message and message[
                              'msgSenderName'] != bot])
        if len(chats.shape) == 2:
            teams.append(chats)
    return teams


def get_talk_data(name):
    data = load_data(name)
    bots = data.keys()
    teams = []
    for bot in bots:
        periods = data[bot]["history"]
        chats = []
        for period in periods:
            if "isInBO" in data[bot]["history"][period] and "activeHistory" in data[bot]["history"][period] and \
                    data[bot]["history"][period]["isInBO"]:
                members = data[bot]["history"][period]["userList"]
                ids_to_user_name = {}
                for member_id in members:
                    if member_id not in ids_to_user_name:
                        ids_to_user_name[int(member_id)] = members[member_id]["username"]

                talk_history = data[bot]["history"][period]["activeHistory"]
                for talk_event in talk_history:
                    for zoom_id in talk_history[talk_event]['zoomid']:
                        zooom_user_name = ids_to_user_name[zoom_id]
                        member_hash = int(hashlib.sha1(zooom_user_name.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
                        chats.append((int(talk_history[talk_event]['timestamp']), member_hash))
        teams.append(np.array(chats))
    return teams


def get_start_end_time(teams):
    start = end = None
    for team in teams:
        team_min = team[:, 0].min()
        team_max = team[:, 0].max()
        if start is None or team_min < start:
            start = team_min
        if end is None or team_max > end:
            end = team_max
    return start, end


def to_minutes_since_start(start_timestamp, timestamp):
    return (timestamp - start_timestamp) / (1000 * 60)

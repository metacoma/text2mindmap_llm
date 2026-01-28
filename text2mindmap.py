#!/usr/bin/env python3
import os
import sys
from openai import OpenAI
import pprint
import json
import grpc
import freeplane_pb2_grpc
import freeplane_pb2
import json
import argparse
import pyperclip
from dotenv import load_dotenv

load_dotenv()
insert_mode = "current"

def get_data():
    global insert_mode
    parser = argparse.ArgumentParser(description="Read data from clipboard or stdin")
    parser.add_argument('--clipboard', action='store_true', help="Read data from clipboard if set")
    parser.add_argument('--root', action='store_true', help="Insert into the root node")
    args = parser.parse_args()

    if args.root:
        insert_mode = "root"

    if args.clipboard:
        try:
            data = pyperclip.paste()
            if data:
                print("Data read from clipboard.")
                return data
            else:
                print("Clipboard is empty.")
                sys.exit(1)
        except pyperclip.PyperclipException as e:
            print(f"Error accessing clipboard: {e}")
            sys.exit(1)
    else:
        print("Reading data from stdin.")
        data = sys.stdin.read()
        return data

def extract_text_parts(text, max_title_length=40, min_title_length=20, detail_lines=4):
    words = text.split()
    lines = text.splitlines() or [text]

    title = ""
    for i in range(len(words)):
        current_title = " ".join(words[:i+1])
        if min_title_length <= len(current_title) <= max_title_length:
            title = current_title
            break
    else:
        title = " ".join(words[:5])

    details = "\n".join(lines[:detail_lines])

    fulltext = text

    return title, details, fulltext

def prompt3():
    return """
"I will provide text from my clipboard. Your task is to determine the language of the original text, then create a knowledge graph and represent it as mind map with the following rules:

The JSON object should follow these rules:

    Each mindmap node is represented as a key-value table to store contextual information.
    Add the key metrics for node into the key-value table
    There are three special keys for each node:
        "_uuid": A unique 12-digit hexadecimal (base 16) ID for the node.
        "icons": a list of emojis in the format emoj-<EMOJI_CODE> using uppercase Unicode code points, example: emoji-1F3E0
        "detail": A portion of the original clipboard text relevant to this mindmap node.
        "link": A URL to an online resource. If no URL is available, generate a Google search link for the term instead.
        "color": An eye-friendly color in the format "red: <value>, green: <value>, blue: <value>, alpha: <value>".
        "tags": A comma-separated string of tags, e.g., "tag1,tag2,tag3".
        "_relationship": A stringified array in the format "<UUID>:<relationship_type>,<UUID2>:<relationship_type2>".
    If a node’s value is a dict, it represents a child node where these rules apply as well.
    Don't use json array, use only json dicts
Here’s an example JSON structure to follow:
    {
    "house": {
        "_uuid": "4e7d52ab13c0",
        "detail": "The house is located on Suze Robertssonstraat 7",
        "icons": "emoji-1F3E0",
        "tags": "building,house",
        "link": "https://www.google.com/maps/place/Suze+Robertsonstraat+7",
        "color": "red: 255, green: 120, blue: 120, alpha: 255",
        "type": "building",
        "address": "Suze Robertsoonstraat 7",
        "floors": 18,
        "apartment 1": {
            "_uuid": "ff23ab781d44",
            "tags": "apartment",
            "icons": "emoji-1F46A",
            "residents": 2,
            "detail": "Family and child",
            "link": "https://www.google.com/search?q=apartment1&btnI=I",
            "color": "red: 120, green: 100, blue: 120, alpha: 255",
            "type": "apartment",
            "floor": "1",
            "resident 1": {
                "_uuid": "a3f9b01c8d2e",
                "_relationship": "ff23ab781d44:tenant",
                "icons": "emoji-1F468",
                "tags": "resident",
                "name": "Steven Peterson",
                "link": "https://en.wikipedia.org/wiki/Peterson,_Steven",
                "sex": "male",
                "age": "42"
            },
            "resident 2": {
                "_uuid": "b3f9b03a9d21",
                "_relationship": "a3f9b01c8d2e:married,ff23ab781d44:tenant",
                "icons": "emoji-1F469",
                "tags": "resident",
                "name": "Anna Bolein",
                "link": "https://en.wikipedia.org/wiki/Anna,_Bolein",
                "sex": "female",
                "age": "42"
            }
        }
    }
}
Generate only the json without any additional explanation and text information
My clipboard data is:
"""


def text2mindmap():
    channel = grpc.insecure_channel('localhost:50051')
    fp = freeplane_pb2_grpc.FreeplaneStub(channel)

    current_node = fp.GetCurrentNode(freeplane_pb2.GetCurrentNodeRequest())
    print(current_node.node_id)

    data = get_data()

    client = OpenAI()
    completion = client.chat.completions.create(

        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt3() + data}
        ]
    )

    answer = completion.choices[0].message.content
    lines = answer.splitlines()[1:-1]
    pprint.pprint(lines, stream=sys.stderr)

    json_string = "\n".join(lines)

    parsed_json = json.loads(json_string)

    print(json_string)


    title, detail, fulltext = extract_text_parts(data)
    # add head node
    mindmap_json = {
        "_fp_import_root_node": current_node.node_id,
        title: {
            "detail": detail,
            "note": fulltext,
            **parsed_json
        }
    }

    pprint.pprint(mindmap_json)

    fp.MindMapFromJSON(freeplane_pb2.MindMapFromJSONRequest(json=json.dumps(mindmap_json)))


if __name__ == "__main__":
    text2mindmap()

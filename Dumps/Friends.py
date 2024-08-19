
import requests
import json
import os

Uuid = []
def save_to_file(filename, data):
    try:
        with open(filename, 'w') as f:
            for item in data:
                f.write(f"{item}\n")
    except IOError as e:
        print(f"Terjadi kesalahan saat menyimpan file: {e}")

def Loop_dump(user, token, cursor=None):
	try:
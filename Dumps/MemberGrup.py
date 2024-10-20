# Author: Fajarkyy

import requests
import json
import os

Uuid = []
print("Direktori kerja saat ini:", os.getcwd())

def save_to_file(filename, data):
    try:
        with open(filename, 'w') as f:
            for item in data:
                f.write(f"{item}\n")
    except IOError as e:
        print(f"Terjadi kesalahan saat menyimpan file: {e}")

def Loop_Dump(user, token, cursor=None):
    try:
        data = {
            'access_token': token,
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "purpose": "fetch",
            "fb_api_req_friendly_name": "FetchGroupMemberListRecentlyJoined_At_Connection_Pagination_Group_group_member_profiles_connection",
            "fb_api_caller_class": "AtConnection",
            "client_doc_id": "3718233544957823756815644982",
            "fb_api_client_context": '{"load_next_page_counter":2,"client_connection_size":30}',
            "variables": json.dumps({
                "group_member_profiles_connection_first": 15,
                "profile_image_size": 176,
                "group_id": user,
                "group_member_profiles_connection_at_stream_use_customized_batch": False,
                "group_member_profiles_connection_after_cursor": cursor,
                "paginationPK": user
            }),
            "fb_api_analytics_tags": ["At_Connection", "GraphServices"],
            "client_trace_id": "d29a9e65-3e76-4f99-9e0f-0b2302cfc266"
        }
        response = requests.post(
            'https://graph.facebook.com/graphql',
            data=data
        ).json()
        
        for edge in response.get("data", {}).get("node", {}).get("group_member_profiles", {}).get("edges", []):
            try:
                uid = edge["node"]["id"]
                name = edge["node"]["name"]
                entry = f"{uid}|{name}"
                print(f"Dumps {uid}|{len(Uuid)}....", end='\r')
                if entry not in Uuid:
                    Uuid.append(entry)
                    save_to_file('group_members_dump.txt', Uuid)
            except KeyError as e:
                print(f"KeyError: {e}")

        if response.get("data", {}).get("node", {}).get("group_member_profiles", {}).get("page_info", {}).get("has_next_page"):
            next_cursor = response.get("data", {}).get("node", {}).get("group_member_profiles", {}).get("page_info", {}).get("end_cursor")
            Loop_Dump(user, token, next_cursor)
    except:pass

if __name__ == '__main__':
    os.system('clear')
    uid = input("Masukkan UID grup: ")
    token = "EAAAAU..." #Dump menggunakan Token EAAAAU
    Loop_Dump(uid, token, '')

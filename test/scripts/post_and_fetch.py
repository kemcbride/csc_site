import requests

from typing import Dict

# assuming that server is running on localhost at the port specifiied in app.py...

base_url = "http://0.0.0.0:25777"
query_params = {"name": "Your mom", "email": "blazeit24069@yahoo.com", "content": "blah"}


def stringify_params(query_params: Dict[str, str]) -> str:
    pairs = [f"{k}={v}" for k, v in query_params.items()]
    result = "&".join(pairs)
    print(result)
    return result


result = requests.post(f"{base_url}/post_timelinepost?{stringify_params(query_params)}") 
print("Post submitted!")
print(result)
print(result.__dict__)


result = requests.get(base_url+"/get_timelineposts")
print("Get submitted!")
print(result)
print(result.__dict__)

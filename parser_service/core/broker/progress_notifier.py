import requests

def send_progress(user_id: int, status: str):
    url = 'http://api_service:81/posts/sendprogress'
    data = {
        'user_id': user_id,
        'status': status,
    }
    try:
        resp = requests.post(url, json=data)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
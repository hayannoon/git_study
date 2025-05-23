import requests

SWARM_URL = "https://swarm.example.com"
REVIEW_ID = "12345"  # 실제 review id로 대체
API_TOKEN = "your_swarm_api_token"  # 필요시

def post_comment(review_id, comment):
    url = f"{SWARM_URL}/api/v10/reviews/{review_id}/comments"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    data = {"body": comment}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

def approve_review(review_id):
    url = f"{SWARM_URL}/api/v10/reviews/{review_id}/approve"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()

def submit_review(review_id):
    url = f"{SWARM_URL}/api/v10/reviews/{review_id}/transition"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    data = {"state": "approved"}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

if __name__ == "__main__":
    # result 파일 읽기
    with open("result", "r", encoding="utf-8") as f:
        lines = f.readlines()
        status = lines[0].strip()
        comment = "".join(lines[1:])

    # 1. 코멘트 등록
    post_comment(REVIEW_ID, comment)

    # 2. 성공이면 approve & submit
    if status == "pass":
        approve_review(REVIEW_ID)
        submit_review(REVIEW_ID)
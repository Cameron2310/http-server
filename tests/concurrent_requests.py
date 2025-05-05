import requests
import threading


def make_get_request(t_id: int):
    for i in range(100):
        response = requests.get("http://localhost:8000")
        print(f"request {t_id * i}: {response.status_code}")
    

def run_concurrent_test(num_threads: int):
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=make_get_request, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


run_concurrent_test(10)

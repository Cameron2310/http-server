import random
import requests
import string
import threading


def generate_body(length: int):
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def make_get_request(t_id: int):
    body = generate_body(128)

    while True:
        n_retries = 0

        try:
            requests.get("http://localhost:8000/echo", json=body)
            break
        except Exception:
            print("\n\nhandling exception\n\n")

            n_retries += 1
            if n_retries > 5:
                break
            else:
                pass
                

        # print(f"request {t_id * i}: {response.status_code}")
    

def run_concurrent_test(num_threads: int):
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=make_get_request, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def run_basic_test_w_body():
    for i in range(50):
        print(f"id #{i}: sending response...")
        make_get_request(i)
        print(f"id #{i}: achieved response...")

run_basic_test_w_body()
# run_concurrent_test(10)

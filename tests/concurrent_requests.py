import random
import requests
import string
import threading


def generate_body(length: int):
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def make_get_request(t_id: int):
    body = generate_body(128)
    print(f"\n\ngenerated body for request {t_id}: {body}")
    
    while True:
        n_retries = 0
        
        try:
            response = requests.get("http://localhost:8000/echo", data=body)
            print(f"request {t_id}: {response.text}\n")
            break
        except Exception as e:
            print("Exception ", e)
            print("\n\nhandling exception\n\n")

            n_retries += 1
            if n_retries > 5:
                break
            else:
                pass
                

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
        make_get_request(i)

# run_basic_test_w_body()
run_concurrent_test(10)

import random
import requests
import string
import threading
import time
import concurrent.futures


def generate_body(length: int):
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def generate_success_percentage(total: int, success_count: int):
    return (success_count / total) * 100


# def make_get_request(t_id: int):
def make_get_request(request_id, body=None):
    if not body:
        body = generate_body(128)
    
    while True:
        n_retries = 0
        
        try:
            response = requests.get("http://localhost:8000/echo", data=body)
            print(f"request {request_id}: {response.text}\n")
            
            return response.text

        except Exception as e:
            print(f"Exception {e}\nRetrying connection...")

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


def run_concurrent_test_2():
    body = [generate_body(128) for _ in range(10)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: # optimally defined number of threads
        res = [executor.submit(make_get_request, b) for b in body]
        concurrent.futures.wait(res)


def run_basic_test_w_body():
    responses = []
    count = 0

    start = time.time()
    for i in range(500):
        responses.append(make_get_request(i))

    end = time.time()

    for r in responses:
        if r:
            count += 1

    print(f"{end - start} secs")
    print(f"Successful response percentage: {generate_success_percentage(len(responses), count)}%")

run_basic_test_w_body()
# run_concurrent_test(10)

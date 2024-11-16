import json
import requests
import time
import os
import hashlib

JSON_RPC_TOKEN = ""
if JSON_RPC_TOKEN == "": 
    with open("RPC_TOKEN", 'r') as f:
        JSON_RPC_TOKEN = f.read().strip()

# Tunable parameters
HARDHAT_PORT = 1234
MAX_RUNS = 200
COOLDOWN_SECONDS = 1
PAYLOADS = "payloads.json"
LOG_DIR = "logs"

HEADERS = {
    'Content-Type': 'application/json'
}
FORK_PAYLOAD = {
    "jsonrpc": "2.0",
    "method": "hardhat_reset",
    "params": [
        {
            "forking": {
                "jsonRpcUrl": JSON_RPC_TOKEN,
                "blockNumber": 20845407
            }
        }
    ],
    "id": 1
}
REQUEST_BLOCK_INFO_PAYLOAD = {
    "jsonrpc": "2.0",
    "method": "eth_getBlockByNumber",
    "params": ["latest", False],
    "id": 1
}


def submit_payload(payload):
    response = requests.request("POST", f"http://127.0.0.1:{HARDHAT_PORT}", headers=HEADERS, data=json.dumps(payload))  
    assert response.status_code == 200
    return json.loads(response.text)


def main(run):
    # first fork the mainnet
    submit_payload(FORK_PAYLOAD)

    # then read payloads from a file
    with open(PAYLOADS, 'r') as f:
        payloads = json.load(f)
    
    # submit each payload and log the response
    with open(f"{LOG_DIR}/output_{str(run).zfill(3)}.json", 'w') as f:
        for i, payload in enumerate(payloads):
            response = submit_payload(payload)
            
            # log the response
            f.write(json.dumps(response).replace("\n", ""))
            f.write("\n")

    # request block info
    response = submit_payload(REQUEST_BLOCK_INFO_PAYLOAD)

    # return the hash of the block
    return response


if __name__ == "__main__":
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    for i in range(MAX_RUNS):
        main(i)
        time.sleep(1)


    log_files = os.listdir(LOG_DIR)
    log_files = [fname for fname in log_files if fname.endswith(".json")]
    log_files.sort()

    # display the hash of the last block
    for log_file in log_files:
        with open(f"{LOG_DIR}/{log_file}", 'r') as f:
            file_content = f.read()
        print(f"{log_file}: {hashlib.sha256(file_content.encode()).hexdigest()}")

    
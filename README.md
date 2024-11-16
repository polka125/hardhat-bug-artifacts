This is a repository for bug artifacts for the Hardhat tool 


### Steps to build: 

1. `git clone {todo}`
2. put your remote api key to the file `RPC_TOKEN`
3. `docker build -t hardhat_bug .`
4. `docker run -v ./host_logs:/app/logs -it hardhat_bug`
5. `find ./host_logs -type f -print0 | sort -z | xargs -0 shasum -a 1`


### If no error: 

in the `submit_payloads.py` please try to increate the `MAX_RUNS` parameters to a larger value, if still no bug, please try to decrease the `COOLDOWN_SECONDS` parameter (but decreasing it too much will cause `connection refuse` error)


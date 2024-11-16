FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv nodejs npm git
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip3 install requests
RUN npm init -y
RUN npm install --save-dev hardhat

COPY submit_payloads.py /app
COPY hardhat.config.js /app
COPY payloads.json /app
COPY RPC_TOKEN /app
COPY entrypoint.sh /app

# create logs directory
RUN mkdir /app/logs
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# in order to build the docker, run the following command
# docker build -t hardhat_bug .

# in order to run the docker, executing the CMD command, run the following command, binding with the host_logs directory:
# docker run -v ./host_logs:/app/logs -it hardhat_bug
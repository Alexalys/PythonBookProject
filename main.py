import signal
import sys
import uvicorn
import json

def handle_exit(sig, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

if __name__=='__main__':
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    with open('./config/config.json','r', encoding='utf-8') as f:
        config = json.load(f)
    uvicorn.run("app.apis.__init__:app", **config)
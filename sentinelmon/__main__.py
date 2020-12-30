import argparse
import os
import requests
import json
import sys, os
from .auth import TokenRequester

parser = argparse.ArgumentParser(
    prog="sentinelmon", description="Simple Azure Sentinel monitor"
)

args = parser.parse_args()


def main():
    global args
    req = TokenRequester()
    token = req.acquire_token()
    if not token:
        print("Could not acquire token")
        sys.exit(1)


if __name__ == "__main__":
    main()
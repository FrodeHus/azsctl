import os, sys, atexit, json
from typing import Any


class Config:
    SUBSCRIPTION = "subscription"
    SUBSCRIPTION_ID = "subscriptionId"
    WORKSPACE = "workspaceName"
    WORKSPACE_ID = "workspaceId"
    def __init__(self):
        self._config = {}
        self.config_has_changed = False
        from pathlib import Path

        home = str(Path.home())
        self.config_path = f"{home}/.sentinelmon"
        self.config_file_path = f"{self.config_path}/config.json"
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)

        if os.path.exists(self.config_file_path):
            with open(self.config_file_path) as config_file:
                self._config = json.load(config_file)

        atexit.register(
            lambda: open(self.config_file_path, "w").write(
                json.dumps(self._config, indent=2)
            )
            if self.config_has_changed
            else None
        )

    def set(self, key: str, value: Any):
        """
        Sets a config value
        """
        self._config[key] = value
        self.config_has_changed = True

    def get(self, key: str):
        """
        Retrieves a config value - None if not existant
        """
        if key in self._config:
            return self._config[key]
        return None
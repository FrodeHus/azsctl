import os, sys, atexit, json
from typing import Any, Tuple


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
        self.config_path = f"{home}/.azsctl"
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

    def set_subscription(self, subscription_name: str, subscription_id: str):
        """
        Sets the active subscription
        """
        self._set(Config.SUBSCRIPTION, subscription_name)
        self._set(Config.SUBSCRIPTION_ID, subscription_id)

    def set_workspace(self, workspace_name: str, workspace_id: str):
        """
        Sets the active log analytics workspace
        """
        self._set(Config.WORKSPACE, workspace_name)
        self._set(Config.WORKSPACE_ID, workspace_id)

    def get_subscription(self) -> Tuple[str, str]:
        """
        Gets the active subscription name and id
        """
        subscription_name = self._get(Config.SUBSCRIPTION)
        subscription_id = self._get(Config.SUBSCRIPTION_ID)
        return subscription_name, subscription_id

    def get_workspace(self) -> Tuple[str, str]:
        """
        Gets the active workspace name and id
        """
        workspace_name = self._get(Config.WORKSPACE)
        workspace_id = self._get(Config.WORKSPACE_ID)
        return workspace_name, workspace_id

    def _set(self, key: str, value: any):
        """
        Sets a config value
        """
        self._config[key] = value
        self.config_has_changed = True

    def _get(self, key: str):
        """
        Retrieves a config value - None if not existant
        """
        if key in self._config:
            return self._config[key]
        return None
from sentinelmon.config import Config
import msal
import requests
import sys, os, atexit


class TokenRequester:
    def __init__(self):
        self._config = Config()
        self._scope = ["https://management.core.windows.net//user_impersonation"]
        cache = self._init_cache()
        self._app = msal.PublicClientApplication(
            "5850ddcd-4b8e-4777-9ea9-46e470a30fa2",
            authority="https://login.microsoftonline.com/common",
            token_cache=cache,
        )

    def _init_cache(self):
        cache = msal.SerializableTokenCache()
        cachefile = f"{self._config.config_path}/tokencache"
        if os.path.exists(cachefile):
            cache.deserialize(open(cachefile, "r").read())

        atexit.register(
            lambda: open(cachefile, "w").write(cache.serialize())
            if cache.has_state_changed
            else None
        )

        return cache

    def acquire_token(self):
        accounts = self._app.get_accounts()
        result = None
        if accounts:
            chosen = accounts[0]
            result = self._app.acquire_token_silent(self._scope, account=chosen)
        if not result:
            return self._acquire_token_interactively()
        if "access_token" in result:
            return result["access_token"]

    def _acquire_token_interactively(self):
        flow = self._app.initiate_device_flow(scopes=self._scope)
        print(flow["message"])
        sys.stdout.flush()
        result = self._app.acquire_token_by_device_flow(flow)
        if "access_token" in result:
            return result["access_token"]
        elif "error_description" in result:
            print(result["error_description"])
        return None

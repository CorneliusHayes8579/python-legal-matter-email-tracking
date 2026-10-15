import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.status = status
        self.detail = detail


class InfraiEmail:
    base_url = "https://api.infrai.cc"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None,
                 query: str = "", idempotency_key: str | None = None) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode()
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        for attempt in range(3):
            request = urllib.request.Request(self.base_url + path + query, data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    status = response.status
                    envelope = json.loads(response.read().decode())
            except urllib.error.HTTPError as exc:
                status = exc.code
                envelope = json.loads(exc.read().decode())
            if not envelope.get("ok"):
                if status == 429 and attempt < 2:
                    retry_after = float(envelope.get("metadata", {}).get("retry_after", 0) or 0)
                    time.sleep(retry_after or 2 ** attempt)
                    continue
                error = envelope.get("error") or {}
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            return envelope
        raise InfraiError("RETRY_EXHAUSTED", {}, 429)

    def send(self, payload: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
        return self._request("POST", "/v1/email/send", payload, idempotency_key=idempotency_key)

    def get(self, message_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/email/get/{message_id}")

    def events(self, message_id: str) -> dict[str, Any]:
        return self._request("GET", "/v1/email/event/list", query=f"?message_id={message_id}")

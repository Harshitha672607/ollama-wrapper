import requests
import json
from app.core.config import settings
from app.core.logging import logger

class PIClient:
    def __init__(self, base_url: str = settings.PI_BASE_URL, transaction_id: str = settings.TRANSACTION_ID):
        self.base_url = base_url
        self.transaction_id = transaction_id

    def insert_instance(self, schema_id: str, payload: dict, token: str):
        url = f"{self.base_url}/schemas/{schema_id}/instances"
        params = {"transactionID": self.transaction_id}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        logger.info("PI insert: %s", url)
        resp = requests.post(url, params=params, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def delete_instances(self, schema_id: str, filter_payload: dict, token: str):
        url = f"{self.base_url}/schemas/{schema_id}/instances"
        params = {"confirmDelete": "true"}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        resp = requests.delete(url, params=params, headers=headers, json=filter_payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def update_instances(self, schema_id: str, payload: dict, token: str):
        url = f"{self.base_url}/schemas/{schema_id}/instances"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        resp = requests.put(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_instances(self, schema_id: str, token: str, db_type: str = "TIDB"):
        url = f"{self.base_url}/schemas/{schema_id}/instances/list"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {"dbType": db_type}
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

pi_client = PIClient()

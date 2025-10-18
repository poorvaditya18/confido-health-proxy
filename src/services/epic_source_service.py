import requests, logging
from configs.config import Config
logger = logging.getLogger("epic_source_service")

class EpicSourceService:
    def __init__(self):
        self.source = "EPIC"
        self.base_url = Config.EPIC_BASE_URL

    def _get_access_token(self):
        try:
            url = Config.AUTH_SERVICE_URL
            headers = {"x-source-type": self.source}
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get("access_token")
            if not self.access_token:
                raise Exception("no access token received from auth service")
            return self.access_token
        except Exception as e:
            raise Exception(f"error obtaining access token from auth service. err: {str(e)}")
    
    def get_patient_data(self, patient_id: str):
        try:
            url = f"{self.base_url}/Patient/{patient_id}?_format=json"
            token = self._get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"error getting patient data from {self.source} for patient_id: {patient_id}. err: {str(e)}")

    def get_appointment_data(self, patient_id: str):
        try:
            url = f"{self.base_url}/Appointment?patient={patient_id}&service-category=appointment&_format=json"
            token = self._get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"error getting appointment data from {self.source} for patient_id: {patient_id}. err: {str(e)}")

import requests


class ReportClient:
    BASE_URL = "http://127.0.0.1:4723"

    @staticmethod
    def set_test_info(driver, name, status, error=None):
        payload = {
            "sessionId": driver.session_id,
            "testName": name,
            "testStatus": status,
        }
        if error:
            payload["error"] = error

        response = requests.post(f"{ReportClient.BASE_URL}/setTestInfo", json=payload)
        print(f"set_test_info: {response.status_code} {response.text}")
        return response

    @staticmethod
    def get_report():
        response = requests.get(f"{ReportClient.BASE_URL}/getReport")
        if response.status_code == 200:
            return response.text
        print(f"get_report error: {response.status_code} {response.text}")
        return None

    @staticmethod
    def delete_report_data():
        response = requests.delete(f"{ReportClient.BASE_URL}/deleteReportData")
        print(f"delete_report_data: {response.status_code} {response.text}")
        return response

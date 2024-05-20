import sys
import requests
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# check dims
try:
    readiness_url = "http://localhost:8081/readiness"
    # need verify false b/c using selfsigned certs
    r = requests.get(readiness_url, verify=False)
    if (r.status_code != 200):
        print("Notifier readiness failed")
        sys.exit(1)
    print("Notifier readiness passed")
    sys.exit(0)
except Exception:
    print("Notifier readiness failed")
    sys.exit(1)
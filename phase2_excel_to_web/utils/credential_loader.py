from pathlib import Path

# Absolute path to credentials file
BASE_DIR = Path(__file__).resolve().parents[2]
CRED_FILE = BASE_DIR / "config" / "credentials.properties"


def get_password(OEM: str) -> str | None:
    """
    Fetch password for a given OEM from credentials.properties
    """

    if not CRED_FILE.exists():
        print(f" credentials.properties not found at {CRED_FILE}")
        return None

    with open(CRED_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # ignore empty lines & comments
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            if key.strip() == OEM.strip():
                return value.strip()

    return None

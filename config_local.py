import os
from config import *

BASE_DIR = os.getenv('BASE_DIR')
LOG_DIR = os.path.join(BASE_DIR, 'var/log/pgadmin')
LOG_FILE = os.path.join(LOG_DIR, 'pgadmin4.log')
DATA_DIR = os.path.join(BASE_DIR, 'var/lib/pgadmin')
SQLITE_PATH = os.path.join(DATA_DIR, 'pgadmin4.db')
SESSION_DB_PATH = os.path.join(DATA_DIR, 'sessions')
STORAGE_DIR = os.path.join(DATA_DIR, 'storage')
KERBEROS_CCACHE_DIR = os.path.join(DATA_DIR, 'krbccache')
AZURE_CREDENTIAL_CACHE_DIR = os.path.join(DATA_DIR, 'storage')

if not os.path.exists(DATA_DIR):
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SESSION_DB_PATH, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(KERBEROS_CCACHE_DIR, exist_ok=True)
    os.makedirs(AZURE_CREDENTIAL_CACHE_DIR, exist_ok=True)

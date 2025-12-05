import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
access_log = "-"
error_log = "-"

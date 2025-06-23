import time
from datetime import datetime

now = datetime.now()
start = time.perf_counter()
# ... some code ...
elapsed_ms = (time.perf_counter() - start) * 1000
print(f"경과 시간: {int(now.timestamp() * 1000)}ms")
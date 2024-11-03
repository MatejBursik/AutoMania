import sys
import os

print("Python executable:", sys.executable)
print("Virtual environment (sys.prefix):", sys.prefix)
print("VIRTUAL_ENV environment variable:", os.environ.get('VIRTUAL_ENV'))

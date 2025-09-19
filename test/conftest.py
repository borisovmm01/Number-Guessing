import sys
import os
# Добавляем корень репозитория (где лежит main.py) в sys.path, чтобы pytest мог импортировать main
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

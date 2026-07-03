import ast
from pathlib import Path

for file in Path('.').glob('*.py'):
    ast.parse(file.read_text(encoding='utf-8'))
print('syntax ok')

src/flask/blueprints.py 파일의 `Blueprint.__init__` 메서드에서 `name` 매개변수가 비어있는 경우 `ValueError`를 발생시키는 검증 코드를 추가했다.

```python
if not name:
    raise ValueError("'name' must not be empty.")
```
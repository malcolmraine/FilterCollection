# FilterCollection
Query-able collection in Python

```python
from FilterCollection import FilterCollection


test = FilterCollection([1, 2, 3, 4])
print(test.query().where(lambda x: x >= 3).get())
```
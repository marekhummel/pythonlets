# python-misc
Collection of various python mini projects


### Dev
Since this is not a complete project but rather a collection of single file programs, `mypy` has be called on each file independently.
```bash
find -type f -name "*.py" -not -path "./.venv/*" -not -path "./_out/*" -exec poetry run mypy {} \;
```

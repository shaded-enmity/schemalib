# schemalib

Schemalib is a library for simple handling and usage of JSON schemas in your code. Simply define
a schema library with paths from which to load the schemas and then use the `check` decorator provided
by the object instance to perform actual checking against that schema library. Relative or absolute paths
can be specified, there's also a support for loading schemas relative to a Python module (Python's module load
order applies here).

## Examples:

```python
from schemalib import SchemaLibrary
schemas = SchemaLibrary('/my/schema/path', 'package://my.python.package')

# check contents of keyword argument `data_obj`
@schemas.check(data_obj='some-schema-file')
def my_function(data_obj=None):
    ...

# check return value of the function
@schemas.check('some-other-schema-file')
def my_function():
    ...

# check both
@schemas.check('some-other-schema-file', data_obj='some-schema-file')
def my_function(data_obj=None):
    ...
```

## Lincese

GNU/GPLv-3

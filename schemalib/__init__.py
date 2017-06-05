import jsonschema
import json
import pkgutil
import errno
from os import path


PKG_PREFIX = 'package://'
SCHEMA_SUFFIX = '.json'


def _get_positional_args(func):
    """Get positional argument names for given function

    :param func: function to inspect
    :return:
    """
    code = func.__code__
    return list(code.co_varnames[:code.co_argcount])


class SchemaArgumentError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


class Schema(object):
    def __init__(self, name, schema):
        """Initialize schema object

        :param name: name of the schema file
        :type name: str
        :param schema: schema contents
        :type schema: str
        """

        self.name = name
        self.schema = schema

    def check(self, data):
        """Check the validity of data against this schema

        :param data: Input object to check
        :raises: jsonschema.ValidationError
        """

        jsonschema.validate(data, self.schema)


class SchemaLibrary(dict):
    def __init__(self, *base_paths):
        """Initialize schema library object

        :param base_paths: paths where to look when looking for a schema
        :type base_paths: str
        """

        self._base_paths = list(base_paths)
        super(SchemaLibrary, self).__init__()

    def load_schema(self, name):
        """Load schema specified by name, searching `base_paths` sequentially

        :param name: schema name
        :type name: str
        :return: schema contents as string
        :rtype: str
        :raises: schemalib.SchemaNotFoundError when the schema couldn't be found or was empty
        """

        for p in self._base_paths:
            if p.startswith(PKG_PREFIX):
                stripped, data = p[len(PKG_PREFIX):], None
                try:
                    data = pkgutil.get_data(stripped, name + SCHEMA_SUFFIX)
                except IOError as err:
                    if err.errno == errno.ENOENT:
                        continue
                if data:
                    return data
            else:
                lookup = path.join(p, name) + SCHEMA_SUFFIX
                if path.exists(lookup):
                    with open(lookup, 'r') as f:
                        data = f.read()
                        if data:
                            return data

        raise SchemaNotFoundError(name)

    def __getitem__(self, item):
        """Caching wrapper around __getitem__ that lazily loads schemas from disk

        :param item: Schema name to look up
        :type item: str
        :return: Schema object
        :rtype: schemalib.Schema
        """

        if item not in self:
            schema = Schema(item, json.loads(self.load_schema(item)))
            self[item] = schema
        return super(SchemaLibrary, self).__getitem__(item)


    def check(self, *args, **kwargs):
        """ Function decorator that allows for return value and keyword parameter schema validation """

        assert len(args) < 2, 'Cannot validate multiple return schemas'

        return_schema = args[0] if len(args) > 0 else None
        schemas = dict(kwargs)

        def wrapped(f):
            def inner(*iargs, **ikwargs):
                positional = _get_positional_args(f)
                for k, v in schemas.items():
                    if k in ikwargs:
                        self[v].check(ikwargs[k])
                    elif k in positional:
                        idx = positional.index(k)
                        self[v].check(iargs[idx])
                    else:
                        raise SchemaArgumentError('Argument does not exist: {}'.format(k))
                v = f(*iargs, **ikwargs)
                if return_schema:
                    self[return_schema].check(v)
                return v
            return inner
        return wrapped


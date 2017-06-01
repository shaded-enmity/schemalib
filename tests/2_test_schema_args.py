import schemalib
from jsonschema import ValidationError

schemas = schemalib.SchemaLibrary('./schemas/')

def test_single_kwarg():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(kwarg=None):
        pass
    single(kwarg={'test': 1})

def test_single_kwarg_bad_schema():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(kwarg=None):
        pass
    try:
        single(kwarg={'bad_test': 1})
        assert False, 'Validation should have failed'
    except ValidationError:
        pass

def test_multi_kwarg():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(another=None, kwarg=None):
        pass
    single(kwarg={'test': 1})

def test_multi_kwarg_bad_schema():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(another=None, kwarg=None):
        pass
    try:
        single(kwarg={'bad_test': 1})
        assert False, 'Validation should have failed'
    except ValidationError:
        pass

def test_complex():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(x, y, z=None, kwarg=None):
        pass
    single(0, 0, kwarg={'test': 1})



import schemalib
from jsonschema import ValidationError

schemas = schemalib.SchemaLibrary('./schemas/')


def test_single_positional():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(kwarg):
        pass
    single({'test': 1})

def test_single_kwarg():
    @schemas.check(kwarg='test-schema-1.0.0')
    def single(kwarg=None):
        pass
    single(kwarg={'test': 1})

def test_single_unknown():
    @schemas.check(not_there='test-schema-1.0.0')
    def single(kwarg):
        pass
    try:
        single({'test': 1})
    except schemalib.SchemaArgumentError as e:
        assert (e.message == "Argument does not exist: not_there")
        return 
    assert False, 'Should not get here'

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

def test_complex_2():
    @schemas.check(kwarg='test-schema-1.0.0', y='test-schema-1.0.0')
    def single(x, y, z=None, kwarg=None):
        pass
    single(0, {'test': 1}, kwarg={'test': 1})


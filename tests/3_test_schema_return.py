import schemalib
from jsonschema import ValidationError

schemas = schemalib.SchemaLibrary('./schemas/')

def test_single_kwarg():
    @schemas.check('test-schema-1.0.0')
    def single(kwarg=None):
        return {'test': 1}
    single()

def test_single_kwarg_bad_schema():
    @schemas.check('test-schema-1.0.0')
    def single(kwarg=None):
        return {'bad_test': 1}
    try:
        single()
        assert False, 'Validation should have failed'
    except ValidationError:
        pass

def test_complex():
    @schemas.check('test-schema-1.0.0')
    def single(x, y, z=None, kwarg=None):
        return {'test': 1}
    single(0, 0)


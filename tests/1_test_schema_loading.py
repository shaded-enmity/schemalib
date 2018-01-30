import schemalib

def test_local_dir_schema():
    schemas = schemalib.SchemaLibrary('./schemas/')
    schemas.load_schema('test-schema-1.0.0')

def test_package_resolution_schema():
    schemas = schemalib.SchemaLibrary('package://schemas')
    schemas.load_schema('test-schema-1.0.0')

def test_unknown_schema():
    schemas = schemalib.SchemaLibrary('package://schemas')
    caught = True
    try:
        schemas.load_schema('---invalid-name---')
    except schemalib.SchemaNotFoundError:
        caught = False
    assert not caught


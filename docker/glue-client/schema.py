"""Schema for AvroDeserializer and AvroSerializer."""

deserializer_schema = """
{
    "name": "iris_data",
    "type": "record",
    "fields": [
        {
            "name": "id",
            "type": ["int", "null"]
        },
        {
            "name": "timestamp",
            "type": ["string", "null"]
        },
        {
            "name": "sepal_length",
            "type": ["double", "null"]
        },
        {
            "name": "sepal_width",
            "type": ["double", "null"]
        },
        {
            "name": "petal_length",
            "type": ["double", "null"]
        },
        {
            "name": "petal_width",
            "type": ["double", "null"]
        },
        {
            "name": "target",
            "type": ["int", "null"]
        }
    ]
}
"""


serializer_schema = """
{
    "name": "new_iris_data",
    "type": "record",
    "fields": [
        {
            "name": "id",
            "type": ["int", "null"]
        },
        {
            "name": "timestamp",
            "type": ["string", "null"]
        },
        {
            "name": "sepal_length",
            "type": ["double", "null"]
        },
        {
            "name": "sepal_width",
            "type": ["double", "null"]
        },
        {
            "name": "petal_length",
            "type": ["double", "null"]
        },
        {
            "name": "petal_width",
            "type": ["double", "null"]
        },
        {
            "name": "target",
            "type": ["int", "null"]
        }
    ]
}
"""

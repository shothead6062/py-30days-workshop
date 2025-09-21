from pydantic import TypeAdapter


def test_typeadapter_list_int_from_strings():
    ta = TypeAdapter(list[int])
    assert ta.validate_python(["1", "2", "3"]) == [1, 2, 3]

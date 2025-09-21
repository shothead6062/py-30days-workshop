from pydantic import ValidationError

from demo_app.cli_args import Args, parse_and_validate


def test_cli_args_ok():
    args = parse_and_validate(["--host", "localhost", "--port", "8080"])
    assert isinstance(args, Args)
    assert args.host == "localhost"
    assert args.port == 8080


def test_cli_args_invalid_port():
    try:
        parse_and_validate(["--host", "localhost", "--port", "notint"])
    except ValidationError:
        pass
    else:
        raise AssertionError("Expected ValidationError for non-integer port")

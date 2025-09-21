import argparse

from pydantic import BaseModel


class Args(BaseModel):
    host: str
    port: int


def parse_and_validate(argv: list[str] | None = None) -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True)
    ns = parser.parse_args(argv)
    # Use model_validate for dict-like input (Pydantic v2)
    return Args.model_validate(vars(ns))


__all__ = ["Args", "parse_and_validate"]

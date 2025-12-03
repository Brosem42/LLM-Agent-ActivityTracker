from __future__ import annotations
import math

from typing import Any, Dict

class SandboxErr(Exception):
    pass

def _build_restricted_globals(extra: Dict[str, Any]| None = None) -> Dict[str, Any]:
    safe_builtins = {
        "len": len,
        "sum": sum,
        "min": min,
        "max": max,
        "range": range,
        "abs": abs,
        "round": round
    }

    globals_dict: Dict[str, Any] = {
        "__builtins__": safe_builtins,
        "math": math
    }

    if extra:
        globals_dict.update(extra)
    return globals_dict

def run_untrusted_llm(code: str, context: Dict[str, Any]) -> Dict[str, Any]:
    restricted_globals = _build_restricted_globals()
    locals_dict, dict(context) #type: ignore

    try:
        exec(code, restricted_globals, locals_dict) # type: ignore
    except Exception as exc:
        raise SandboxErr(f"Error executing untrusted LLM: {exc}") from exc
    return locals_dict # type: ignore

def run_untrusted_slm(code: str, context: Dict[str, Any]) -> Dict[str, Any]:
    restricted_globals = _build_restricted_globals()
    locals_dict, dict(context) #type: ignore

    try:
        exec(code, restricted_globals, locals_dict) # type: ignore
    except Exception as exc:
        raise SandboxErr(f"Error executing untrusted SLM: {exc}") from exc
    return locals_dict # type: ignore
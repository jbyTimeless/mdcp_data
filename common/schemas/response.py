from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class ResponseStructure(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: Optional[T] = None

class ErrorResponse(ResponseStructure[Any]):
    code: int = 500
    msg: str = "error"
    data: Any = None

def success(data: Any = None, msg: str = "success", code: int = 200) -> ResponseStructure[Any]:
    return ResponseStructure(code=code, msg=msg, data=data)

def error(msg: str = "error", code: int = 500, data: Any = None) -> ResponseStructure[Any]:
    return ResponseStructure(code=code, msg=msg, data=data)

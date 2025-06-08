import typing
from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse


class AbstractCRUDResponse:
    status_code: typing.ClassVar[int] = None
    _description: typing.ClassVar[str] = None
    _message: typing.ClassVar[str] = None
    _detail: typing.ClassVar[dict[str, Any]] = None
    _headers: typing.ClassVar[dict[str, Any]] = None

    @classmethod
    def response(
        cls: type["AbstractCRUDResponse"],
        _message: str | None = None,
        *,
        _detail: str | dict | None = None,
        _headers: dict[str, str] | None = None,
    ) -> JSONResponse:
        headers = cls._headers or {}
        if _headers is not None:
            headers.update(_headers)
        return JSONResponse(
            content=cls._response_model(_message, _detail=_detail),
            status_code=cls.status_code,
            headers=headers,
        )

    @classmethod
    def docs(
        cls: type["AbstractCRUDResponse"],
        _message: str | None = None,
        *,
        _detail: str | dict | None = None,
        _description: str | None = None,
    ) -> dict[int | str, dict[str, Any]] | None:
        return {
            cls.status_code: {
                "description": _description or cls._description,
                "content": {
                    "application/json": {
                        "example": cls._response_model(_message, _detail=_detail),
                    },
                },
            },
        }

    @classmethod
    def _response_model(
        cls: type["AbstractCRUDResponse"],
        _message: str | None = None,
        *,
        _detail: str | dict | None = None,
    ) -> dict[str, Any]:
        response = {
            "message": _message or cls._message or "OK",
        }
        if _detail is not None or cls._detail is not None:
            response["detail"] = _detail or cls._detail
        return response


class ObjectCreatedResponse(AbstractCRUDResponse):
    status_code: typing.ClassVar = status.HTTP_201_CREATED
    _description: typing.ClassVar = (
        "Returns the ID of the created object as a guarantee of endpoint provisioning."
    )
    _message: typing.ClassVar = "Successfully created"
    _detail: typing.ClassVar = {"id": 0}
    _headers: typing.ClassVar = {"X-Action-Performed": "create"}


class ObjectUpdatedResponse(AbstractCRUDResponse):
    status_code: typing.ClassVar = status.HTTP_200_OK
    _description: typing.ClassVar = "Successfully updated"
    _message: typing.ClassVar = "Successfully updated"
    _headers: typing.ClassVar = {"X-Action-Performed": "update"}


class ObjectDeletedResponse(AbstractCRUDResponse):
    status_code: typing.ClassVar = status.HTTP_200_OK
    _description: typing.ClassVar = "Successfully deleted"
    _message: typing.ClassVar = "Successfully deleted"
    _headers: typing.ClassVar = {"X-Action-Performed": "delete"}

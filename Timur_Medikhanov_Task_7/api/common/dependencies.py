from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, Response
from typing import Callable, TypeVar, Type

TRepo = TypeVar("TRepo")
TService = TypeVar("TService")


async def get_service(
    session: AsyncSession,
    repository: Type[TRepo],
    service_cls: Type[TService],
) -> TService:
    repo = repository(session)
    service = service_cls(repo)
    return service


def make_access_token_dependency(
    get_service_dep: Callable[..., TService],
) -> Callable[..., dict]:
    """
    Возвращает функцию-зависимость, которая принимает Request, Response и
    «сервис», полученный из get_service_dep, и возвращает payload.
    """

    async def _getter(
        request: Request,
        response: Response,
        service: TService = Depends(get_service_dep),
    ) -> dict:

        return await service.access_token_payload(request, response)

    return _getter

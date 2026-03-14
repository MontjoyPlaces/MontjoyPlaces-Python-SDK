from __future__ import annotations

class MontjoyPlacesError(Exception):
    def __init__(self, message: str, *, status: int | None = None, body: object | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body

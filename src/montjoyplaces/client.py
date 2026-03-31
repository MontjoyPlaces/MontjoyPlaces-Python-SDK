from __future__ import annotations

import json
from typing import Any
from urllib import error, parse, request

from .exceptions import MontjoyPlacesError
from .models import (
    BillingPlansResponse,
    CategoryChildrenResponse,
    CategoryResponse,
    CategorySearchResponse,
    CustomPlaceCreateRequest,
    CustomPlaceHideRequest,
    CustomPlaceSingleResponse,
    CustomPlaceUpdateRequest,
    CustomPlacesListResponse,
    DeleteResponse,
    GetCategoryChildrenParams,
    GroupCreateRequest,
    GroupDeleteResponse,
    GroupSingleResponse,
    GroupUpdateRequest,
    GroupsListResponse,
    ListCustomPlacesParams,
    ListGroupsParams,
    LookupNearestUsCitiesParams,
    OverrideRequest,
    OverrideResponse,
    PlanCatalogEntry,
    PlaceSingleResponse,
    SearchCategoriesParams,
    SearchPlacesParams,
    SearchResponse,
    SearchUsCitiesParams,
    UsCityListResponse,
    UsCitySearchResponse,
    UsZipLookupResponse,
    WhoAmIResponse,
    from_payload,
    model_to_dict,
    parse_category_lookup_row,
    parse_custom_place,
    parse_group,
    parse_place,
    parse_search_resolved,
    parse_search_row,
    parse_us_city,
)

DEFAULT_BASE_URL = "https://api.montjoyplaces.com"


class MontjoyPlaces:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        opener: request.OpenerDirector | None = None,
        timeout: float = 30.0,
    ) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._api_key = api_key
        self._opener = opener or request.build_opener()

    def close(self) -> None:
        return None

    def __enter__(self) -> "MontjoyPlaces":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def list_billing_plans(self) -> BillingPlansResponse:
        payload = self._request("GET", "/billing/plans")
        payload["plans"] = [from_payload(plan, PlanCatalogEntry) for plan in payload["plans"]]
        return from_payload(payload, BillingPlansResponse)

    def who_am_i(self) -> WhoAmIResponse:
        return from_payload(self._request("GET", "/v1/whoami"), WhoAmIResponse)

    def list_groups(self, params: ListGroupsParams | dict[str, Any] | None = None) -> GroupsListResponse:
        payload = self._request("GET", "/v1/groups", query=params)
        payload["rows"] = [parse_group(row) for row in payload["rows"]]
        return from_payload(payload, GroupsListResponse)

    def create_group(self, body: GroupCreateRequest | dict[str, Any]) -> GroupSingleResponse:
        payload = self._request("POST", "/v1/groups", body=body)
        payload["row"] = parse_group(payload["row"])
        return from_payload(payload, GroupSingleResponse)

    def update_group(self, group_id: str, body: GroupUpdateRequest | dict[str, Any]) -> GroupSingleResponse:
        payload = self._request("PUT", f"/v1/groups/{parse.quote(group_id, safe='')}", body=body)
        payload["row"] = parse_group(payload["row"])
        return from_payload(payload, GroupSingleResponse)

    def delete_group(self, group_id: str) -> GroupDeleteResponse:
        return from_payload(self._request("DELETE", f"/v1/groups/{parse.quote(group_id, safe='')}"), GroupDeleteResponse)

    def list_custom_places(self, params: ListCustomPlacesParams | dict[str, Any] | None = None) -> CustomPlacesListResponse:
        payload = self._request("GET", "/v1/custom-places", query=params)
        payload["rows"] = [parse_custom_place(row) for row in payload["rows"]]
        return from_payload(payload, CustomPlacesListResponse)

    def create_custom_place(self, body: CustomPlaceCreateRequest | dict[str, Any]) -> CustomPlaceSingleResponse:
        payload = self._request("POST", "/v1/custom-places", body=body)
        payload["row"] = parse_custom_place(payload["row"])
        return from_payload(payload, CustomPlaceSingleResponse)

    def get_custom_place(self, custom_place_id: str) -> CustomPlaceSingleResponse:
        payload = self._request("GET", f"/v1/custom-places/{parse.quote(custom_place_id, safe='')}")
        payload["row"] = parse_custom_place(payload["row"])
        return from_payload(payload, CustomPlaceSingleResponse)

    def update_custom_place(self, custom_place_id: str, body: CustomPlaceUpdateRequest | dict[str, Any]) -> CustomPlaceSingleResponse:
        payload = self._request("PUT", f"/v1/custom-places/{parse.quote(custom_place_id, safe='')}", body=body)
        payload["row"] = parse_custom_place(payload["row"])
        return from_payload(payload, CustomPlaceSingleResponse)

    def delete_custom_place(self, custom_place_id: str) -> DeleteResponse:
        return from_payload(self._request("DELETE", f"/v1/custom-places/{parse.quote(custom_place_id, safe='')}"), DeleteResponse)

    def hide_custom_place(self, custom_place_id: str, body: CustomPlaceHideRequest | dict[str, Any]) -> CustomPlaceSingleResponse:
        payload = self._request("POST", f"/v1/custom-places/{parse.quote(custom_place_id, safe='')}/hide", body=body)
        payload["row"] = parse_custom_place(payload["row"])
        return from_payload(payload, CustomPlaceSingleResponse)

    def get_place(self, place_id: str) -> PlaceSingleResponse:
        payload = self._request("GET", f"/v1/places/{parse.quote(place_id, safe='')}")
        if payload["row"] is not None:
            payload["row"] = parse_place(payload["row"])
        return from_payload(payload, PlaceSingleResponse)

    def override_place(self, fsq_place_id: str, body: OverrideRequest | dict[str, Any]) -> OverrideResponse:
        payload = self._request("PUT", f"/v1/places/{parse.quote(fsq_place_id, safe='')}/override", body=body)
        payload["row"] = parse_custom_place(payload["row"])
        return from_payload(payload, OverrideResponse)

    def lookup_nearest_us_cities(self, params: LookupNearestUsCitiesParams | dict[str, Any]) -> UsCityListResponse:
        payload = self._request("GET", "/v1/lookup/us-cities/nearest", query=params)
        payload["rows"] = [parse_us_city(row) for row in payload["rows"]]
        return from_payload(payload, UsCityListResponse)

    def search_us_cities(self, params: SearchUsCitiesParams | dict[str, Any]) -> UsCitySearchResponse:
        payload = self._request("GET", "/v1/lookup/us-cities/search", query=params)
        payload["rows"] = [parse_us_city(row) for row in payload["rows"]]
        return from_payload(payload, UsCitySearchResponse)

    def lookup_us_zipcode(self, zipcode: str) -> UsZipLookupResponse:
        payload = self._request("GET", f"/v1/lookup/us-cities/zip/{parse.quote(zipcode, safe='')}")
        payload["rows"] = [parse_us_city(row) for row in payload["rows"]]
        return from_payload(payload, UsZipLookupResponse)

    def search_categories(self, params: SearchCategoriesParams | dict[str, Any] | None = None) -> CategorySearchResponse:
        payload = self._request("GET", "/v1/lookup/categories/search", query=params)
        payload["rows"] = [parse_category_lookup_row(row) for row in payload["rows"]]
        return from_payload(payload, CategorySearchResponse)

    def get_category(self, category_id: str) -> CategoryResponse:
        payload = self._request("GET", f"/v1/lookup/categories/{parse.quote(category_id, safe='')}")
        payload["row"] = parse_category_lookup_row(payload["row"])
        return from_payload(payload, CategoryResponse)

    def get_category_children(
        self, category_id: str, params: GetCategoryChildrenParams | dict[str, Any] | None = None
    ) -> CategoryChildrenResponse:
        payload = self._request("GET", f"/v1/lookup/categories/{parse.quote(category_id, safe='')}/children", query=params)
        payload["parent"] = parse_category_lookup_row(payload["parent"])
        payload["rows"] = [parse_category_lookup_row(row) for row in payload["rows"]]
        return from_payload(payload, CategoryChildrenResponse)

    def search_places(self, params: SearchPlacesParams | dict[str, Any]) -> SearchResponse:
        payload = self._request("GET", "/v1/search", query=params)
        payload["resolved"] = parse_search_resolved(payload["resolved"])
        payload["rows"] = [parse_search_row(row) for row in payload["rows"]]
        return from_payload(payload, SearchResponse)

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: Any = None,
        body: Any = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        query_params = _build_query(query)
        if query_params:
            url = f"{url}?{parse.urlencode(query_params)}"

        payload_bytes = None
        headers = {
            "Accept": "application/json",
            "X-API-Key": self._api_key,
        }
        if body is not None:
            payload_bytes = json.dumps(model_to_dict(body)).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = request.Request(
            url=url,
            data=payload_bytes,
            headers=headers,
            method=method,
        )
        try:
            with self._opener.open(req, timeout=self.timeout) as response:
                return _parse_response(response.read())
        except error.HTTPError as exc:
            payload = _parse_response(exc.read())
            message = payload.get("error") if isinstance(payload, dict) and isinstance(payload.get("error"), str) else f"Request failed with status {exc.code}"
            raise MontjoyPlacesError(message, status=exc.code, body=payload) from exc
        except error.URLError as exc:
            raise MontjoyPlacesError(f"Failed to call Montjoy Places API: {exc.reason}") from exc


def _build_query(query: Any) -> dict[str, str] | None:
    if query is None:
        return None

    source = model_to_dict(query)
    result: dict[str, str] = {}
    for key, value in source.items():
        if value is None:
            continue
        if key == "includeHidden" and isinstance(value, bool):
            result[key] = "1" if value else "0"
            continue
        if isinstance(value, bool):
            result[key] = "true" if value else "false"
            continue
        result[key] = str(value)
    return result


def _parse_response(response_body: bytes) -> Any:
    if not response_body:
        return None
    text = response_body.decode("utf-8")
    try:
        return json.loads(text)
    except ValueError:
        return text

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from typing import Any, Literal, TypeVar, Union, get_args, get_origin

try:
    from types import UnionType as _UnionType
except ImportError:  # pragma: no cover
    _UnionType = None

JsonPrimitive = Union[str, int, float, bool, None]
JsonValue = Union[JsonPrimitive, list["JsonValue"], dict[str, "JsonValue"]]


def _parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


@dataclass
class PlanCatalogEntry:
    code: str
    label: str
    monthlyRequests: int | None
    maxTenants: int | None
    maxApps: int | None
    maxApiKeys: int | None
    overageAllowed: bool
    overageBlockRequests: int
    overageBlockPriceCents: int
    maxUsageMultiplier: int | None
    hardCapByDefault: bool


@dataclass
class BillingPlansResponse:
    ok: bool
    plans: list[PlanCatalogEntry]


@dataclass
class WhoAmIResponse:
    ok: bool
    apiKeyId: str
    tenantId: str
    appId: str
    keyName: str
    prefix: str


@dataclass
class Place:
    fsq_place_id: str
    place_source: Literal["fsq", "address"]
    name: str
    latitude: float
    longitude: float
    address: str | None = None
    locality: str | None = None
    region: str | None = None
    postcode: str | None = None
    country: str | None = None
    website: str | None = None
    tel: str | None = None
    email: str | None = None
    formatted_address: str | None = None
    geocode_provider: str | None = None
    geocode_confidence: float | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class PlaceSingleResponse:
    ok: bool
    row: Place | None


@dataclass
class Group:
    group_id: str
    tenant_id: str
    name: str
    created_at: datetime


@dataclass
class GroupsListResponse:
    ok: bool
    rows: list[Group]


@dataclass
class GroupSingleResponse:
    ok: bool
    row: Group


@dataclass
class GroupDeleteResponse:
    ok: bool
    deleted: bool


@dataclass
class DeleteResponse:
    ok: bool
    deleted: bool | None = None


@dataclass
class CustomPlace:
    custom_place_id: str
    tenant_id: str
    source: Literal["tenant", "user"]
    name: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime
    app_id: str | None = None
    group_id: str | None = None
    owner_user_id: str | None = None
    fsq_place_id: str | None = None
    address: str | None = None
    locality: str | None = None
    region: str | None = None
    postcode: str | None = None
    country: str | None = None
    website: str | None = None
    tel: str | None = None
    email: str | None = None
    tags: JsonValue | None = None
    meta: JsonValue | None = None
    dist_m: float | None = None


@dataclass
class CustomPlacesListResponse:
    ok: bool
    rows: list[CustomPlace]
    nextCursor: str | None


@dataclass
class CustomPlaceSingleResponse:
    ok: bool
    row: CustomPlace


@dataclass
class SearchRowGlobal:
    fsq_place_id: str
    name: str
    latitude: float
    longitude: float
    dist_m: float
    _source: Literal["global"]
    category_name: str | None = None


@dataclass
class SearchRowCustom(CustomPlace):
    _source: Literal["custom"] = "custom"


SearchRow = Union[SearchRowGlobal, SearchRowCustom]


@dataclass
class SearchResolvedCenter:
    lat: float
    lon: float
    source: Literal["request", "locality", "address_cache", "address_geocode"]
    kind: str
    label: str


@dataclass
class SearchResolved:
    mode: Literal["address", "nearby", "typeahead", "category"]
    reason: str | None = None
    prefix: str | None = None
    categoryName: str | None = None
    groupId: str | None = None
    customOnly: bool | None = None
    localityText: str | None = None
    addressQuery: str | None = None
    addressPlaceId: str | None = None
    formattedAddress: str | None = None
    geocodeProvider: str | None = None
    geocodeCacheHit: bool | None = None
    addressRadiusMeters: float | None = None
    addressCandidateCount: int | None = None
    addressFilteredCount: int | None = None
    center: SearchResolvedCenter | None = None


@dataclass
class SearchResponse:
    ok: bool
    mode: Literal["search"]
    q: str
    resolved: SearchResolved
    count: int
    rows: list[SearchRow]


@dataclass
class UsCity:
    id: int
    city: str
    state_id: str
    state_name: str
    zipcode: str
    lat: float
    lon: float
    dist_m: float | None = None


@dataclass
class UsCityListResponse:
    ok: bool
    count: int
    rows: list[UsCity]


@dataclass
class UsCitySearchResponse:
    ok: bool
    q: str
    state: str | None
    count: int
    rows: list[UsCity]


@dataclass
class UsZipLookupResponse:
    ok: bool
    zipcode: str
    count: int
    rows: list[UsCity]


@dataclass
class CategoryHierarchyNode:
    level: int
    category_id: str | None
    category_name: str | None


@dataclass
class CategoryLookupRow:
    category_id: str
    hierarchy: list[CategoryHierarchyNode]
    category_name: str | None = None
    category_label: str | None = None
    category_level: int | None = None


@dataclass
class CategorySearchResponse:
    ok: bool
    q: str | None
    level: int | None
    parentId: str | None
    count: int
    rows: list[CategoryLookupRow]


@dataclass
class CategoryResponse:
    ok: bool
    row: CategoryLookupRow


@dataclass
class CategoryChildrenResponse:
    ok: bool
    parent: CategoryLookupRow
    count: int
    rows: list[CategoryLookupRow]


@dataclass
class OverrideResponse:
    ok: bool
    action: Literal["created", "updated"]
    row: CustomPlace


@dataclass
class GroupCreateRequest:
    name: str


@dataclass
class GroupUpdateRequest:
    name: str


@dataclass
class ListGroupsParams:
    limit: int | None = None


@dataclass
class CustomPlaceCreateRequest:
    name: str
    latitude: float
    longitude: float
    groupId: str | None = None
    source: Literal["tenant", "user"] | None = None
    ownerUserId: str | None = None
    fsqPlaceId: str | None = None
    address: str | None = None
    locality: str | None = None
    region: str | None = None
    postcode: str | None = None
    country: str | None = None
    website: str | None = None
    tel: str | None = None
    email: str | None = None
    tags: JsonValue | None = None
    meta: JsonValue | None = None


@dataclass
class CustomPlaceUpdateRequest:
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None
    locality: str | None = None
    region: str | None = None
    postcode: str | None = None
    country: str | None = None
    website: str | None = None
    tel: str | None = None
    email: str | None = None
    tags: JsonValue | None = None
    meta: JsonValue | None = None


@dataclass
class CustomPlaceHideRequest:
    hidden: bool


@dataclass
class ListCustomPlacesParams:
    groupId: str | None = None
    limit: int | None = None
    cursor: str | None = None
    includeHidden: bool | Literal["0", "1"] | None = None


@dataclass
class OverrideRequest:
    groupId: str | None = None
    hide: bool | None = None
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None
    locality: str | None = None
    region: str | None = None
    postcode: str | None = None
    country: str | None = None
    website: str | None = None
    tel: str | None = None
    email: str | None = None
    tags: JsonValue | None = None
    meta: JsonValue | None = None


@dataclass
class LookupNearestUsCitiesParams:
    lat: float
    lon: float
    limit: int | None = None


@dataclass
class SearchUsCitiesParams:
    q: str
    state: str | None = None
    limit: int | None = None


@dataclass
class SearchCategoriesParams:
    q: str | None = None
    level: int | None = None
    parentId: str | None = None
    limit: int | None = None


@dataclass
class GetCategoryChildrenParams:
    limit: int | None = None


@dataclass
class SearchPlacesParams:
    q: str
    lat: float | None = None
    lon: float | None = None
    radiusMeters: float | None = None
    limit: int | None = None
    excludeCategoryMatch: bool | None = None
    forceTypeahead: bool | None = None
    customOnly: bool | None = None
    onlyCustom: bool | None = None
    isAddress: bool | None = None
    groupId: str | None = None


def model_to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {
            field.name: model_to_dict(getattr(value, field.name))
            for field in fields(value)
            if getattr(value, field.name) is not None
        }
    if isinstance(value, list):
        return [model_to_dict(item) for item in value]
    if isinstance(value, tuple):
        return [model_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: model_to_dict(item) for key, item in value.items() if item is not None}
    return value


T = TypeVar("T")
NoneType = type(None)


def from_payload(payload: Any, model: type[T]) -> T:
    if payload is None:
        return payload
    return _coerce(payload, model)


def parse_group(payload: dict[str, Any]) -> Group:
    data = dict(payload)
    data["created_at"] = _parse_datetime(data["created_at"])
    return from_payload(data, Group)


def parse_place(payload: dict[str, Any]) -> Place:
    data = dict(payload)
    data["created_at"] = _parse_datetime(data.get("created_at"))
    data["updated_at"] = _parse_datetime(data.get("updated_at"))
    return from_payload(data, Place)


def parse_custom_place(payload: dict[str, Any]) -> CustomPlace:
    data = dict(payload)
    data["created_at"] = _parse_datetime(data["created_at"])
    data["updated_at"] = _parse_datetime(data["updated_at"])
    return from_payload(data, CustomPlace)


def parse_search_row(payload: dict[str, Any]) -> SearchRow:
    if payload.get("_source") == "custom":
        data = dict(payload)
        data["created_at"] = _parse_datetime(data["created_at"])
        data["updated_at"] = _parse_datetime(data["updated_at"])
        return from_payload(data, SearchRowCustom)
    return from_payload(payload, SearchRowGlobal)


def parse_search_resolved(payload: dict[str, Any]) -> SearchResolved:
    data = dict(payload)
    center = data.get("center")
    if center is not None:
        data["center"] = from_payload(center, SearchResolvedCenter)
    return from_payload(data, SearchResolved)


def parse_us_city(payload: dict[str, Any]) -> UsCity:
    return from_payload(payload, UsCity)


def parse_category_lookup_row(payload: dict[str, Any]) -> CategoryLookupRow:
    data = dict(payload)
    data["hierarchy"] = [from_payload(item, CategoryHierarchyNode) for item in data.get("hierarchy", [])]
    return from_payload(data, CategoryLookupRow)


def _coerce(value: Any, annotation: Any) -> Any:
    origin = get_origin(annotation)
    if annotation in (Any, JsonValue, JsonPrimitive) or origin is Literal:
        return value
    if isinstance(value, annotation) if isinstance(annotation, type) else False:
        return value
    if origin is list:
        inner = get_args(annotation)[0]
        return [_coerce(item, inner) for item in value]
    if origin is dict:
        key_type, value_type = get_args(annotation)
        return {_coerce(k, key_type): _coerce(v, value_type) for k, v in value.items()}
    if origin is Union or (_UnionType is not None and origin is _UnionType):
        args = [arg for arg in get_args(annotation) if arg is not NoneType]
        if value is None:
            return None
        for arg in args:
            if is_dataclass(arg) and is_dataclass(value) and isinstance(value, arg):
                return value
        if len(args) == 1:
            return _coerce(value, args[0])
        return value
    if is_dataclass(annotation):
        return annotation(**{field.name: value[field.name] for field in fields(annotation) if field.name in value})
    return value

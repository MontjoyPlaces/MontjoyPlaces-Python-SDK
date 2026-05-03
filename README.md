# MontjoyPlaces Python SDK

Official Python SDK for the Montjoy Places API.

- Homepage: https://montjoyplaces.com
- API Base URL: `https://api.montjoyplaces.com`
- Python Version: 3.9+
- License: MIT
- Support: paul@montjoyapp.com

## Installation

Install from a package index:

```bash
pip install MontjoyPlaces
```

Install from source:

```bash
pip install .
```

## Authentication

Create a client with your Montjoy Places API key:

```python
from montjoyplaces import MontjoyPlaces

client = MontjoyPlaces("your-api-key")
```

The SDK sends the API key using the `X-API-Key` header.

## Quick Start

```python
from montjoyplaces import MontjoyPlaces, SearchPlacesParams

client = MontjoyPlaces("your-api-key")

try:
    who_am_i = client.who_am_i()
    print("tenant=", who_am_i.tenantId)

    search = client.search_places(
        SearchPlacesParams(q="coffee near Boston MA", limit=3)
    )
    print("results=", search.count)
    print(search.rows)
finally:
    client.close()
```

## Client Construction

The SDK supports the default API base URL:

```python
from montjoyplaces import MontjoyPlaces

client = MontjoyPlaces("your-api-key")
```

You can also point at a different environment:

```python
client = MontjoyPlaces(
    api_key="your-api-key",
    base_url="https://api.montjoyplaces.com",
)
```

## Common Examples

### Check API Identity

```python
who_am_i = client.who_am_i()
print(who_am_i)
```

### List Groups

```python
from montjoyplaces import ListGroupsParams

groups = client.list_groups(ListGroupsParams(limit=10))
```

### Create a Group

```python
from montjoyplaces import GroupCreateRequest

created_group = client.create_group(GroupCreateRequest(name="Favorites"))
```

### Search Places

```python
from montjoyplaces import SearchPlacesParams

search = client.search_places(
    SearchPlacesParams(
        q="pizza near New York NY",
        limit=5,
        radiusMeters=5000,
    )
)
```

### Create a Custom Place

```python
from montjoyplaces import CustomPlaceCreateRequest

created = client.create_custom_place(
    CustomPlaceCreateRequest(
        groupId="group_123",
        name="My Custom Place",
        latitude=42.3601,
        longitude=-71.0589,
        address="1 Beacon St",
        locality="Boston",
        region="MA",
        postcode="02108",
        country="US",
        website="https://example.com",
        tags=["favorite", "team"],
        meta={"source": "python-sdk"},
    )
)
```

### Update a Custom Place

```python
from montjoyplaces import CustomPlaceUpdateRequest

updated = client.update_custom_place(
    "custom_place_id",
    CustomPlaceUpdateRequest(
        name="Updated Place Name",
        website="https://example.com/updated",
    ),
)
```

### Hide or Unhide a Custom Place

```python
from montjoyplaces import CustomPlaceHideRequest

client.hide_custom_place("custom_place_id", CustomPlaceHideRequest(hidden=True))
client.hide_custom_place("custom_place_id", CustomPlaceHideRequest(hidden=False))
```

### Delete a Custom Place

```python
deleted = client.delete_custom_place("custom_place_id")
```

### Export and Import Custom Places

```python
from montjoyplaces import CustomPlaceImportRow, CustomPlacesImportRequest, ExportCustomPlacesParams

exported = client.export_custom_places(
    ExportCustomPlacesParams(groupId="group_123", includeHidden=True)
)

imported = client.import_custom_places(
    CustomPlacesImportRequest(
        mode="upsert",
        rows=[
            CustomPlaceImportRow(
                custom_place_id=row.custom_place_id,
                group_id=row.group_id,
                name=row.name,
                latitude=row.latitude,
                longitude=row.longitude,
            )
            for row in exported.rows
        ],
    )
)
```

### Override a Place

```python
from montjoyplaces import OverrideRequest

response = client.override_place(
    "fsq_place_id",
    OverrideRequest(
        groupId="group_123",
        name="My Overridden Name",
        hide=False,
    ),
)
```

### Lookup US Cities

```python
from montjoyplaces import LookupNearestUsCitiesParams, SearchUsCitiesParams

nearest = client.lookup_nearest_us_cities(
    LookupNearestUsCitiesParams(lat=42.3601, lon=-71.0589, limit=5)
)

matches = client.search_us_cities(
    SearchUsCitiesParams(q="Boston", state="MA", limit=5)
)

zip_lookup = client.lookup_us_zipcode("02108")
```

### Lookup Categories

```python
from montjoyplaces import GetCategoryChildrenParams, SearchCategoriesParams

categories = client.search_categories(
    SearchCategoriesParams(q="coffee", limit=10)
)

category = client.get_category("13032")

children = client.get_category_children(
    "13032",
    GetCategoryChildrenParams(limit=20),
)
```

## Supported Operations

The SDK currently includes methods for:

- API identity: `who_am_i`
- Groups: `list_groups`, `create_group`, `update_group`, `delete_group`
- Custom places: `list_custom_places`, `export_custom_places`, `import_custom_places`, `create_custom_place`, `get_custom_place`, `update_custom_place`, `delete_custom_place`, `hide_custom_place`
- Place overrides: `override_place`
- US city lookup: `lookup_nearest_us_cities`, `search_us_cities`, `lookup_us_zipcode`
- Category lookup: `search_categories`, `get_category`, `get_category_children`
- Search: `search_places`

## Error Handling

API failures raise `MontjoyPlacesError`.

```python
from montjoyplaces import MontjoyPlaces, MontjoyPlacesError

try:
    client = MontjoyPlaces("your-api-key")
    client.who_am_i()
except MontjoyPlacesError as exc:
    print("status:", exc.status)
    print("message:", exc)
    print("body:", exc.body)
```

## Samples

Sample programs are included in [`samples/`](./samples):

- `basic.py` shows authentication, group listing, and search
- `integration.py` exercises create, update, hide, list, export, import, and cleanup flows for groups and custom places

Run a sample with an API key set in the environment:

```bash
PYTHONPATH=src MONTJOY_PLACES_API_KEY=your-api-key python3 samples/basic.py
PYTHONPATH=src MONTJOY_PLACES_API_KEY=your-api-key python3 samples/integration.py
```

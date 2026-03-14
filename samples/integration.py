import os
import time

from montjoy_places import (
    CustomPlaceCreateRequest,
    CustomPlaceHideRequest,
    CustomPlaceUpdateRequest,
    GroupCreateRequest,
    ListCustomPlacesParams,
    MontjoyPlaces,
)


def main() -> None:
    api_key = os.environ.get("MONTJOY_PLACES_API_KEY")
    if not api_key:
        raise RuntimeError("Set MONTJOY_PLACES_API_KEY before running the sample.")

    suffix = int(time.time() * 1000)
    group_name = f"sdk-python-{suffix}"

    group_id: str | None = None
    custom_place_id: str | None = None

    with MontjoyPlaces(api_key) as client:
        try:
            created_group = client.create_group(GroupCreateRequest(name=group_name))
            group_id = created_group.row.group_id
            print("created group:", created_group.row)

            created_place = client.create_custom_place(
                CustomPlaceCreateRequest(
                    groupId=group_id,
                    name=f"SDK Python Test Place {suffix}",
                    latitude=42.3601,
                    longitude=-71.0589,
                    address="1 Beacon St",
                    locality="Boston",
                    region="MA",
                    postcode="02108",
                    country="US",
                    website="https://example.com/python",
                    tags=["sdk", "python"],
                    meta={"source": "integration-sample"},
                )
            )
            custom_place_id = created_place.row.custom_place_id
            print("created custom place:", created_place.row)

            fetched_place = client.get_custom_place(custom_place_id)
            print("fetched custom place:", fetched_place.row)

            updated_place = client.update_custom_place(
                custom_place_id,
                CustomPlaceUpdateRequest(
                    name=f"SDK Python Updated Place {suffix}",
                    website="https://example.com/python-updated",
                    meta={"source": "integration-sample", "updated": True},
                ),
            )
            print("updated custom place:", updated_place.row)

            hidden_place = client.hide_custom_place(custom_place_id, CustomPlaceHideRequest(hidden=True))
            print("hidden custom place:", hidden_place.row)

            unhidden_place = client.hide_custom_place(custom_place_id, CustomPlaceHideRequest(hidden=False))
            print("unhidden custom place:", unhidden_place.row)

            custom_places = client.list_custom_places(
                ListCustomPlacesParams(groupId=group_id, limit=10, includeHidden=True)
            )
            print("group custom places:", [row.name for row in custom_places.rows])
        finally:
            if custom_place_id:
                try:
                    deleted_place = client.delete_custom_place(custom_place_id)
                    print("deleted custom place:", deleted_place)
                except Exception as exc:  # pragma: no cover
                    print("cleanup failed for custom place:", exc)

            if group_id:
                try:
                    deleted_group = client.delete_group(group_id)
                    print("deleted group:", deleted_group)
                except Exception as exc:  # pragma: no cover
                    print("cleanup failed for group:", exc)


if __name__ == "__main__":
    main()

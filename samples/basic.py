from montjoy_places import ListGroupsParams, MontjoyPlaces, SearchPlacesParams

import os


def main() -> None:
    api_key = os.environ.get("MONTJOY_PLACES_API_KEY")
    if not api_key:
        raise RuntimeError("Set MONTJOY_PLACES_API_KEY before running the sample.")

    with MontjoyPlaces(api_key) as client:
        who_am_i = client.who_am_i()
        print("whoami:", who_am_i)

        groups = client.list_groups(ListGroupsParams(limit=5))
        print("groups:", [group.name for group in groups.rows])

        search = client.search_places(SearchPlacesParams(q="coffee near Boston MA", limit=3))
        print("search results:", search.rows)


if __name__ == "__main__":
    main()

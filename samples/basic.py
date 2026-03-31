from montjoyplaces import ListGroupsParams, MontjoyPlaces, SearchPlacesParams, SearchRowGlobal

import os


def main() -> None:
    api_key = os.environ.get("MONTJOY_PLACES_API_KEY")
    if not api_key:
        raise RuntimeError("Set MONTJOY_PLACES_API_KEY before running the sample.")

    with MontjoyPlaces(api_key) as client:
        plans = client.list_billing_plans()
        print("billing plans:", [plan.code for plan in plans.plans])

        who_am_i = client.who_am_i()
        print("whoami:", who_am_i)

        groups = client.list_groups(ListGroupsParams(limit=5))
        print("groups:", [group.name for group in groups.rows])

        search = client.search_places(SearchPlacesParams(q="coffee near Boston MA", limit=3))
        print("search results:", search.rows)

        first_place_id = next((row.fsq_place_id for row in search.rows if isinstance(row, SearchRowGlobal)), None)
        if first_place_id:
            place = client.get_place(first_place_id)
            print("direct place lookup:", place.row)


if __name__ == "__main__":
    main()

class TripMixin:
    def get_trips(
        self,
    ):
        return self.get_objects(
            "Trip",
            self.base_url
            / "list"
            / "trip"
            / "traveler"
            / "true"
            / "past"
            / "true"
            / "include_objects"
            / "false",
            self.base_url
            / "list"
            / "trip"
            / "traveler"
            / "true"
            / "past"
            / "false"
            / "include_objects"
            / "false",
        )

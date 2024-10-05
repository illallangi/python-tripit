class ProfileMixin:
    def get_profiles(
        self,
    ):
        return self.get_objects(
            "Profile",
            self.base_url / "get" / "profile",
        )

from collections.abc import Generator
from typing import Any

from illallangi.tripit.models import Profile


def get_name(
    profile: dict[str, Any],
) -> str:
    return profile["public_display_name"]


def get_company(
    profile: dict[str, Any],
) -> str:
    return profile["company"]


def get_location(
    profile: dict[str, Any],
) -> str:
    return profile["home_city"]


class ProfileMixin:
    def get_profiles(
        self,
        *_: list[Any],
        debug: bool = False,
        progress: bool = True,
    ) -> Generator[Profile, Any, None]:
        for profile in self.get_objects(
            "Profile",
            self.base_url / "get" / "profile",
            progress=progress,
        ):
            # profile_id=UUID(profile["uuid"]),
            yield Profile(
                name=get_name(profile),
                company=get_company(profile),
                location=get_location(profile),
                **(
                    {
                        "api": profile["@api"],
                        "profile": {
                            k: v for k, v in profile.items() if k not in ["@api"]
                        },
                    }
                    if debug
                    else {}
                ),
            )

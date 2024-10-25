from typing import Any

from attrs import define, field, validators


@define(kw_only=True)
class ProfileKey:
    # Natural Keys

    name: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )


@define(kw_only=True)
class Profile(ProfileKey):
    # Fields

    company: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )

    location: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )

    # API Responses

    _api: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
    _profile: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )

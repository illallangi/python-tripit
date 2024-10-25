from attrs import define, field, validators


@define(kw_only=True)
class AirlineKey:
    # Natural Keys

    iata: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[0-9A-Z]{2}$"),
        ],
    )

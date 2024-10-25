from attrs import define, field, validators


@define(kw_only=True)
class AirportKey:
    # Natural Keys

    iata: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[A-Z]{3}$"),
        ],
    )

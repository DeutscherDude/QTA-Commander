from dataclasses import dataclass


@dataclass(frozen=True)
class Icons:
    return_ = ":return"
    remo_st = ":rem_stor"
    drive = ":drive"
    trash = ":trash"
    file = ":file"
    directory = ":dir"
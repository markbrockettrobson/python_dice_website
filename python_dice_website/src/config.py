import os

__ENV_USAGE_LIMITER_MAX_COST = os.environ.get("ENV_USAGE_LIMITER_MAX_COST")
if __ENV_USAGE_LIMITER_MAX_COST is None:
    USAGE_LIMITER_MAX_COST = float("inf")
elif not __ENV_USAGE_LIMITER_MAX_COST.isdigit():
    raise ValueError(
        f"ENV_USAGE_LIMITER_MAX_COST is not an int, was : "
        f"{__ENV_USAGE_LIMITER_MAX_COST} using default"
    )
else:
    USAGE_LIMITER_MAX_COST = int(__ENV_USAGE_LIMITER_MAX_COST)

USAGE_LIMITER_MAX_COST = 10000

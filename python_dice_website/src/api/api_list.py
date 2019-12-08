import typing

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.src.api.privacy_policy_api as privacy_policy_api
import python_dice_website.src.api.roll_api as roll_api

API_LIST: typing.List[i_api_type.IApi] = [
    roll_api.RollApi(),
    privacy_policy_api.PrivacyApi(),
]

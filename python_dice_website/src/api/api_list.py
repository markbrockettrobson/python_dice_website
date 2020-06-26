import typing

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.src.api.at_least_api as at_least_api
import python_dice_website.src.api.at_most_api as at_most_api
import python_dice_website.src.api.average_api as average_api
import python_dice_website.src.api.compare_api as compare_api
import python_dice_website.src.api.compare_at_least_api as compare_at_least_api
import python_dice_website.src.api.compare_at_most_api as compare_at_most_api
import python_dice_website.src.api.compare_histogram_api as compare_histogram_api
import python_dice_website.src.api.histogram_api as histogram_api
import python_dice_website.src.api.privacy_policy_api as privacy_policy_api
import python_dice_website.src.api.roll_api as roll_api
import python_dice_website.src.api.slack_roll_api as slack_roll_api

API_LIST: typing.List[i_api_type.IApi] = [
    roll_api.RollApi(),
    average_api.AverageApi(),
    histogram_api.HistogramApi(),
    compare_api.CompareApi(),
    at_least_api.AtLeastApi(),
    at_most_api.AtMostApi(),
    compare_histogram_api.CompareHistogramApi(),
    compare_at_least_api.CompareAtLeastApi(),
    compare_at_most_api.CompareAtMostApi(),
    privacy_policy_api.PrivacyApi(),
    slack_roll_api.SlackRollApi(),
]

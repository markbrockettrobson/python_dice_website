import typing

import python_dice_website.interface.i_api_list_factory as i_api_list_factory
import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.interface.i_usage_limiter as i_usage_limiter
import python_dice_website.src.api.at_least_api as at_least_api
import python_dice_website.src.api.at_most_api as at_most_api
import python_dice_website.src.api.average_api as average_api
import python_dice_website.src.api.compare_api as compare_api
import python_dice_website.src.api.compare_at_least_api as compare_at_least_api
import python_dice_website.src.api.compare_at_most_api as compare_at_most_api
import python_dice_website.src.api.compare_histogram_api as compare_histogram_api
import python_dice_website.src.api.histogram_api as histogram_api
import python_dice_website.src.api.max_api as max_api
import python_dice_website.src.api.min_api as min_api
import python_dice_website.src.api.privacy_policy_api as privacy_policy_api
import python_dice_website.src.api.roll_api as roll_api
import python_dice_website.src.api.slack_roll_api as slack_roll_api


class ApiListFactory(i_api_list_factory.IApiListFactory):
    @staticmethod
    def build_api_list(
        image_sender: i_pil_image_sender.IPilImageSender,
        python_dice_interpreter_factory: i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
        usage_limiter: i_usage_limiter.IUsageLimiter,
    ) -> typing.List[i_api_type.IApi]:
        return [
            roll_api.RollApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                usage_limiter=usage_limiter,
            ),
            average_api.AverageApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                usage_limiter=usage_limiter,
            ),
            min_api.MinApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                usage_limiter=usage_limiter,
            ),
            max_api.MaxApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                usage_limiter=usage_limiter,
            ),
            histogram_api.HistogramApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            at_least_api.AtLeastApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            at_most_api.AtMostApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            slack_roll_api.SlackRollApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                usage_limiter=usage_limiter,
            ),
            compare_histogram_api.CompareHistogramApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            compare_api.CompareApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            compare_at_least_api.CompareAtLeastApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            compare_at_most_api.CompareAtMostApi(
                python_dice_interpreter_factory=python_dice_interpreter_factory,
                pil_image_sender=image_sender,
                usage_limiter=usage_limiter,
            ),
            privacy_policy_api.PrivacyApi(),
        ]

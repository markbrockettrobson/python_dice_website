import abc
import typing

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory


class IApiListFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def build_api_list(
        image_sender: i_pil_image_sender.IPilImageSender,
        python_dice_interpreter_factory: i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
    ) -> typing.List[i_api_type.IApi]:
        pass

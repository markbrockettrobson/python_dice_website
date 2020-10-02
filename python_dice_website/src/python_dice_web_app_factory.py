import os
import typing

import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.src.api.helpers.pil_image_sender as pil_image_sender
import python_dice_website.src.api_list_factory as api_list_factory
import python_dice_website.src.python_dice_interpreter_factory as python_dice_interpreter_factory
import python_dice_website.src.python_dice_web_app as python_dice_web_app


class PythonDiceWebAppFactory:
    @staticmethod
    def create_app() -> python_dice_web_app.PythonDiceWebApp:
        api_list = api_list_factory.ApiListFactory().build_api_list(
            image_sender=pil_image_sender.PilImageSender(),
            python_dice_interpreter_factory=python_dice_interpreter_factory.PythonDiceInterpreterFactory(),
        )

        return python_dice_web_app.PythonDiceWebApp(
            api_list=api_list, https_server=bool(os.environ.get("HTTPS_SERVER", False))
        )

    @staticmethod
    def create_local_app() -> python_dice_web_app.PythonDiceWebApp:
        api_list = api_list_factory.ApiListFactory().build_api_list(
            image_sender=pil_image_sender.PilImageSender(),
            python_dice_interpreter_factory=python_dice_interpreter_factory.PythonDiceInterpreterFactory(),
        )

        return python_dice_web_app.PythonDiceWebApp(
            api_list=api_list, host="localhost", debug=True, port=5000
        )

    @staticmethod
    def create_test_app(
        image_sender: typing.Optional[i_pil_image_sender.IPilImageSender] = None,
        interpreter_factory: typing.Optional[
            i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory
        ] = None,
    ):
        if not image_sender:
            image_sender = pil_image_sender.PilImageSender()
        if not interpreter_factory:
            interpreter_factory = (
                python_dice_interpreter_factory.PythonDiceInterpreterFactory(),
            )

        api_list = api_list_factory.ApiListFactory().build_api_list(
            image_sender=image_sender,
            python_dice_interpreter_factory=interpreter_factory,
        )

        return python_dice_web_app.PythonDiceWebApp(
            api_list=api_list, debug=True, logging=False
        )

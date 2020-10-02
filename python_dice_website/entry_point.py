import python_dice_website.src.python_dice_web_app_factory as python_dice_web_app_factory

if __name__ == "__main__":
    python_dice_web_app_factory.PythonDiceWebAppFactory.create_local_app().run()
else:
    APP = python_dice_web_app_factory.PythonDiceWebAppFactory.create_app().get_app()

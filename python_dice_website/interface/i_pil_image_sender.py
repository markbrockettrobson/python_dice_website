import abc

import PIL.Image as Image


class IPilImageSender(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def send_image(pil_image: Image):
        pass

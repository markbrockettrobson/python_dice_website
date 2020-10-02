import io

import flask
import PIL.Image as Image

import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender


class PilImageSender(i_pil_image_sender.IPilImageSender):
    @staticmethod
    def send_image(pil_image: Image):
        file_pointer = io.BytesIO()
        pil_image.save(file_pointer, format="png")
        file_pointer.seek(0)
        return flask.send_file(
            file_pointer,
            attachment_filename="histogram.png",
            as_attachment=False,
            add_etags=False,
        )

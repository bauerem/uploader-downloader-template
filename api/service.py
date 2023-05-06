import os
import magic
import time
from PIL import Image


class Service:
    def __init__(self, token, input_extension=None):
        # Construct upload folder path
        self.upload_folder = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "static/files"
        )

        self.token = token
        self.suffix = "_processed"

        # self.get_file_extension() assumes the file is already uploaded.
        # This might not be the case. That's why we can also pass the
        # input_extension to the constructor.
        if input_extension == None:
            self.input_extension = self.get_file_extension()
        else:
            self.input_extension = input_extension

        #
        # SPECIFY THIS BY HAND!
        #
        # If we have e.g. images, we can have input as jpg or png and the
        # output should be the same. That's what we see below.
        # But if we have e.g. OCR from PDF to txt then input is pdf but output
        # would be fixed to .txt
        self.output_extension = self.input_extension

        #
        # SPECIFY THIS BY HAND!
        #
        # Define allowed mime types
        self.allowed_mime_types = [
            "image/png",
            "image/jpeg",
            "text/plain",
            "application/pdf",
        ]

        self.path_input_file = os.path.join(
            self.upload_folder, self.token + "." + self.output_extension
        )
        self.path_processed_file = os.path.join(
            self.upload_folder, self.token + self.suffix + "." + self.output_extension
        )

    def get_file_extension(self):
        # Get names of all files in the upload folder
        filenames = os.listdir(self.upload_folder)

        # Look for the correct filename that contains the token.
        # Note: "filename" is always unique since we check for uniqueness when we
        # store it.
        filename = list(filter(lambda filename: self.token in filename, filenames))[0]

        extension = filename.split(".")[-1]

        return extension

    def process(self, **kwargs):
        # Load file
        input = Image.open(self.path_input_file)

        # Here we'd change the file somehow. We just wait 3 seconds.
        time.sleep(3)

        # Update file: We set the input as the output (because we didn't do
        # anything) and save it undera new name.
        output = input
        output.save(self.path_processed_file)

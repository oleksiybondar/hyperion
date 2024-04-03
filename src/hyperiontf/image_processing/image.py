import uuid
import os
import tempfile
from typing import Optional
import base64
import cv2
import numpy as np
from hyperiontf.fs import File
from hyperiontf.helpers.numeric_helpers import greatest_common_divisor


class Image(File):
    """
    An abstraction for image operations that extends the File class, incorporating image-specific functionalities.
    This class leverages OpenCV for image processing, providing methods to load, save, and display images, while
    inheriting file handling capabilities from the File class.

    Supported image formats include, but are not limited to: JPEG, PNG, BMP, and TIFF. The actual support depends on the
    OpenCV library's capabilities on the host system.

    The Image class simplifies interactions with image data, integrating file system operations and image processing
    into a cohesive object-oriented model.
    """

    def __init__(
        self, path: Optional[str] = None, img_data: Optional[str] = None, mode="rb"
    ):
        """
        Initializes a new instance of the Image class, allowing instantiation from either a file path or a base64 string.

        Args:
            path (Optional[str]): The path to the image file. If None and img_data is not provided, a temporary file path is generated.
            img_data (Optional[str]): The base64 encoded string of the image data.
            mode (str): The mode in which to open the file. Defaults to 'rb'.

        The constructor prioritizes img_data if provided. It decodes the base64 data and initializes the image.
        If img_data is not provided and a path is not specified, it generates a temporary filename for the image.

        Raises:
            ValueError: If neither path nor img_data is provided, or if the provided img_data cannot be processed.
        """
        # Generate a temporary path if no path is provided
        if not path and not img_data:
            path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.png")

        super().__init__(path, mode)

        if img_data:
            # Decode the base64 string to initialize the image
            image_data = base64.b64decode(img_data.split(",")[-1])
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            self._image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
            if self._image is None:
                raise ValueError("Unable to decode image from base64 string.")
        else:
            self._image = None

    @property
    def image(self):
        if self._image is None:
            self.open()

        return self._image

    def open(self):
        """
        Overrides the File class's open method to load the image using OpenCV. This method ensures that the image
        data is loaded into memory and available for processing.
        """
        if not self.exists():
            raise FileNotFoundError("The specified image file does not exist.")
        self._image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        if self.image is None:
            raise ValueError(
                "Unable to load image. The file may be corrupted or in an unsupported format."
            )

    def write(self, content=None, save_path=None):
        """
        Overrides the File class's write method to save the image data to a file. This can be used to save modifications
        made to the image.

        Args:
            content: Not used here, as image content is managed via the self.image attribute.
            save_path (str): The path where the image should be saved. If None, the image is saved over the original file.

        Raises:
            ValueError: If the image data is not available or the save path is invalid.
        """
        if self.image is None:
            raise ValueError("No image data available to save.")
        save_target = save_path if save_path else self.path
        cv2.imwrite(save_target, self.image)

    def close(self):
        """
        Overrides the File class's close method to clear the loaded image data from memory, ensuring that resources are
        released properly.
        """
        self._image = None

    def display_image(self):
        """
        Displays the loaded image in a window. This method provides a simple interface to visualize the image content.

        Raises:
            ValueError: If the image data is not available for display.
        """
        if self.image is None:
            raise ValueError("No image data available to display.")
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @property
    def width(self):
        """
        Gets the width of the image.

        Returns:
            int: The width of the image in pixels, or None if no image is loaded.
        """
        return self.image.shape[1] if self.image is not None else None

    @property
    def height(self):
        """
        Gets the height of the image.

        Returns:
            int: The height of the image in pixels, or None if no image is loaded.
        """
        return self.image.shape[0] if self.image is not None else None

    @property
    def has_alpha(self):
        return self.image.shape[2] == 4

    @property
    def aspect_ratio(self):
        """
        Gets the aspect ratio of the image.

        Returns:
            str: The aspect ratio in the format 'width:height', or None if no image is loaded.
                 The aspect ratio is reduced to its simplest form (e.g., 16:9 instead of 1920:1080) using the greatest common divisor.
        """
        width, height = self.width, self.height
        divisor = greatest_common_divisor(width, height)
        simplified_width = width // divisor
        simplified_height = height // divisor

        return f"{simplified_width}:{simplified_height}"

    def _calculate_new_dimensions(self, width, height):
        """
        Calculates new dimensions for the image, maintaining the aspect ratio based on the provided width and height.

        Args:
            width (int): The target width for the image resizing. Can be None if height is provided.
            height (int): The target height for the image resizing. Can be None if width is provided.

        Returns:
            tuple: A tuple containing the new width and height (int, int).

        This method uses the original image dimensions stored in the image attribute to calculate new dimensions
        that maintain the aspect ratio. If only one dimension (width or height) is provided, the other is calculated.
        If both are provided, the method adjusts them to maintain the aspect ratio, based on the most restrictive dimension.
        """
        if width is None and height is None:
            raise ValueError("Either width or height must be specified.")

        original_height, original_width = self.image.shape[:2]

        # Determine which dimension is the most restrictive and adjust the other accordingly
        ratio_w = width / float(original_width)
        ratio_h = height / float(original_height)
        if ratio_h > ratio_w:
            width = int(original_width * ratio_h)
        else:
            height = int(original_height * ratio_w)

        return width, height

    def resize(self, width=None, height=None, keep_aspect_ratio=True):
        """
        Resizes the image to the given width and height. If keep_aspect_ratio is True, maintains the original aspect ratio,
        adjusting the specified width and height to act as maximum dimensions.

        Args:
            width (int): The target new width of the image. If None and keep_aspect_ratio is False, the original width is maintained.
            height (int): The target new height of the image. If None and keep_aspect_ratio is False, the original height is maintained.
            keep_aspect_ratio (bool): Whether to maintain the original aspect ratio. Defaults to True.

        This method modifies the image attribute in-place, resizing the loaded image.
        """
        if width is None and height is None:
            raise ValueError("Either width or height must be specified.")

        if self.image is None:
            raise ValueError("No image loaded to resize.")

        if keep_aspect_ratio:
            width, height = self._calculate_new_dimensions(width, height)

        self._image = cv2.resize(self.image, (width, height))

    def rotate(self, angle, scale=1.0):
        """
        Rotates the image by the specified angle and scale.

        Args:
            angle (float): The angle in degrees to rotate the image. Positive values mean
                           counter-clockwise rotation (the coordinate origin is assumed to be the top-left corner).
            scale (float): Isotropic scale factor. If you want to avoid aliasing artifacts, you can use scale factors like 1/2, 1/4, etc.

        This method modifies the image attribute in-place, rotating the loaded image according to the given parameters.
        """
        if self.image is None:
            raise ValueError("No image loaded to rotate.")

        # Get the image dimensions, necessary for calculating the rotation matrix
        (height, width) = self.image.shape[:2]
        # Get the center of the image to create the rotation matrix
        center = (width / 2, height / 2)

        # Calculate the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        # Perform the actual rotation and store the result back in the image attribute
        self._image = cv2.warpAffine(self.image, rotation_matrix, (width, height))

    def to_base64(self, image_format="PNG"):
        """
        Converts the image to a base64-encoded string.

        Args:
            image_format (str): The format to use for encoding the image (e.g., "PNG", "JPEG"). Defaults to "PNG".

        Returns:
            str: The base64-encoded representation of the image.

        This method can be useful for embedding the image directly into HTML, storing it in text-based formats,
        or transmitting it over networks where binary data is not suitable.
        """
        if self.image is None:
            raise ValueError("No image loaded to convert.")

        retval, buffer = cv2.imencode(f".{image_format}", self.image)
        if not retval:
            raise ValueError(f"Could not encode the image to {image_format} format.")

        image_base64 = base64.b64encode(buffer).decode("utf-8")

        return f"data:image/{image_format.lower()};base64,{image_base64}"

    def __repr__(self):
        return f"Image(path='{self.path}', mode='{self.mode}')"

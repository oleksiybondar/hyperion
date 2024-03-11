from typing import Optional, Any

from .expectation_result import ExpectationResult, DEFAULT_EXPECT_LOGGER
from hyperiontf.logging.logger import Logger


def _add_attachment(attachments: list, title: str, data):
    attachments.append(
        {
            "title": title,
            "type": "image",
            "url": data,
        }
    )


class ImageExpectationResult(ExpectationResult):

    def __init__(
        self,
        result: bool,
        actual_value: Any,
        expected_value: Any,
        method: str,
        is_assertion: Optional[bool] = True,
        logger: Optional[Logger] = DEFAULT_EXPECT_LOGGER,
        sender: Optional[str] = None,
        diff: Optional[str] = None,
        human_readable_description: Optional[str] = None,
        prefix: Optional[str] = None,
        extra: Optional[dict] = None,
        processing_data: Optional[dict] = None,
    ):
        super().__init__(
            result,
            actual_value,
            expected_value,
            method,
            is_assertion,
            logger,
            sender,
            diff,
            human_readable_description,
            prefix,
            extra,
        )
        self.image_processing_data = processing_data

    @property
    def _log_meta(self):
        # Base metadata includes only the assertion result.
        meta = {"assertion": self.result} if self.is_assertion else {}

        # For failed assertions, include actual, expected, and diff images as attachments.

        attachments = []
        _add_attachment(attachments, "Actual Image", self.actual_value.to_base64())
        if self.image_processing_data["match_score"] < 100:
            if self.image_processing_data:
                _add_attachment(
                    attachments,
                    "Difference Image",
                    self.image_processing_data["difference_image"],
                )
            if self.expected_value:
                _add_attachment(
                    attachments, "Expected Image", self.expected_value.to_base64()
                )

        meta["attachments"] = attachments

        return meta

    @property
    def _short_comparison_info(self):
        info = "Comparison info."
        info += f"\nMatch score: {self.image_processing_data.get('match_score')},"
        info += f"\nImages scaled: {self.image_processing_data.get('scaled')},"
        info += f"\nPixel perfect verification: {self.image_processing_data.get('pixel_perfect')},"
        info += f"\nPartial verification: {self.image_processing_data.get('partial')},"
        info += f"\nSource images proportional: {self.image_processing_data.get('proportional')},"
        return info

    @property
    def _full_comparison_info(self):
        info = self._short_comparison_info
        info += f"\nActual image dimensions: {self.actual_value.aspect_ratio},"
        info += f"{self.actual_value.width}x{self.actual_value.height}"
        info += f"\nExpected image dimensions: {self.expected_value.aspect_ratio},"
        info += f"{self.expected_value.width}x{self.expected_value.height}"
        info += (
            f"\nComparison image dimensions: {self.image_processing_data.get('ratio')},"
        )
        info += f" {self.image_processing_data.get('width')}x{self.image_processing_data.get('height')}"
        return info

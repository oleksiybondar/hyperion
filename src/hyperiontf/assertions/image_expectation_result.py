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
        info = "Images match."
        info += f" Match score: {self.image_processing_data.get('match_score')},"
        info += f" Scaled: {self.image_processing_data.get('scaled')},"
        info += f" Final image ratio: {self.actual_value.aspect_ratio},"
        info += f" Size: {self.actual_value.width}x{self.actual_value.height}"
        return info

    @property
    def _full_comparison_info(self):
        info = f"Actual value ratio and dimensions: {self.actual_value.aspect_ratio}, {self.actual_value.width}x{self.actual_value.height}"
        info += f"\nExpected value: {self.expected_value.aspect_ratio}, {self.expected_value.width}x{self.expected_value.height}"
        info += f"\nComparison image dimensions: {self.image_processing_data.get('actual_value_width')}x{self.image_processing_data.get('actual_value_height')}"
        info += f"\nMatch score: {self.image_processing_data.get('match_score')}"
        info += f"\nScaled: {self.image_processing_data.get('scaled')}"
        info += f"\nProportional: {self.image_processing_data.get('proportional')}"
        info += f"\nRatio: {self.image_processing_data.get('ratio')}"
        return info

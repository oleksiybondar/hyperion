from ..section import Section


class PageObject(Section):
    """
    Represents the [page_object] section in the config.
    """

    def __init__(self):
        self.start_retries = 3
        self.retry_delay = 1

        self.log_private = True

        # Explanation of `viewport_*` properties and their usage in Responsive Design:
        # The `viewport_*` properties define minimum width thresholds for various viewport categories,
        # establishing a framework for responsive design that ensures web content adapts effectively across
        # a wide range of device sizes. Each property signifies the start of a new breakpoint range,
        # allowing developers to tailor CSS and JavaScript to respond dynamically to the browser's width.
        #
        # Breakpoint ranges are interpreted using the following logic: 1. For any given breakpoint `viewport_x`,
        # the applicable range is: viewport_x <= actual_width < viewport_x_plus_1. This delineates that devices with
        # widths falling within this range are categorized under `viewport_x`. 2. If no upper breakpoint is defined (
        # indicating the highest category), the range extends to infinity: viewport_x <= actual_width < infinity.
        # This category accommodates the widest screens. 3. The lowest category encompasses widths less than the
        # first breakpoint: -infinity < actual_width < viewport_x_zero, capturing the smallest devices.
        #
        # As a practical implementation example, the default values for these breakpoints are based on widely
        # recognized standards, such as those used by Facebook for its responsive design. These defaults serve
        # as a starting point and are as follows:
        # - `viewport_xs = 0`: For Tiny devices (-infinity < width < 576px)
        # - `viewport_sm = 576`: For Small devices (576px <= width < 768px)
        # - `viewport_md = 768`: For Medium devices (768px <= width < 992px)
        # - `viewport_lg = 992`: For Large devices (992px <= width < 1200px)
        # - `viewport_xl = 1200`: For Extra Large devices (1200px <= width < 1400px)
        # - `viewport_xxl = 1400`: For Ultra Large devices (1400px <= width < infinity)
        #
        # Developers are encouraged to customize these breakpoints based on their specific audience's
        # device usage patterns and emerging trends. Regularly updating these values ensures that web
        # applications remain optimized for the best possible user experience across all devices.

        self.viewport_xs = 0
        self.viewport_sm = 576
        self.viewport_md = 768
        self.viewport_lg = 992
        self.viewport_xl = 1200
        self.viewport_xxl = 1400

        # Viewport Configuration Rationale:
        # The viewport sizes and device resolutions specified in this configuration are derived from
        # statistical data reflecting the most common screen sizes and resolutions in use as of the
        # current time, with a notable emphasis on Apple devices due to their widespread prevalence
        # and influence on web design standards. These selections are informed by an analysis of
        # device usage patterns and market share, aiming to cover a broad spectrum of the most
        # frequently encountered devices in web traffic.
        #
        # It's important to note that the specified viewport resolutions are adjusted for device
        # pixel ratios (DPR). This means that while the actual physical screen resolution of a device
        # may be higher, the values here represent the effective resolution from a web content
        # rendering perspective. For example, a device with a DPR of 2 and a physical screen resolution
        # of 750 x 1334 will have an effective viewport resolution of 375 x 667 for web content.
        # This adjustment is crucial for designing and testing responsive web layouts, ensuring
        # compatibility and optimal viewing experiences across a variety of devices.
        #
        # These configurations are meant to serve as a practical guideline for responsive design
        # testing, acknowledging the dynamic nature of device and browser landscapes. Users are
        # encouraged to periodically review and update these values based on evolving trends in
        # device usage and screen specifications to maintain alignment with the majority of end-user
        # experiences.

        self.default_xs_resolution = "375x667"  # iPhone SE (Portrait)
        self.default_sm_resolution = "600x1000"  # Galaxy Tab A7 (Portrait)
        self.default_md_resolution = "768x1024"  # iPag 9.7 (Portrait)
        self.default_lg_resolution = "1280x800"  # MacBook Air 13-inch
        self.default_xl_resolution = "1536x9607"  # MacBook Pro 16-inch
        self.default_xxl_resolution = "2560x1440"  # 27-inch iMac

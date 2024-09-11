
/**
 * Line class for rendering and managing individual log lines, including expansion and extra data.
 */
class Line {
  /**
   * Constructor for the Line class.
   * @param {Line} parent - The parent Line object (if any) to which this line belongs.
   * @param {Object} meta - Metadata for this log line.
   */
  constructor(parent, meta) {
    this.parent = parent
    this.metaData = meta

    this.wasRendered = false;
    this.isExpandToggled = false;

    this.lines = []

    this.domElement = document.createElement('div');
    this.messageWrapper = document.createElement('div');
  }

  /**
   * Check if the line is expandable (has child lines).
   * @returns {boolean} True if the line has child lines, false otherwise.
   */
  get isExpandable(){
    return this.lines.length > 0;
  }

  /**
   * Get the configuration object from the window.
   * @returns {Object} The configuration object.
   */
  get config(){
    return window.hyperionTestingFrameworkConfig;
  }

  /**
   * Get the event broker object from the window.
   * @returns {Object} The event broker object.
   */
  get eventBroker(){
    return window.hyperionTestingFrameworkEventBrocker;
  }

  /**
   * Get the level of the log line, considering child lines.
   * @returns {number} The level of the log line.
   */
  get level(){
    if (!this.isExpandable) return this.metaData.lvl || 0;

    let currentLevel = this.metaData.lvl || 0;

    this.lines.forEach((line) => {
      if (line.level > currentLevel && line.level !== 10000) currentLevel = line.level;
    });

    return currentLevel;
  }

  /**
   * Check if the log line has an assertion.
   * @returns {boolean} True if the log line or any of its child lines has an assertion, false otherwise.
   */
  get hasAssertion(){
    if (this.assertion !== undefined) return true

    return this.lines.find((line) => {line.hasAssertion}) !== undefined;
  }

  /**
   * Get the assertion value of the log line.
   * If the log line itself has an assertion, return it. Otherwise, return the first assertion value found in child lines.
   * @returns {string|undefined} The assertion value if available, undefined otherwise.
   */
  get assertionValue(){
    if (this.assertion !== undefined) return this.assertion;

    return this.lines.find((line) => {line.hasAssertion}).assertionValue;
  }

  /**
   * Get the log level name based on the numeric log level.
   * @returns {string} The log level name. Possible values: 'debug', 'info', 'warning', 'error', 'fatal', 'header'.
   */
  get levelName(){
    switch (this.level) {
      case 0: case 1: case 2: case 3: case 5: case 6: case 7: case 8: case 9: case 10:
        return 'debug'
      case 11: case 12: case 13: case 15: case 16: case 17: case 18: case 19: case 20:
        return 'info'
      case 21: case 22: case 23: case 25: case 26: case 27: case 28: case 29: case 30:
        return 'warning'
      case 31: case 32: case 33: case 35: case 36: case 37: case 38: case 39: case 40:
        return 'error'
      case 41: case 42: case 43: case 45: case 46: case 47: case 48: case 49: case 50:
        return 'fatal'
      case -999:
        return 'header'
    }
  }

  /**
   * Get the log message of the log line.
   * @returns {string} The log message.
   */
  get message(){
    return this.metaData.msg;
  }

  /**
   * Get the depth of the log line.
   * @returns {number} The depth of the log line.
   */
  get depth(){
    return this.metaData.depth || 0;
  }

  /**
   * Get the timestamp of the log line.
   * @returns {string} The timestamp of the log line.
   */
  get timestamp(){
    return this.metaData.time || Date.now().toString();
  }

  get loggerName(){
    return this.metaData.name;
  }

  get loggerPackage(){
    return this.loggerName?.split('.')[0];
  }

  get assertion(){
    return this.metaData.assertion
  }

  get exception(){
    return this.metaData.exception
  }

  get attachments(){
    if (!this.metaData.attachments) return undefined;

    return  JSON.parse(this.metaData.attachments);
  }

  get filePath(){
    return this.metaData.fPath;
  }

  get fileLine(){
    return this.metaData.fLine;
  }

  get hasBacktrace(){
    return  !!this.exception;
  }

  get screenSnaps(){
    if (!this.attachments) return [];

    return this.attachments.filter((attachment) => { return attachment.type === 'image' });
  }

  get hasScreenSnap(){
    return  this.screenSnaps.length > 0;
  }

  get pageSources(){
    if (!this.attachments) return [];

    return this.attachments.filter((attachment) => { return ['html', 'xml'].indexOf(attachment.type) !== -1  });
  }

  get hasPageSource(){
    return  this.pageSources.length > 0;
  }

  /**
   * Renders the log line and its child lines recursively.
   * This method generates the DOM elements representing the log line and its content.
   * It also handles the visibility of log lines based on the configuration settings.
   * @returns {HTMLElement} The DOM element representing the log line.
   */
  render() {
    // Check if the log line has been rendered before
    if (this.wasRendered) return this.domElement;

    // Add CSS class to the main log line wrapper
    this.domElement.classList.toggle('log-line-wrapper');

    // Render the main log line content
    this.renderLine();

    // Render any extra data such as exceptions and attachments
    this.renderExtraData();

    // Toggle the visibility of the log line based on configuration and content
    this.toggleLine();

    // Subscribe to relevant events for updating log line visibility
    this.subscribeForEvents();

    // Mark the log line as rendered
    this.wasRendered = true;

    // Return the DOM element representing the log line
    return this.domElement;
  }

  /**
   * Renders the main log line content and constructs the DOM elements for the log message, timestamp,
   * log level, logger name, source link, and other relevant details.
   */
  renderLine() {
    // Create the message wrapper DOM element for holding the log message and related elements
    this.messageWrapper.classList.toggle('message-wrapper');
    this.messageWrapper.classList.toggle(this.levelName); // Add CSS class based on the log level

    // Check if the log line contains an assertion and apply appropriate CSS classes if present
    if (this.hasAssertion) {
      this.messageWrapper.classList.toggle('assertion');
      this.messageWrapper.classList.toggle(`assert-${this.assertionValue}`);
    }

    // Render the expand/collapse button for log lines with children (expandable)
    if (this.isExpandable) this.renderExpandCollapseButton();

    // Render a stub element for spacing purposes when the log line is collapsed
    this.renderExpandCollapseStub();

    // Render the timestamp element
    this.renderTime();

    // Render the log level element (icon indicating log level)
    this.renderLevel();

    // Render the logger name element with tooltip showing the package and full name
    this.renderLoggerName();

    // Render the log message content and handle message collapsing if needed
    this.renderMessage();

    // Render the source link to the file and line where the log was generated
    this.renderSourceLink();

    // Append the message wrapper containing all the log line elements to the main DOM element
    this.domElement.append(this.messageWrapper);
  }

  /**
   * Renders the expand/collapse button for log lines with children (expandable).
   * The button allows users to toggle the visibility of child log lines.
   */
  renderExpandCollapseButton() {
    // Create the expand/collapse button wrapper element
    const component = this; // Reference to the current Line instance (used in the click event handler)
    const button = document.createElement('span');
    button.classList.toggle('expand-collapse-wrapper');

    // Create the icon element for the button
    const icon = document.createElement('icon');
    icon.classList.toggle('expand');
    icon.classList.toggle('icon');
    icon.classList.toggle(this.levelName); // Add CSS class based on the log level
    button.append(icon);

    // Define the click event handler for the button
    button.onclick = function () {
      // Toggle the expand/collapse state for the log line
      component.isExpandToggled = !component.isExpandToggled;

      // If the log line is expanded, render and display its children log lines
      if (component.isExpandToggled) {
        component.renderChildrenLines();
      }

      // Toggle the icon class to show the appropriate icon (expand or collapse)
      icon.classList.toggle('expand');
      icon.classList.toggle('collapse');

      // Toggle the visibility of children log lines
      component.toggleChildrenVisibility();
    };

    // Append the expand/collapse button to the message wrapper element
    this.messageWrapper.append(button);
  }

  /**
   * Renders the expand/collapse stub, a placeholder for the expand/collapse button.
   * The expand/collapse stub is shown when the log line is not expandable (has no children).
   * It serves as a visual alignment for log lines with children.
   */
  renderExpandCollapseStub() {
    // Create the expand/collapse stub element
    this.timeElement = document.createElement('span');
    this.timeElement.classList.toggle('expand-collapse-stub');
    this.timeElement.innerHTML = '&nbsp'; // Use non-breaking space as a placeholder

    // Append the expand/collapse stub to the message wrapper element
    this.messageWrapper.append(this.timeElement);
  }

  /**
   * Renders the timestamp element for the log line.
   * The timestamp is displayed with each log line to indicate the time when the log was recorded.
   */
  renderTime() {
    // Create the timestamp element
    this.timeElement = document.createElement('span');
    this.timeElement.classList.toggle('time-stamp');
    this.timeElement.innerHTML = this.timestamp; // Set the timestamp value

    // Toggle the timestamp visibility based on configuration
    this.toggleTimestamp();

    // Append the timestamp element to the message wrapper element
    this.messageWrapper.append(this.timeElement);
  }

  /**
   * Renders the logger name element for the log line.
   * The logger name is displayed with each log line to indicate the source of the log message.
   * The logger name may contain a package name and a logger name, and it is split for better display.
   */
  renderLoggerName() {
    // Create the logger name element
    this.loggerNameElement = document.createElement('span');
    this.loggerNameElement.classList.toggle('logger-name');

    // Determine the color class based on the logger package
    this.loggerNameElement.classList.toggle(this.config.getSourceColor(this.loggerPackage));

    // Construct the logger name HTML content with a tooltip showing the full logger name
    this.loggerNameElement.innerHTML = `<span class="logger-package tooltip tooltip-arrow-left">[${capitalise(splitCamelCased(this.loggerPackage))}]
                                   <span class="logger-full-name tooltip-text">${this.loggerName}</span></span>`;

    // Toggle the logger name visibility based on configuration
    this.toggleLoggerName();

    // Append the logger name element to the message wrapper element
    this.messageWrapper.append(this.loggerNameElement);
  }

  /**
   * Renders the log level element for the log line.
   * The log level is displayed with each log line to indicate the severity of the log message.
   * The log level is represented as an icon with a specific color based on the severity level.
   * If the log line has an associated assertion, an additional assertion icon is displayed.
   */
  renderLevel() {
    // Create the log level element
    this.levelElement = document.createElement('span');
    this.levelElement.classList.toggle('level');

    // Construct the HTML content for the log level element with an icon representing the severity level
    let innerHTML = `<icon class="${this.levelName} icon">&nbsp;</nbs></icon>`;

    // If the log line has an associated assertion, add an additional assertion icon
    if (this.assertion !== undefined) {
      innerHTML += `<icon class="assertion assert-${this.assertion} icon">&nbsp;</nbs></icon>`;
    }

    // Set the constructed HTML content to the log level element
    this.levelElement.innerHTML = innerHTML;

    // Toggle the log level visibility based on configuration
    this.toggleLogLevel();

    // Append the log level element to the message wrapper element
    this.messageWrapper.append(this.levelElement);
  }

  /**
   * Renders the expand/collapse button for the log message content.
   * This button allows the user to toggle the visibility of the log message content.
   * If the log message has more than 9 lines, it will be initially collapsed, and this button will be displayed.
   * When clicked, the button toggles the "collapsed" class on the log message element to hide or show its content.
   * The icon for the button changes between "expand" and "collapse" based on the current visibility state.
   * The icon color corresponds to the severity level of the log message.
   *
   * @returns {HTMLElement} The HTML element representing the expand/collapse button.
   */
  renderMessageExpandCollapseButton() {
    const component = this;

    // Create the button element
    const button = document.createElement('span');
    button.classList.toggle('message-expand-collapse-wrapper');

    // Create the icon element representing the expand/collapse icon
    const icon = document.createElement('icon');
    icon.classList.toggle('expand');
    icon.classList.toggle('stick-top');
    icon.classList.toggle('icon');
    icon.classList.toggle('sticky');
    icon.classList.toggle(this.levelName);

    // Append the icon to the button
    button.append(icon);

    // Define the behavior when the button is clicked
    button.onclick = function () {
      // Toggle the "collapsed" class of the log message element to hide/show its content
      component.messageElement.classList.toggle('collapsed');
      // Toggle the icon between "expand" and "collapse" to represent the current visibility state
      icon.classList.toggle('expand');
      icon.classList.toggle('stick-top');
      icon.classList.toggle('collapse');
      icon.classList.toggle('stick-bottom');
    };

    return button;
  }

  /**
   * Renders the log message content.
   * This method creates and configures the HTML elements to display the log message content.
   * It handles cases where the log message has more than 9 lines and provides an expand/collapse button.
   * The content is initially collapsed if it exceeds 9 lines, and the button allows the user to toggle visibility.
   * The method also applies appropriate classes to style the log message based on its severity level and assertion status.
   *
   * @returns {HTMLElement} The HTML element representing the log message content.
   */
  renderMessage() {
    // Create the main container for the log message content
    this.messageElement = document.createElement('span');
    this.messageElement.classList.toggle('message');
    this.messageElement.classList.toggle('collapsed');

    // Create a wrapper to contain the log message text content
    const contentWrapper = document.createElement('span');
    contentWrapper.classList.toggle('message-content');
    contentWrapper.innerHTML = formatRegularTextToHtml(this.message);

    // Append the log message text content to the message element
    this.messageElement.append(contentWrapper);

    // Check if the log message has more than 9 lines to decide whether to add the expand/collapse button
    if (this.message.split('\n').length > 9) {
      const expandCollapseMessageButton = this.renderMessageExpandCollapseButton();
      this.messageElement.append(expandCollapseMessageButton);
    }

    // Append the log message content to the main container element
    this.messageWrapper.append(this.messageElement);
  }

  /**
   * Renders the source code link associated with the log message.
   * This method creates and configures an HTML element to display a link to the source code location
   * associated with the log message. The link is represented by an anchor tag with the source code icon.
   * If the log message contains a file path and line number, the link will point to that location.
   *
   * @returns {HTMLElement} The HTML element representing the source code link.
   */
  renderSourceLink() {
    // Create the container for the source code link
    this.sourceLinkElement = document.createElement('span');
    this.sourceLinkElement.classList.toggle('logger-source');

    // Initialize the link URL and target attributes
    let lnk = '#';
    let target = '';
    if (this.filePath) {
      lnk = `file:///${this.filePath}#${this.fileLine}`;
      target = 'target="_blank"';
    }

    // Create the anchor tag (link) with the source code icon inside
    this.sourceLinkElement.innerHTML = `<a href="${lnk}" ${target}>
                                         <icon class="icon sourceCode">&nbsp;</icon></a>`;

    // Toggle visibility of the source code link based on the configuration
    this.toggleSourceCode();

    // Append the source code link to the log message container
    this.messageWrapper.append(this.sourceLinkElement);
  }

  /**
   * Renders any extra data associated with the log message, such as exception information or attachments.
   * This method creates and configures an HTML element to display the extra data associated with the log message.
   * If the log message contains an exception, it will be rendered as part of the extra data.
   * If the log message has any attachments (e.g., screen snapshots or page sources), they will also be rendered.
   *
   * @returns {void}
   */
  renderExtraData() {
    // If no extra data (exception or attachments) exists, return without rendering anything
    if (!(!!this.exception || !!this.attachments)) return;

    // Create the container for the extra data
    this.extraWrapper = document.createElement('div');
    this.extraWrapper.classList.toggle('extra-message-data-wrapper');

    // Render the exception information if available
    this.renderException();

    // Render any attachments (e.g., screen snapshots or page sources) associated with the log message
    this.renderAttachments();

    // Toggle visibility of the extra data based on the configuration
    this.toggleExtraData();

    // Append the extra data container to the log message container
    this.domElement.append(this.extraWrapper);
  }

  /**
   * Renders any attachments (e.g., screen snapshots or page sources) associated with the log message.
   * This method creates and configures HTML elements to display the attachments, if available.
   * If the log message contains any screen snapshots, they will be rendered with their titles and image URLs.
   * If the log message contains any page sources, they will be rendered with their titles and iframe URLs.
   *
   * @returns {void}
   */
  renderAttachments() {
    // If no attachments exist, return without rendering anything
    if (!this.attachments) return;

    // Render any screen snapshots associated with the log message
    this.renderScreenSnaps();

    // Render any page sources associated with the log message
    this.renderPageSources();
  }

  renderException(){
    if (!this.exception) return;

    this.exceptionElement = document.createElement('div');
    this.exceptionElement.classList.toggle('exception');
    this.exceptionElement.innerHTML = formatRegularTextToHtml(this.exception);

    this.extraWrapper.append(this.exceptionElement);
  }

  /**
   * Renders the exception associated with the log message, if available.
   * This method creates and configures an HTML element to display the exception details.
   * If the log message contains an exception, it will be rendered as formatted text within a div element.
   * If there is no exception, this method does nothing.
   *
   * @returns {void}
   */
  renderException() {
    // If no exception exists, return without rendering anything
    if (!this.exception) return;

    // Create a new div element to display the exception details
    this.exceptionElement = document.createElement('div');
    this.exceptionElement.classList.toggle('exception');

    // Set the innerHTML of the div element with the formatted text of the exception
    this.exceptionElement.innerHTML = formatRegularTextToHtml(this.exception);

    // Append the exception element to the extra data wrapper for display
    this.extraWrapper.append(this.exceptionElement);
  }

  /**
   * Renders screen snaps if available.
   * This method creates a container element for screen snaps, generates the HTML for each screen snap,
   * and appends them to the parent element.
   */
  renderScreenSnaps() {
    // Check if there are any screen snaps available
    if (!this.hasScreenSnap) return;

    // Create a new container element for screen snaps
    this.screenSnapsElement = document.createElement('div');
    this.screenSnapsElement.classList.toggle('screen-snaps-wrapper');

    // Generate the HTML for each screen snap
    const screenSnaps = this.screenSnaps.map((screenSnap) => {
      return `<div class="screen-snap-wrapper">
                    <label class="screen-snap-label">${screenSnap.title}</label>
                    <img class="screen-snap" src="${screenSnap.url}">
                </div>`;
    });

    // Add the generated screen snaps HTML to the container element
    this.screenSnapsElement.innerHTML = screenSnaps.join('\n');

    // Append the container element to the parent element (this.extraWrapper)
    this.extraWrapper.append(this.screenSnapsElement);
  }

  /**
   * Renders the page sources associated with the log message, if available.
   * This method creates and configures an HTML element to display the page sources.
   * If the log message contains page sources, they will be rendered as iframes within div elements.
   * If there are no page sources, this method does nothing.
   *
   * @returns {void}
   */
  renderPageSources() {
    // If no page sources exist, return without rendering anything
    if (!this.hasPageSource) return;

    // Create a new div element to contain the page sources
    this.pageSourcesElement = document.createElement('div');
    this.pageSourcesElement.classList.toggle('page-sources-wrapper');

    // Prepare the HTML for each page source and create iframe elements to display them
    const sources = this.pageSources.map((pageSource) => {
      return `<div class="page-source-wrapper">
                 <label class="page-source-label">${pageSource.title}</label>
                 <iframe class="page-source" src="${pageSource.url}"></iframe>
               </div>`;
    });

    // Set the innerHTML of the div element with the page source iframes
    this.pageSourcesElement.innerHTML = sources.join('\n');

    // Append the page sources element to the extra data wrapper for display
    this.extraWrapper.append(this.pageSourcesElement);
  }

  /**
   * Renders the children lines associated with the log message, if available.
   * This method creates and configures a div element to contain the children lines.
   * If the log message has child lines, they will be rendered recursively and appended to the children wrapper.
   * If there are no child lines, this method does nothing.
   *
   * @returns {void}
   */
  renderChildrenLines() {
    // If the children wrapper already exists, return without rendering anything
    if (this.childrenWrapper) return;

    // Create a new div element to contain the children lines
    this.childrenWrapper = document.createElement('div');
    this.childrenWrapper.classList.toggle('child-messages-wrapper');
    this.childrenWrapper.classList.toggle('hidden');

    // Render and append each child line to the children wrapper
    this.lines.forEach((childLine) => {
      if (childLine.level !== 10000) {
        this.childrenWrapper.append(childLine.render());
      }
    });

    // Append the children wrapper to the current log line's DOM element
    this.domElement.append(this.childrenWrapper);
  }

  /**
   * Toggles the visibility of the children lines associated with the log message.
   * If the children wrapper is hidden, this method makes it visible by removing the 'hidden' class.
   * If the children wrapper is visible, this method hides it by adding the 'hidden' class.
   *
   * The visibility of the children lines is controlled by adding or removing the 'hidden' class from the
   * children wrapper element, which is a div that contains the child log lines.
   *
   * @returns {void}
   */
  toggleChildrenVisibility() {
    // Toggle the 'hidden' class to show or hide the children wrapper element
    this.childrenWrapper.classList.toggle('hidden');
  }

  /**
   * Toggles the visibility of the logger name in the log message.
   * If the logger name element is hidden, this method makes it visible by removing the 'hidden' class.
   * If the logger name element is visible, this method hides it by adding the 'hidden' class.
   *
   * The visibility of the logger name is controlled by adding or removing the 'hidden' class from the
   * logger name element, which is a span displaying the logger name.
   *
   * The visibility of the logger name is based on the configuration settings, specifically whether the
   * 'logger' column is enabled or disabled.
   *
   * @returns {void}
   */
  toggleLoggerName() {
    // Check if the 'logger' column is enabled in the configuration
    const visible = this.config.isColumnEnabled('logger');

    // Check if the logger name element is currently hidden
    const disabled = this.loggerNameElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility settings
    if (!(visible ^ disabled)) {
      this.loggerNameElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of the timestamp in the log message.
   * If the timestamp element is hidden, this method makes it visible by removing the 'hidden' class.
   * If the timestamp element is visible, this method hides it by adding the 'hidden' class.
   *
   * The visibility of the timestamp is controlled by adding or removing the 'hidden' class from the
   * timestamp element, which is a span displaying the timestamp of the log message.
   *
   * The visibility of the timestamp is based on the configuration settings, specifically whether the
   * 'timestamp' column is enabled or disabled.
   *
   * @returns {void}
   */
  toggleTimestamp() {
    // Check if the 'timestamp' column is enabled in the configuration
    const visible = this.config.isColumnEnabled('timestamp');

    // Check if the timestamp element is currently hidden
    const disabled = this.timeElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility settings
    if (!(visible ^ disabled)) {
      this.timeElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of the log level icon in the log message.
   * If the log level element is hidden, this method makes it visible by removing the 'hidden' class.
   * If the log level element is visible, this method hides it by adding the 'hidden' class.
   *
   * The visibility of the log level icon is controlled by adding or removing the 'hidden' class from
   * the level element, which is a span displaying the log level icon (e.g., debug, info, warning, etc.).
   *
   * The visibility of the log level is based on the configuration settings, specifically whether the
   * 'level' column is enabled or disabled.
   *
   * @returns {void}
   */
  toggleLogLevel() {
    // Check if the 'level' column is enabled in the configuration
    const visible = this.config.isColumnEnabled('level');

    // Check if the log level element is currently hidden
    const disabled = this.levelElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility settings
    if (!(visible ^ disabled)) {
      this.levelElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of the source code link in the log message.
   * If the source code link element is hidden, this method makes it visible by removing the 'hidden' class.
   * If the source code link element is visible, this method hides it by adding the 'hidden' class.
   *
   * The visibility of the source code link is controlled by adding or removing the 'hidden' class from
   * the sourceLinkElement, which is a span containing an anchor element linking to the source code.
   *
   * The visibility of the source code link is based on the configuration settings, specifically whether
   * the 'sourceCode' column is enabled or disabled.
   *
   * @returns {void}
   */
  toggleSourceCode() {
    // Check if the 'sourceCode' column is enabled in the configuration
    const visible = this.config.isColumnEnabled('sourceCode');

    // Check if the source code link element is currently hidden
    const disabled = this.sourceLinkElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility settings
    if (!(visible ^ disabled)) {
      this.sourceLinkElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of the entire log line.
   * If the log line element is hidden, this method makes it visible by removing the 'hidden' class.
   * If the log line element is visible, this method hides it by adding the 'hidden' class.
   *
   * The visibility of the log line is controlled by adding or removing the 'hidden' class from
   * the domElement, which is a div containing the entire log line's content.
   *
   * The visibility of the log line is based on the configuration settings, specifically whether
   * the log level ('levelName') and source ('loggerPackage') are enabled or disabled in the columns.
   * If the log level or source is disabled, the log line is hidden.
   * Additionally, if the log line contains an assertion and the 'assertion' level is disabled,
   * the log line is hidden as well.
   *
   * @returns {void}
   */
  toggleLine() {
    // Check if the log level is visible based on the configuration
    const isLevelVisible = this.config.isLevelEnabled(this.levelName);

    // Check if the source is visible based on the configuration
    const isSourceVisible = this.config.isSourceEnabled(this.loggerPackage.toLowerCase());

    // Check if the log line contains an assertion and if the 'assertion' level is visible
    const isAssertionsVisible = this.config.isLevelEnabled('assertion');
    const hasAssertion = this.hasAssertion;

    // Check if the log line element is currently hidden
    let disabled = this.domElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility settings and assertion presence
    if (hasAssertion && isAssertionsVisible) {
      if (disabled) this.domElement.classList.toggle('hidden');
      return;
    }

    if (!(isLevelVisible ^ disabled)) {
      this.domElement.classList.toggle('hidden');
      disabled = !disabled;
    }

    if (!(isSourceVisible ^ disabled) && isLevelVisible) {
      this.domElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of extra data associated with the log line.
   * The extra data includes backtraces, screen snaps, and page sources.
   *
   * If the extra data wrapper (extraWrapper) is hidden, this method makes it visible
   * by removing the 'hidden' class. If the extra data wrapper is visible, this method hides
   * it by adding the 'hidden' class.
   *
   * The visibility of the extra data is controlled by adding or removing the 'hidden' class
   * from the extraWrapper, which is a div containing the additional data elements.
   *
   * The visibility of the extra data is based on the configuration settings, specifically
   * whether backtraces, screen snaps, or page sources are enabled or disabled in the content.
   * If any of these content types are disabled, the corresponding extra data will be hidden.
   *
   * @returns {void}
   */
  toggleExtraData() {
    // Check if the backtrace content is visible based on the configuration
    const isBacktraceVisible = this.config.isContentEnabled('backtrace');

    // Check if the screen snap content is visible based on the configuration
    const isScreenSnapVisible = this.config.isContentEnabled('screenSnap');

    // Check if the page source content is visible based on the configuration
    const isPageSourceVisible = this.config.isContentEnabled('pageSource');

    // Check if the extra data wrapper is currently hidden
    const disabled = this.extraWrapper.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility settings for each content type
    if (!(((isBacktraceVisible && this.hasBacktrace) ||
      (isScreenSnapVisible && this.hasScreenSnap) ||
      (isPageSourceVisible && this.hasPageSource)) ^ disabled)) {
      this.extraWrapper.classList.toggle('hidden');
    }

    // Call individual methods to toggle visibility of specific extra data elements
    this.toggleException();
    this.toggleScreenSnaps();
    this.togglePageSources();
  }

  /**
   * Toggles the visibility of the exception content associated with the log line.
   * The exception content includes stack traces and error information.
   *
   * If the exception element (exceptionElement) is hidden, this method makes it visible
   * by removing the 'hidden' class. If the exception element is visible, this method hides
   * it by adding the 'hidden' class.
   *
   * The visibility of the exception content is controlled by adding or removing the 'hidden' class
   * from the exceptionElement, which is a div containing the formatted exception text.
   *
   * The visibility of the exception content is based on the configuration setting for backtraces.
   * If backtraces are disabled in the content, the exception content will be hidden.
   *
   * @returns {void}
   */
  toggleException() {
    if (!this.exceptionElement) return
    // Check if the backtrace content is visible based on the configuration
    const isBacktraceVisible = this.config.isContentEnabled('backtrace');

    // Check if the exception element is currently hidden
    const disabled = this.exceptionElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility setting for backtraces
    if (!(isBacktraceVisible ^ disabled)) {
      this.exceptionElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of the screen snapshots content associated with the log line.
   * The screen snapshots content includes images captured during testing or logging.
   *
   * If the screen snapshots element (screenSnapsElement) is hidden, this method makes it visible
   * by removing the 'hidden' class. If the screen snapshots element is visible, this method hides
   * it by adding the 'hidden' class.
   *
   * The visibility of the screen snapshots content is controlled by adding or removing the 'hidden' class
   * from the screenSnapsElement, which is a div containing the screen snapshot images.
   *
   * The visibility of the screen snapshots content is based on the configuration setting for screenSnap.
   * If screen snapshots are disabled in the content, the screen snapshots content will be hidden.
   *
   * @returns {void}
   */
  toggleScreenSnaps() {
    // entire that
    if (!this.screenSnapsElement) return

    // Check if the screen snapshot content is visible based on the configuration
    const isScreenSnapVisible = this.config.isContentEnabled('screenSnap');

    // Check if the screen snapshots element is currently hidden
    const disabled = this.screenSnapsElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility setting for screen snapshots
    if (!(isScreenSnapVisible ^ disabled)) {
      this.screenSnapsElement.classList.toggle('hidden');
    }
  }

  /**
   * Toggles the visibility of the page sources content associated with the log line.
   * The page sources content includes HTML or XML sources captured during testing or logging.
   *
   * If the page sources element (pageSourcesElement) is hidden, this method makes it visible
   * by removing the 'hidden' class. If the page sources element is visible, this method hides
   * it by adding the 'hidden' class.
   *
   * The visibility of the page sources content is controlled by adding or removing the 'hidden' class
   * from the pageSourcesElement, which is a div containing iframes displaying the page sources.
   *
   * The visibility of the page sources content is based on the configuration setting for pageSource.
   * If page sources are disabled in the content, the page sources content will be hidden.
   *
   * @returns {void}
   */
  togglePageSources() {
    if (!this.pageSourcesElement) return
    // Check if the page source content is visible based on the configuration
    const isPageSourceVisible = this.config.isContentEnabled('pageSource');

    // Check if the page sources element is currently hidden
    const disabled = this.pageSourcesElement.classList.contains('hidden');

    // Toggle the 'hidden' class based on the visibility setting for page sources
    if (!(isPageSourceVisible ^ disabled)) {
      this.pageSourcesElement.classList.toggle('hidden');
    }
  }

  /**
   * Subscribes the log line to various events that control its visibility and behavior in the log viewer.
   * These events include toggling the visibility of log lines based on their log level or source package,
   * toggling the visibility of specific columns (e.g., timestamp, logger name, level, source code),
   * and toggling the visibility of extra data associated with the log line (e.g., backtrace, screen snaps, page sources).
   *
   * This method registers event handlers for the log line using the event broker (eventBroker) of the application.
   * When the specified events are triggered elsewhere in the application (e.g., by user actions or changes in settings),
   * the event handlers in this log line will be called to update its visibility and behavior accordingly.
   *
   * The method subscribes the log line to the following events:
   * - Log level visibility events (e.g., 'debugLevelVisibility', 'infoLevelVisibility', 'errorLevelVisibility', etc.)
   * - Source package visibility events (e.g., 'somepackageSourceVisibility', 'anotherpackageSourceVisibility', etc.)
   * - Column visibility events (e.g., 'timestampColumnVisibility', 'loggerColumnVisibility', 'levelColumnVisibility', etc.)
   * - Assertion level visibility event ('assertionLevelVisibility')
   * - Content visibility events (e.g., 'backtraceContentVisibility', 'screenSnapContentVisibility', 'pageSourceContentVisibility')
   *
   * The event handlers are specified as strings in the format 'methodName' (e.g., 'toggleLine', 'toggleTimestamp', etc.),
   * and these methods must be defined in the current Line instance to be called when the corresponding events are triggered.
   *
   * @returns {void}
   */
  subscribeForEvents() {
    // Subscribe to log level visibility events
    this.eventBroker.subscribe(`${this.levelName}LevelVisibility`, this, 'toggleLine');

    // Subscribe to source package visibility events
    this.eventBroker.subscribe(`${this.loggerPackage.toLowerCase()}SourceVisibility`, this, 'toggleLine');

    // Subscribe to column visibility events
    this.eventBroker.subscribe('timestampColumnVisibility', this, 'toggleTimestamp');
    this.eventBroker.subscribe('loggerColumnVisibility', this, 'toggleLoggerName');
    this.eventBroker.subscribe('levelColumnVisibility', this, 'toggleLogLevel');
    this.eventBroker.subscribe('sourceCodeColumnVisibility', this, 'toggleSourceCode');

    // Subscribe to assertion level visibility event
    if (this.hasAssertion) this.eventBroker.subscribe('assertionLevelVisibility', this, 'toggleLine');

    // Subscribe to content visibility events (backtrace, screen snaps, page sources)
    if (this.hasPageSource) this.eventBroker.subscribe('pageSourceContentVisibility', this, 'toggleExtraData');
    if (this.hasScreenSnap) this.eventBroker.subscribe('screenSnapContentVisibility', this, 'toggleExtraData');
    if (this.hasBacktrace) this.eventBroker.subscribe('backtraceContentVisibility', this, 'toggleExtraData');
  }
}
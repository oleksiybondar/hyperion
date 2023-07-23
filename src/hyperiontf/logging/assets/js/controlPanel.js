/**
 * ControlPanel class for rendering and managing the control panel, which includes filters and switches
 * for log levels, log sources, and column visibility.
 */
class ControlPanel {
  constructor() {
    // Initialize the flag to track whether the control panel was rendered
    this.wasRendered = false;

    // Create a DOM element to represent the control panel
    this.domElement = document.createElement('div');
  }

  // Get the application configuration from the global window object
  get config() {
    return window.hyperionTestingFrameworkConfig;
  }

  // Get the event broker from the global window object
  get eventBroker() {
    return window.hyperionTestingFrameworkEventBrocker;
  }

  /**
   * Render the control panel and return the DOM element representing it.
   * @returns {HTMLElement} The DOM element representing the control panel.
   */
  render() {
    if (this.wasRendered) return this.domElement;

    // Toggle CSS classes for styling
    this.domElement.classList.toggle('control-panel-wrapper');
    this.domElement.classList.toggle('document-header');

    // Render filters and column switcher components
    this.renderFilers();
    this.renderColumnsSwitcher();

    // Set the rendered flag to true and return the DOM element
    this.wasRendered = true;
    return this.domElement;
  }

  /**
   * Render the filters section in the control panel for log sources, and add event listeners.
   */
  renderFilers() {
    // Create a container for the filters section
    this.filtersContainer = document.createElement('div');
    this.filtersContainer.classList.toggle('filters-panel-wrapper');

    // Render and add log source filters bar
    this.renderSourceFiltersBar();

    // Render and add log levels filters bar
    this.renderLevelsFiltersBar();

    // Render and add content filters bar
    this.renderContentFilterBar();

    // Append the filters container to the main control panel DOM element
    this.domElement.append(this.filtersContainer);
  }

  /**
   * Render the column switcher section in the control panel and add event listeners.
   */
  renderColumnsSwitcher() {
    // Create a container for the column switcher section
    this.columnsContainer = document.createElement('div');
    this.columnsContainer.classList.toggle('column-switch-panel-wrapper');

    // Render and add column filters bar
    this.renderColumnsFilterBar();

    // Append the column switcher container to the main control panel DOM element
    this.domElement.append(this.columnsContainer);
  }

  /**
   * Render a filter bar title with a specified class.
   * @param {string} title - The title text for the filter bar.
   * @param {string} klass - The CSS class to apply to the filter bar.
   * @returns {HTMLElement} The DOM element representing the filter bar title.
   */
  renderFilterBarTitle(title, klass) {
    const labelElement = document.createElement('div');
    labelElement.classList.toggle(`${klass}-filter-label`);
    labelElement.classList.toggle('label');
    labelElement.innerHTML = title;

    return labelElement;
  }

  /**
   * Render a container for a filter bar with a specified class.
   * @param {string} klass - The CSS class to apply to the filter bar container.
   * @returns {HTMLElement} The DOM element representing the filter bar container.
   */
  renderFilterBarContainer(klass) {
    const filtersContainer = document.createElement('div');
    filtersContainer.classList.toggle(`${klass}-filter-container`);
    filtersContainer.classList.toggle('filter-container');

    return filtersContainer;
  }

  /**
   * Render a filter button with a specified title, class, icon class, and initial enabled state.
   * @param {string} title - The title text for the filter button.
   * @param {string} klass - The CSS class to apply to the filter button.
   * @param {string} iconClass - The CSS class representing the icon of the filter button.
   * @param {boolean} isEnabled - The initial enabled state of the filter button.
   * @param {string} colorClass - The CSS class representing the color of the filter button.
   * @returns {HTMLElement} The DOM element representing the filter button.
   */
  renderFilterButton(title, klass, iconClass, isEnabled, colorClass) {
    const button = document.createElement('span');
    if (!iconClass) iconClass = klass;
    button.classList.toggle('button');
    button.classList.toggle(`${klass}-button`);
    if (iconClass) button.classList.toggle(iconClass);
    if (colorClass) button.classList.toggle(colorClass);
    if (isEnabled) button.classList.toggle('enabled');
    button.innerHTML = `<icon class="icon ${iconClass} ${colorClass || ''}">&nbsp;</icon><span class="filter-name">${capitalise(
      splitCamelCased(title)
    )}</span>`;

    return button;
  }

  /**
   * Render the log source filters bar and add event listeners for toggling source visibility.
   */
  renderSourceFiltersBar() {
    this.sourceFilterElement = document.createElement('div');
    this.sourceFilterElement.classList.toggle('source-filter-bar-wrapper');
    this.sourceFilterElement.classList.toggle('filter-bar');

    // Add title to the log source filters bar
    this.sourceFilterElement.append(this.renderFilterBarTitle('Log source filters', 'source'));

    // Create a container for log source filters
    const filtersContainer = this.renderFilterBarContainer('source');
    const that = this;

    // Loop through each log source in the config and render a filter button for it
    this.config.sources.forEach((source) => {
      const sourceButton = that.renderFilterButton(
        source.originalName,
        'source',
        'log',
        source.enabled,
        source.color
      );

      // Add click event listener to toggle source visibility
      sourceButton.onclick = () => {
        sourceButton.classList.toggle('enabled');
        source.enabled = !source.enabled;
        that.eventBroker.dispatchEvent({ eventName: `${source.name.toLowerCase()}SourceVisibility` });
      };

      filtersContainer.append(sourceButton);
    });

    // Append the log source filters bar to the filters container
    this.sourceFilterElement.append(filtersContainer);

    // Append the filters container to the main control panel DOM element
    this.filtersContainer.append(this.sourceFilterElement);
  }

  /**
   * Render the log levels filters bar and add event listeners for toggling log level visibility.
   */
  renderLevelsFiltersBar() {
    // Create a container for log levels filters
    this.levelFilterElement = document.createElement('div');
    this.levelFilterElement.classList.toggle('level-filter-bar-wrapper');
    this.levelFilterElement.classList.toggle('filter-bar');

    // Add title to the log levels filters bar
    this.levelFilterElement.append(this.renderFilterBarTitle('Log levels filters', 'level'));

    // Create a container for log level filters
    const filtersContainer = this.renderFilterBarContainer('level');
    const that = this;

    // Loop through each log level in the config and render a filter button for it
    Object.getOwnPropertyNames(this.config.levelSwitches).forEach((levelName) => {
      const iconName = levelName === 'assertion' ? 'assert-true' : levelName;
      const levelButton = that.renderFilterButton(
        levelName,
        'level',
        iconName,
        that.config.isLevelEnabled(levelName)
      );

      // Add click event listener to toggle log level visibility
      levelButton.onclick = () => {
        levelButton.classList.toggle('enabled');
        that.config.toggleLevel(levelName);
        that.eventBroker.dispatchEvent({ eventName: `${levelName}LevelVisibility` });
      };

      filtersContainer.append(levelButton);
    });

    // Append the log levels filters bar to the filters container
    this.levelFilterElement.append(filtersContainer);

    // Append the filters container to the main control panel DOM element
    this.filtersContainer.append(this.levelFilterElement);
  }

  /**
   * Render the content filters bar and add event listeners for toggling content visibility.
   */
  renderContentFilterBar() {
    // Create a container for content filters
    this.contentFilterElement = document.createElement('div');
    this.contentFilterElement.classList.toggle('content-filter-bar-wrapper');
    this.contentFilterElement.classList.toggle('filter-bar');

    // Add title to the content filters bar
    this.contentFilterElement.append(this.renderFilterBarTitle('Content filters', 'level'));

    // Create a container for content filters
    const filtersContainer = this.renderFilterBarContainer('content');
    const that = this;

    // Loop through each content item in the config and render a filter button for it
    Object.getOwnPropertyNames(this.config.contentSwitches).forEach((contentName) => {
      const contentButton = that.renderFilterButton(
        contentName,
        'content',
        contentName,
        that.config.isContentEnabled(contentName)
      );

      // Add click event listener to toggle content visibility
      contentButton.onclick = () => {
        contentButton.classList.toggle('enabled');
        that.config.toggleContent(contentName);
        that.eventBroker.dispatchEvent({ eventName: `${contentName}ContentVisibility` });
      };

      filtersContainer.append(contentButton);
    });

    // Append the content filters bar to the filters container
    this.contentFilterElement.append(filtersContainer);

    // Append the filters container to the main control panel DOM element
    this.filtersContainer.append(this.contentFilterElement);
  }

  /**
   * Render the column switch bar and add event listeners for toggling column visibility.
   */
  renderColumnsFilterBar() {
    // Create a container for column filters
    this.columnFilterElement = document.createElement('div');
    this.columnFilterElement.classList.toggle('column-filter-bar-wrapper');
    this.columnFilterElement.classList.toggle('filter-bar');

    // Add title to the column switch bar
    this.columnFilterElement.append(this.renderFilterBarTitle('Column switches', 'column'));

    // Create a container for column filters
    const filtersContainer = this.renderFilterBarContainer('column');
    const that = this;

    // Loop through each column in the config and render a filter button for it
    Object.getOwnPropertyNames(this.config.columnsSwitches).forEach((columnName) => {
      const contentButton = that.renderFilterButton(
        columnName,
        'column',
        columnName,
        that.config.isColumnEnabled(columnName)
      );

      // Add click event listener to toggle column visibility
      contentButton.onclick = () => {
        contentButton.classList.toggle('enabled');
        that.config.toggleColumn(columnName);
        that.eventBroker.dispatchEvent({ eventName: `${columnName}ColumnVisibility` });
      };

      filtersContainer.append(contentButton);
    });

    // Append the column switch bar to the column container
    this.columnFilterElement.append(filtersContainer);

    // Append the column container to the main control panel DOM element
    this.columnsContainer.append(this.columnFilterElement);
  }
}

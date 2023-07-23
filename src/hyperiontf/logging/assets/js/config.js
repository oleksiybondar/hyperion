// Constants for sources and colors
const DisabledByDefaultSources = ['selenium', 'appium', 'playwright', 'xdo', 'siculix', 'autoit'];
const ColorsClasses = ['green-color', 'blue-color', 'pink-color', 'gray-color', 'green2-color', 'orange-color',
  'yellow-color', 'purple-color', 'gray2-color', 'red-color'];

/**
 * Config class for managing application configuration, such as log level switches, content switches,
 * column switches, sources, and source colors.
 */
class Config {
  constructor() {
    // Initialize default log level switches
    this.levelSwitches = {
      debug: false,
      info: true,
      warning: false,
      error: true,
      fatal: true,
      assertion: true,
    };

    // Initialize default content switches
    this.contentSwitches = {
      backtrace: true,
      screenSnap: true,
      pageSource: false,
    };

    // Initialize default column switches
    this.columnsSwitches = {
      timestamp: true,
      level: true,
      logger: true,
      sourceCode: false,
    };

    // Initialize an empty array to store sources
    this.sources = [];

    // Initialize the index for the last used color
    this.lastUledCollor = -1;
  }

  /**
   * Add a new source to the configuration.
   * @param {string} source - The name of the source to add.
   */
  addSource(source) {
    const normalizedSource = source.toLowerCase();

    // Check if the source already exists, and if so, return early
    if (this.sources.find((item) => item.name === normalizedSource)) return;

    // Increment the index for the last used color and wrap around if necessary
    this.lastUledCollor += 1;
    if (this.lastUledCollor > ColorsClasses.length - 1) this.lastUledCollor = 0;

    // Create an object representing the new source and add it to the sources array
    const sourceData = {
      name: normalizedSource,
      originalName: source,
      enabled: DisabledByDefaultSources.indexOf(normalizedSource) === -1,
      color: ColorsClasses[this.lastUledCollor],
    };

    this.sources.push(sourceData);
  }

  /**
   * Check if a specific source is enabled.
   * @param {string} source - The name of the source to check.
   * @returns {boolean} True if the source is enabled, false otherwise.
   */
  isSourceEnabled(source) {
    const needed = this.sources.find((item) => item.name === source.toLowerCase());
    if (needed) return needed.enabled;

    // If the source is not found in the sources array, assume it's enabled by default
    return true;
  }

  /**
   * Check if a specific column is enabled.
   * @param {string} column - The name of the column to check.
   * @returns {boolean} True if the column is enabled, false otherwise.
   */
  isColumnEnabled(column) {
    return this.columnsSwitches[column];
  }

  /**
   * Check if a specific log level is enabled.
   * @param {string} level - The log level to check.
   * @returns {boolean} True if the log level is enabled, false otherwise.
   */
  isLevelEnabled(level) {
    // The 'header' level is always enabled
    if (level === 'header') return true;

    return this.levelSwitches[level];
  }

  /**
   * Check if a specific content item is enabled.
   * @param {string} itemName - The name of the content item to check.
   * @returns {boolean} True if the content item is enabled, false otherwise.
   */
  isContentEnabled(itemName) {
    return this.contentSwitches[itemName];
  }

  /**
   * Toggle the state of a specific log level switch.
   * @param {string} level - The log level to toggle.
   */
  toggleLevel(level) {
    this.levelSwitches[level] = !this.levelSwitches[level];
  }

  /**
   * Toggle the state of a specific content switch.
   * @param {string} itemName - The name of the content item to toggle.
   */
  toggleContent(itemName) {
    this.contentSwitches[itemName] = !this.contentSwitches[itemName];
  }

  /**
   * Toggle the state of a specific column switch.
   * @param {string} column - The name of the column to toggle.
   */
  toggleColumn(column) {
    this.columnsSwitches[column] = !this.columnsSwitches[column];
  }

  /**
   * Toggle the state of a specific source.
   * @param {string} source - The name of the source to toggle.
   */
  toggleSource(source) {
    const needed = this.sources.find((item) => item.name === source.toLowerCase());

    // If the source is not found in the sources array, return early
    if (!needed) return;

    // Toggle the enabled state of the source
    needed.enabled = !needed.enabled;
  }

  /**
   * Get the color associated with a specific source.
   * @param {string} source - The name of the source.
   * @returns {string} The color class associated with the source, or the original source name if not found.
   */
  getSourceColor(source) {
    const needed = this.sources.find((item) => item.name === source.toLowerCase());

    // If the source is not found in the sources array, return the original source name
    if (!needed) return source;

    return needed.color;
  }
}

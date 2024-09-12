/**
 * Logger class for rendering and managing the log viewer, including the main header and log lines.
 */
class Logger {
  constructor() {
    // Initialize log data and meta information
    this.lines = [];
    this.meta = {};
    // Create a ControlPanel instance for managing the control panel UI
    this.controlPannel = new ControlPanel();
    // Create a Line instance for the table header line
    this.tableHeaderLine = new Line(this, { msg: 'Log message', lvl: -999, time: 'Timestamp', name: 'Logger', depth: 0 });
    this.wasRendered = false;

    // Read the log data source and update meta information
    this.readLoggerDataSource();
    // Update the page title with the test name and status
    this.updatePageTitle();
    // Render the logger UI
    this.render();
  }

  // Getters for meta information
  get testStatus() {
    return this.meta.testStatus || 'Unknown';
  }

  get testName() {
    return this.meta.testName || 'Test Log';
  }

  get testTags() {
    return this.meta.testTags;
  }

  get statusClass() {
    return `status-${this.testStatus.toLowerCase()}`;
  }

  get testDuration() {
    return this.meta.testDuration;
  }

  get testDescription() {
    return this.meta.testDescription;
  }

  // Read the logger data source (JSON data in NDJSON format) and parse it into log lines
  readLoggerDataSource() {
    const data = readNdJsonData();
    let linesContainer = this;
    data.forEach((logEntry) => {
      if (logEntry.key) {
        // Store meta information from the log data
        this.meta[logEntry.key] = JSON.parse(logEntry.msg);
      } else {
        // Create a Line instance for the log entry and organize it in the lines hierarchy
        const line = new Line(linesContainer, logEntry);
        window.hyperionTestingFrameworkConfig.addSource(line.loggerPackage);

        if (line.depth > (linesContainer.depth || 0)) {
          linesContainer.lines.push(line);
          linesContainer = line;
        } else if (line.depth < (linesContainer.depth || 0)) {
          while (line.depth !== (linesContainer.depth || 0)) linesContainer = linesContainer.parent;
          linesContainer.lines.push(line);
        } else {
          linesContainer.lines.push(line);
        }
      }
    });
  }

  // Update the page title with the test name and status
  updatePageTitle() {
    if (this.meta.testName) {
      document.title = `[${this.testStatus}] ${this.testName} | Hyperion Testing Framework`;
    }
  }

  // Render the logger UI components
  render() {
    if (this.wasRendered) return;

    this.renderHeader();
    this.renderControlPanel();
    this.renderTableHeader();
    this.renderLines();
  }

  // Render a single meta line in the header section
  renderMetaLine(metaKey, title, content, contentClass = '') {
    const metaElement = document.createElement('div');
    metaElement.classList.toggle(`test-${metaKey}-wrapper`);
    metaElement.classList.toggle(`test-meta-field`);
    metaElement.innerHTML = `<div class="test-${metaKey}-label label">${title}</div><div class="test-${metaKey} ${contentClass} value">${content}</div>`;

    this.headerElement.append(metaElement);
  }

  // Render the test title in the header section
  renderTestTitle() {
    if (!this.testName) return;
    this.renderMetaLine('name', 'Test name:', this.testName, this.statusClass);
  }

  // Render the test tags in the header section
  renderTestTags() {
    if (!this.testTags) return;
    const tags = this.testTags.map((tag) => `<span class="tag">${tag}</span>`).join('');
    this.renderMetaLine('tags', 'Test tags:', tags);
  }

  // Render the test description in the header section
  renderTestDescription() {
    if (!this.testDescription) return;
    this.renderMetaLine('description', 'Description:', formatRegularTextToHtml(this.testDescription));
  }

  // Render the test status in the header section
  renderTestStatus() {
    if (!this.testStatus) return;
    this.renderMetaLine('status', 'Status:', this.testStatus.toUpperCase(), this.statusClass);
  }

  // Render the test duration in the header section
  renderTestDuration() {
    if (!this.testDuration) return;
    this.renderMetaLine('duration', 'Duration:', this.testDuration);
  }

  // Render the header section containing meta information about the test
  renderHeader() {
    this.headerElement = document.createElement('div');
    this.headerElement.classList.toggle('test-meta-section');
    this.headerElement.classList.toggle('document-header');

    this.renderTestTitle();
    this.renderTestTags();
    this.renderTestDescription();
    this.renderTestStatus();
    this.renderTestDuration();

    document.body.append(this.headerElement);
  }

  // Render the control panel section for log filters and switches
  renderControlPanel() {
    document.body.append(this.controlPannel.render());
  }

  // Render the table header line
  renderTableHeader() {
    const tableHeader = document.createElement('div');
    tableHeader.classList.toggle('lines-header-wrapper');
    tableHeader.classList.toggle('document-header');
    tableHeader.append(this.tableHeaderLine.render());

    document.body.append(tableHeader);
  }

  // Render the log lines in the main content section
  renderLines() {
    const linesDomElement = document.createElement('div');
    linesDomElement.classList.toggle('main-content');
    document.body.append(linesDomElement);
    this.lines.forEach((line) => {
      if(line.level !== 10000) {
        linesDomElement.append(line.render());
      }
    });
  }
}

// app.js - Entry point of the application

// Import necessary modules
// Assume all required modules are imported here using the 'import' statement

/**
 * The ready function ensures that the DOM is fully loaded before running the application.
 * It is used to invoke the main function of the application once the DOM is ready.
 * @param {Function} fn - The main function of the application
 */
function ready(fn) {
  if (document.readyState !== 'loading') {
    // If the DOM is already loaded, execute the main function immediately
    fn();
    return;
  }
  // If the DOM is still loading, add an event listener to execute the main function
  document.addEventListener('DOMContentLoaded', fn);
}

// The main function of the application
ready(() => {
  window.hyperionTestingFrameworkConfig = new Config();
  window.hyperionTestingFrameworkEventBrocker = new EventBroker();
  window.hyperionTestingFrameworkLogger = new Logger();
});
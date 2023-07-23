/**
 * EventBroker class for managing event subscriptions and dispatching events
 */
class EventBroker {
  constructor() {
    // Initialize an array to store event subscriptions
    this.subscriptions = [];
  }

  /**
   * Dispatch an event to all subscribers with matching event names.
   * @param {object} eventData - The event data to be dispatched to subscribers.
   */
  dispatchEvent(eventData) {
    // Loop through all subscriptions and call the callback function for matching event names
    this.subscriptions.forEach((subscription) => {
      if (subscription.eventName === eventData.eventName) {
        // Call the subscriber's callback function with the event data
        subscription.subscriber[subscription.callback](eventData);
      }
    });
  }

  /**
   * Subscribe to an event by providing the event name, subscriber, and callback function name.
   * @param {string} eventName - The name of the event to subscribe to.
   * @param {object} subscriber - The object subscribing to the event.
   * @param {string} callbackFunctionName - The name of the callback function on the subscriber object.
   */
  subscribe(eventName, subscriber, callbackFunctionName) {
    // Add a new subscription to the subscriptions array
    this.subscriptions.push({ eventName: eventName, subscriber: subscriber, callback: callbackFunctionName });
  }
}

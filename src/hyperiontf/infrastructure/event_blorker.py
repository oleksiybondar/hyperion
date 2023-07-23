from typing import Callable, Dict, List, Any


class EventBroker:
    """
    EventBroker is a mediator that handles communication between different components
    of an application. It holds a map of event types to event listeners. When an event
    is published to the EventBroker, it notifies all registered listeners for the event.

    The main benefit of using an EventBroker is to reduce the coupling between different
    parts of an application. With an EventBroker, components can communicate indirectly,
    without needing to hold explicit references to each other.
    """

    def __init__(self):
        """
        Initializes a new instance of EventBroker.
        """
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """
        Registers a callback to be called when an event of the given type is published.

        :param event_type: The type of the event to subscribe to.
        :param callback: The function to call when the event is published. The function
            should take a single argument, which is the data associated with the event.
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data):
        """
        Publishes an event of the given type to all registered listeners.

        :param event_type: The type of the event to publish.
        :param data: The data to associate with the event.
        """
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)

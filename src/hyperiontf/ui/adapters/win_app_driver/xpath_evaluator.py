from lxml import etree
from command.driver import source


class XPathEvaluator:
    """
    XPathEvaluator provides a custom implementation of an XPath engine for the WindowsApplicationDriver client.
    This class enhances the native WinAppDriver XPath engine by enabling searches from an element context and supporting
    complex XPath expressions, including axes that are not available natively in WinAppDriver.

    Attributes:
        bridge (object): A bridge instance responsible for executing commands, managing sessions, and communicating with the WinAppDriver.
                         It is also responsible for converting raw XPath results into a usable format (e.g., a list of element instances).
    """

    def __init__(self, bridge):
        """
        Initializes the XPathEvaluator with a bridge instance.

        Args:
            bridge (object): A bridge object that manages communication between the framework and the WinAppDriver server.
                             It provides access to execute commands and retrieve session-specific information, and it handles
                             conversion of raw results into the expected element format.
        """
        self.bridge = bridge

    def find_elements(self, xpath: str, base_element=None):
        """
        Finds elements in the document or within a base element's context using the provided XPath expression.

        This method determines whether the XPath expression should be evaluated globally (from the document root) or
        locally (relative to a base element). The results are processed via the `bridge` to return elements in the
        framework's expected format.

        Args:
            xpath (str): The XPath expression used to search for elements. If it starts with '//', the search is global.
            base_element (optional): The base element to search within. If provided, the search will be scoped to descendants
                                     of this element. If not provided, the search will be global.

        Returns:
            list: A list of elements found by the XPath query, processed and converted into the framework's format.
                  Each element is processed by the `bridge.process_value` method.
        """
        if xpath.startswith("//"):
            context = self.document
        else:
            context = self._fetch_context(base_element)
        nodes = self._query_xpath(xpath, context)
        return self.bridge.process_value(self._nodes_to_response_format(nodes))

    def _query_xpath(self, xpath: str, context=None):
        """
        Executes an XPath query within the specified context (defaulting to the entire document).

        This method performs the actual query on the given context node using the `lxml.etree` XPath engine.
        If no context is provided, the query is executed on the entire document.

        Args:
            xpath (str): The XPath expression to evaluate.
            context (optional): The XML node (context) in which to evaluate the XPath. If None, the document root is used.

        Returns:
            list: A list of XML nodes found by the XPath query. These nodes are later converted to the framework-specific format.
        """
        if context is None:
            context = self.document
        return context.xpath(xpath)

    def _fetch_context(self, base_element=None):
        """
        Retrieves the context node (element) to be used as the base for further XPath queries.

        If a `base_element` is provided, this method fetches the context node for the element using its `RuntimeId`.
        The WinAppDriver does not natively support element-scoped XPath queries, so this method locates the element
        in the document using its unique identifier.

        Args:
            base_element (optional): The base element whose context is to be fetched. If None, the document root is returned.

        Returns:
            etree.Element: The context element to be used for subsequent XPath queries.
        """
        if base_element is None:
            return self.document

        xpath = f'//*[@RuntimeId="{base_element.element_id}"]'
        return self._query_xpath(xpath)[0]

    @property
    def document(self):
        """
        Retrieves the XML representation of the current page or application state from the WinAppDriver.

        This property fetches the full document source (in XML format) by executing the appropriate command via the `bridge`.
        It then parses the XML string into an `lxml.etree.Element` object for use in XPath queries.

        Returns:
            etree.Element: The root element of the XML document representing the current page or app state.
        """
        source_xml = self.bridge.execute(source, {"sessionId": self.bridge.session_id})
        return etree.fromstring(source_xml)

    @staticmethod
    def _nodes_to_response_format(nodes):
        """
        Converts a list of XML nodes into a framework-specific format.

        This method extracts the 'RuntimeId' attribute from each XML node and formats it into a dictionary with the key 'ELEMENT',
        which is expected by the framework. The resulting list is then processed by the `bridge` to convert these raw results
        into proper element instances.

        Args:
            nodes (list): A list of XML nodes returned by an XPath query.

        Returns:
            list: A list of dictionaries where each dictionary represents an element with the 'RuntimeId' as the 'ELEMENT' key.
        """
        return [{"ELEMENT": node.get("RuntimeId")} for node in nodes]

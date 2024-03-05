from hyperiontf.typing import HyperionUIException
from hyperiontf.logging import getLogger


def error_recovery(logger=getLogger("Element")):
    def inner_decorator(method):
        def decorator(*args, **kwargs):
            instance = args[0]
            # ensure that action can be performed
            instance.__is_interactive__()
            try:
                # try to execute requested action
                return method(*args, **kwargs)
            except HyperionUIException as uie:
                logger.debug(
                    f"[{instance.__full_name__}] Exception intercepted! {uie.__class__.__name__}: {str(uie)}"
                )
                # TODO: process more exception
                match uie.__class__.__name__:
                    case "StaleElementReferenceException" | "NoSuchElementException":
                        # This handles an edge case where a NoSuchElementException is raised for elements in a
                        # different context or when they are not accurately mapped at the adapter end due to changes
                        # in the messaging patterns of newer versions. Under these circumstances, if the target
                        # element was not previously found (indicating that it truly does not exist rather than being
                        # a stale reference issue), a NoSuchElementException is raised. This logic helps
                        # differentiate between genuine absence and context-related or mapping errors.
                        if (
                            uie.__class__.__name__ == "NoSuchElementException"
                            and not instance.__is_present__()
                        ):
                            raise uie

                        # try search element again, if parent element is stale then it will be retried as well as part
                        # of find_itself sequence, given that StaleElementReferenceError occurs during element search
                        # then the same command will be chained to its parent until all chain is resolved or no more
                        # retry attempts left
                        if (
                            hasattr(instance.parent, "contains_multiple_elements")
                            and instance.parent.contains_multiple_elements
                        ):
                            # for an elements we have to always refresh parent one and then re-fetch the element
                            # instance
                            instance.parent.find_itself()

                        instance.find_itself()
                        # ensure that action can be performed, before re-try
                        instance.__is_interactive__()
                        # Retrying, without exception handling
                        return method(*args, **kwargs)
                    case "ContextSwitchingException":
                        instance.document_holder.__resolve__()
                        return decorator(*args, **kwargs)

                    case _:
                        # re-raise exception as it's not something we can handle here
                        raise uie

        return decorator

    return inner_decorator

from typing import Optional, Dict, Any
import copy
from .section import Section
from ..helpers.dict_heplers import transform_keys_to_camel_case


class Capabilities(Section):
    def build_caps(
        self,
        user_caps: Optional[Dict[Any, Any]] = None,
        camel_case_keys: Optional[bool] = True,
    ) -> Dict[Any, Any]:
        if user_caps is None:
            user_caps = {}
        # ensure that outer dictionary will not mutate, because of further caps processing
        copied_caps = copy.deepcopy(user_caps)
        if not camel_case_keys:
            return {**self.to_dict(), **copied_caps}

        camel_cased_caps = transform_keys_to_camel_case(self.to_dict())

        return {**camel_cased_caps, **copied_caps}

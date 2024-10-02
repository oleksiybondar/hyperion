appium_app_launch = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/appium/app/launch",
}
appium_app_close = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/appium/app/close",
}
back = {"method": "POST", "endpointTemplate": "/session/{sessionId}/back"}
find_element = {"method": "POST", "endpointTemplate": "/session/{sessionId}/element"}
find_elements = {"method": "POST", "endpointTemplate": "/session/{sessionId}/elements"}
active_element = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/element/active",
}
forward = {"method": "POST", "endpointTemplate": "/session/{sessionId}/forward"}
location = {"method": "GET", "endpointTemplate": "/session/{sessionId}/location"}
orientation = {"method": "GET", "endpointTemplate": "/session/{sessionId}/orientation"}
screenshot = {"method": "GET", "endpointTemplate": "/session/{sessionId}/screenshot"}
source = {"method": "GET", "endpointTemplate": "/session/{sessionId}/source"}
timeouts = {"method": "POST", "endpointTemplate": "/session/{sessionId}/timeouts"}
title = {"method": "GET", "endpointTemplate": "/session/{sessionId}/title"}

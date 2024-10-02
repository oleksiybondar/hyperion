delete_window = {"method": "DELETE", "endpointTemplate": "/session/{sessionId}/window"}
new_window = {"method": "POST", "endpointTemplate": "/session/{sessionId}/window"}
maximize = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/window/maximize",
}
size = {"method": "GET", "endpointTemplate": "/session/{sessionId}/window/size"}
set_size = {"method": "POST", "endpointTemplate": "/session/{sessionId}/window/size"}
set_window_handle_size = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/window/{windowHandle}/size",
}
get_window_handle_size = {
    "method": "GET",
    "endpointTemplate": "/session/{sessionId}/window/{windowHandle}/size",
}
set_position = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/window/{windowHandle}/position",
}
get_position = {
    "method": "GET",
    "endpointTemplate": "/session/{sessionId}/window/{windowHandle}/position",
}
maximize_window_handle = {
    "method": "POST",
    "endpointTemplate": "/session/{sessionId}/window/{windowHandle}/maximize",
}
handle = {"method": "GET", "endpointTemplate": "/session/{sessionId}/window_handle"}
handles = {"method": "GET", "endpointTemplate": "/session/{sessionId}/window_handles"}

import re

ansi_sequences = [
    "\x1b[0m",  # Reset / Normal
    "\x1b[1m",  # Bold
    "\x1b[3m",  # Italic
    "\x1b[4m",  # Underline
    "\x1b[7m",  # Reverse
    "\x1b[8m",  # Conceal
    "\x1b[9m",  # Strikethrough
    "\x1b[30m",  # Set text color to black
    "\x1b[31m",  # Set text color to red
    "\x1b[32m",  # Set text color to green
    "\x1b[33m",  # Set text color to yellow
    "\x1b[34m",  # Set text color to blue
    "\x1b[35m",  # Set text color to magenta
    "\x1b[36m",  # Set text color to cyan
    "\x1b[37m",  # Set text color to white
    "\x1b[90m",  # Set text color to bright black (gray)
    "\x1b[91m",  # Set text color to bright red
    "\x1b[92m",  # Set text color to bright green
    "\x1b[93m",  # Set text color to bright yellow
    "\x1b[94m",  # Set text color to bright blue
    "\x1b[95m",  # Set text color to bright magenta
    "\x1b[96m",  # Set text color to bright cyan
    "\x1b[97m",  # Set text color to bright white
    "\x1b[40m",  # Set background color to black
    "\x1b[41m",  # Set background color to red
    "\x1b[42m",  # Set background color to green
    "\x1b[43m",  # Set background color to yellow
    "\x1b[44m",  # Set background color to blue
    "\x1b[45m",  # Set background color to magenta
    "\x1b[46m",  # Set background color to cyan
    "\x1b[47m",  # Set background color to white
    "\x1b[100m",  # Set background color to bright black (gray)
    "\x1b[101m",  # Set background color to bright red
    "\x1b[102m",  # Set background color to bright green
    "\x1b[103m",  # Set background color to bright yellow
    "\x1b[104m",  # Set background color to bright blue
    "\x1b[105m",  # Set background color to bright magenta
    "\x1b[106m",  # Set background color to bright cyan
    "\x1b[107m",  # Set background color to bright white
    "\x1b[K",  # Erase to end of line
    "\x1b[J",  # Erase to end of display
    "\x1b[?2004h",  # Enable bracketed paste mode
    "\x1b[?2004l",  # Disable bracketed paste mode
    "\x1b[m",
]


# Example of removing ANSI sequences using str.replace
def remove_ansi_sequences(text: str) -> str:
    for ansi in ansi_sequences:
        text = text.replace(ansi, "")
    text = text.replace("\r\r", "\r")
    text = text.replace("\r \r", "\r")
    text = re.sub(r".\x08", "", text)
    return text

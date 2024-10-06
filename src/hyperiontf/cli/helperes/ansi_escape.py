import re

ansi_sequences = [
    "\x1B[0m",  # Reset / Normal
    "\x1B[1m",  # Bold
    "\x1B[3m",  # Italic
    "\x1B[4m",  # Underline
    "\x1B[7m",  # Reverse
    "\x1B[8m",  # Conceal
    "\x1B[9m",  # Strikethrough
    "\x1B[30m",  # Set text color to black
    "\x1B[31m",  # Set text color to red
    "\x1B[32m",  # Set text color to green
    "\x1B[33m",  # Set text color to yellow
    "\x1B[34m",  # Set text color to blue
    "\x1B[35m",  # Set text color to magenta
    "\x1B[36m",  # Set text color to cyan
    "\x1B[37m",  # Set text color to white
    "\x1B[90m",  # Set text color to bright black (gray)
    "\x1B[91m",  # Set text color to bright red
    "\x1B[92m",  # Set text color to bright green
    "\x1B[93m",  # Set text color to bright yellow
    "\x1B[94m",  # Set text color to bright blue
    "\x1B[95m",  # Set text color to bright magenta
    "\x1B[96m",  # Set text color to bright cyan
    "\x1B[97m",  # Set text color to bright white
    "\x1B[40m",  # Set background color to black
    "\x1B[41m",  # Set background color to red
    "\x1B[42m",  # Set background color to green
    "\x1B[43m",  # Set background color to yellow
    "\x1B[44m",  # Set background color to blue
    "\x1B[45m",  # Set background color to magenta
    "\x1B[46m",  # Set background color to cyan
    "\x1B[47m",  # Set background color to white
    "\x1B[100m",  # Set background color to bright black (gray)
    "\x1B[101m",  # Set background color to bright red
    "\x1B[102m",  # Set background color to bright green
    "\x1B[103m",  # Set background color to bright yellow
    "\x1B[104m",  # Set background color to bright blue
    "\x1B[105m",  # Set background color to bright magenta
    "\x1B[106m",  # Set background color to bright cyan
    "\x1B[107m",  # Set background color to bright white
    "\x1B[K",  # Erase to end of line
    "\x1B[J",  # Erase to end of display
    "\x1B[?2004h",  # Enable bracketed paste mode
    "\x1B[?2004l",  # Disable bracketed paste mode
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

import shutil
from pathlib import Path
from .file import File


class Dir:
    """
    A convenience wrapper class around Python's built-in directory handling functionality.

    The Dir class is designed to simplify interactions with the filesystem, specifically with directories,
    by providing an intuitive and object-oriented interface for common directory operations. This class
    enhances the usability and manageability of directory-related tasks within applications and testing
    frameworks. Key motivations for the Dir class include:

    1. Encapsulation: Simplify directory operations by encapsulating common tasks such as checking existence,
       creation, deletion, and listing contents within a cohesive object. This approach promotes code
       readability and reusability.

    2. Unified Interface: Offer a unified and straightforward interface for directory manipulations, abstracting
       away the complexities of the underlying filesystem operations. This includes handling directories in a
       cross-platform manner, easing the development process.

    3. Integration with Testing: Initially designed to support the 'expect' functionality and FileSystem strategy
       within a testing framework, the Dir class facilitates the setup and teardown of test environments by
       managing directory structures and contents efficiently.

    4. Absence of Built-in Abstraction: While Python provides modules like os and pathlib for filesystem
       operations, there's a lack of a high-level, object-oriented directory management class. The Dir class
       fills this gap, aligning with the design principles of Python's standard library while adding
       additional convenience.

    5. Future-proofing: By wrapping directory operations within the Dir class, applications and frameworks
       can insulate themselves from potential future changes to Python's directory handling functions.
       This class acts as an abstraction layer, minimizing the impact of underlying API changes.

    The Dir class does not reinvent directory handling but rather aims to enhance its accessibility and
    adaptability for application development and testing, providing a robust and flexible tool for
    filesystem management.
    """

    def __init__(self, path):
        """
        Initializes a new instance of the Dir class with a specific directory path.

        Args:
            path (str or Path): The filesystem path to the directory. This can be an absolute or relative path.
                                If a string is provided, it will be converted to a Path object for internal use.
        """
        self.path = Path(path)

    def exists(self):
        """
        Check if the directory exists.
        """
        return self.path.exists() and self.path.is_dir()

    def create(self):
        """
        Create the directory. If the directory already exists, this method does nothing.
        """
        self.path.mkdir(parents=True, exist_ok=True)

    def delete(self, force=False):
        """
        Delete the directory. If force is True, delete all its contents first.

        Args:
            force (bool): If True, forcefully delete the directory and all its contents.
        """
        if force:
            shutil.rmtree(self.path)
        else:
            self.path.rmdir()

    def list_content(self):
        """
        List all content of the directory, returning lists of File and Dir objects.

        Returns:
            tuple: A tuple containing two lists - the first with Dir objects for each subdirectory,
                   and the second with File objects for each file in the directory.
        """
        dirs = [Dir(child) for child in self.path.iterdir() if child.is_dir()]
        files = [File(child) for child in self.path.iterdir() if child.is_file()]
        return (dirs, files)

    def size(self):
        """
        Calculate the total size of the directory by aggregating the sizes of all files within it.

        Returns:
            int: The total size of the directory in bytes.
        """
        total_size = 0
        for child in self.path.rglob("*"):
            if child.is_file():
                total_size += child.stat().st_size
        return total_size

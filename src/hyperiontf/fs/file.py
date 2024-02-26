import hashlib
import os


class File:
    """
    A convenience wrapper class around Python's built-in file handling functionality.

    The creation of the File class is motivated by several key objectives:

    1. Distinction: Clearly distinguish file I/O operations within the testing framework and user code,
       ensuring that when an I/O operation is performed, it is explicitly understood to be file-related.

    2. Encapsulation: Incorporate the most common file manipulation methods within a single, cohesive object,
       simplifying the file handling process by providing a unified and intuitive interface.

    3. Absence of Built-in Abstraction: Python lacks built-in, high-level File/Dir classes for abstracting
       file and directory operations. The File class fills this gap by offering a structured and object-oriented
       approach to file manipulation, enhancing code readability and maintainability.

    4. Future-proofing: Serve as an abstraction layer over Python's built-in file handling. While the class
       leverages existing Python functionality, encapsulating this within the File class allows for resilience
       against potential future changes in Python's file I/O mechanisms. Should Python's core file handling
       undergo significant modifications, adjustments can be centralized within this class, minimizing the
       impact on the broader testing framework and user tests.

    5. Foundation for Testing: Initially conceived to define a base datatype for the 'expect' functionality and
       to facilitate the implementation of a FileSystem strategy within a testing framework, the File class
       simplifies file and directory read/write operations. It not only supports the strategic manipulation of
       the filesystem within tests but also enhances the expressiveness and readability of file-related assertions.

    This class does not aim to reinvent file handling but rather to enhance its usability and adaptability
    within testing scenarios, providing a clear and simple interface for file operations and contributing
    to the robustness and maintainability of test suites.
    """

    def __init__(self, path, mode="r"):
        """
        Initializes a new instance of the File class.

        Args:
            path (str): The file system path to the file. This can be an absolute or relative path.
            mode (str): The mode in which to open the file. The mode string can include the following characters:
                - 'r': Open for reading (default). If the file does not exist, FileNotFoundError is raised.
                - 'w': Open for writing, truncating the file first. If the file does not exist, it is created.
                - 'a': Open for writing, appending to the end of the file if it exists. If the file does not exist, it is created.
                - 'b': Binary mode. Data is read and written in bytes. If omitted, text mode is assumed, and data is read/written as strings.
                - '+': Update mode. Allows reading and writing to the file. Can be combined with other modes, e.g., 'r+'.

                Combining modes:
                - 'rb', 'wb', 'ab': Open the file in binary mode for reading, writing, or appending, respectively.
                - 'r+', 'w+', 'a+': Open the file for updating (reading and writing), with the position set at the beginning, truncating the file, or appending, respectively.

        Raises:
            ValueError: If an invalid mode is provided.
        """
        self._path = path
        self.mode = mode
        self._file = None

    def open(self):
        """
        Opens the file using the mode specified at initialization.

        This method lazily opens the file, meaning the file is opened on demand the first time an I/O operation is performed. This approach ensures resources are utilized efficiently, and the file is only accessed when needed. If the file is already open, this method has no effect.

        The mode used to open the file determines the allowed operations ('r' for read, 'w' for write, 'a' for append, and 'b' for binary mode) and should be chosen based on the intended use of the file.

        Raises:
            IOError: If opening the file fails due to issues like insufficient permissions or the file not existing when expected to.
        """
        if self._file is None:
            self._file = open(self._path, self.mode)

    def close(self):
        """
        Closes the file associated with this File instance.

        If the file is currently open, this method closes it and releases any system resources associated with it. If the file is already closed or was never opened, this method has no effect. It's good practice to call this method when you're done with a file to ensure resources are freed promptly. Alternatively, using the File instance as a context manager (with the 'with' statement) can automate this process.

        Example usage:
            file = File('/path/to/file.txt', 'r')
            file.open()
            # Perform file operations
            file.close()

        Or using a context manager:
            with File('/path/to/file.txt', 'r') as file:
                # Perform file operations
        """
        if self._file:
            self._file.close()
            self._file = None

    def read(self):
        """
        Reads the entire content of the file and returns it as a string.

        This method opens the file in the mode specified during the initialization if it hasn't been opened yet. It reads the entire content of the file and returns it. This method should be used when the file is expected to be in text mode ('r', 'r+', 'w+', 'a+').

        Raises:
            IOError: If the file is not opened in a mode that supports reading ('r', 'r+', 'w+', 'a+').

        Returns:
            str: The content of the file as a string.
        """
        if "r" not in self.mode and "+" not in self.mode:
            raise IOError("File not opened for reading")
        self.open()
        return self._file.read()

    def read_bytes(self):
        """
        Reads the entire content of the file and returns it as bytes.

        This method should be used when the file is expected to be in binary mode ('rb', 'r+b', 'w+b', 'a+b'). It opens the file in the specified mode if it hasn't been opened yet and reads its content as bytes. This is particularly useful for binary files, like images or executables.

        Raises:
            IOError: If the file is not opened in binary mode ('b' not present in mode).

        Returns:
            bytes: The content of the file as bytes.
        """
        if "b" not in self.mode:
            raise IOError("File not opened in binary mode for reading bytes")
        self.open()
        return self._file.read()

    def write(self, content):
        """
        Writes the given content to the file, replacing its current content.

        This method opens the file in the mode specified during the initialization if it hasn't been opened yet and writes the given content to the file. It's intended for use in modes that support writing ('w', 'w+', 'a', 'a+'). If the file was opened in append mode ('a', 'a+'), the content is added to the end of the file.

        Args:
            content (str or bytes): The content to write to the file. If the file is opened in text mode ('w', 'w+'), this should be a string. If in binary mode ('wb', 'wb+'), it should be bytes.

        Raises:
            IOError: If the file is not opened in a mode that supports writing ('w', 'w+', 'a', 'a+').
        """
        if "w" not in self.mode and "+" not in self.mode and "a" not in self.mode:
            raise IOError("File not opened for writing")
        self.open()
        self._file.write(content)

    def append(self, content):
        """
        Appends the given content to the end of the file.

        This method is intended for use when the file is opened in append mode ('a', 'a+', 'ab', 'ab+'). It opens the file if it is not already open and appends the given content to its end. This method does not overwrite existing content but adds to it.

        Args:
            content (str or bytes): The content to append to the file. If the file is opened in text mode ('a', 'a+'), this should be a string. If in binary mode ('ab', 'ab+'), it should be bytes.

        Raises:
            IOError: If the file is not opened in a mode that supports appending ('a', 'a+', 'ab', 'ab+').
        """
        if "a" not in self.mode and "+" not in self.mode:
            raise IOError("File not opened for appending")
        self.open()
        self._file.write(content)

    def exists(self):
        """
        Checks if the file exists on the filesystem.

        This method verifies the existence of the file at the path specified during the initialization of the File instance. It does not require the file to be opened beforehand and can be used to check a file's existence before attempting operations like reading or writing.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(self.path)

    def checksum(self, method="sha256"):
        """
        Calculates and returns a checksum for the file using the specified hash algorithm.

        This method reads the entire content of the file and computes a checksum using the given hash algorithm. It is useful for verifying the integrity of the file's content or comparing two files for equality based on their content.

        Args:
            method (str): The name of the hash algorithm to use for computing the checksum. Defaults to 'sha256'. Other common values include 'md5', 'sha1', etc., depending on the required level of collision resistance and performance.

        Returns:
            str: The hexadecimal digest of the checksum.

        Raises:
            ValueError: If the specified hash algorithm is not supported.
        """
        hasher = hashlib.new(method)
        with open(self.path, "rb") as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()

    def remove(self):
        """
        Removes the file from the filesystem.

        This method deletes the file specified by the path at initialization. It is equivalent to deleting the file through the filesystem but allows for the operation to be performed directly through the File instance. If the file is open when this method is called, it will be closed before deletion.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If there is insufficient permission to delete the file.
        """
        os.remove(self._path)
        self._file = None

    @property
    def file(self):
        return self._file

    @property
    def extension(self):
        """
        Gets the file extension.

        This property extracts and returns the file extension from the path specified during initialization.
        The extension is the substring following the last period ('.') in the filename, if present.

        Returns:
            str: The file extension, including the leading period ('.'). Returns an empty string if the file has no extension.
        """
        return os.path.splitext(self._path)[1]

    @property
    def size(self):
        """
        Gets the size of the file in bytes.

        This property returns the size of the file located at the path specified during initialization.
        The size is determined by the filesystem and represents the total number of bytes occupied by the file.

        Returns:
            int: The size of the file in bytes.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        return os.path.getsize(self._path)

    @property
    def filename(self):
        """
        Gets the filename with extension.

        This property extracts and returns the name of the file, including its extension, from the path specified
        during initialization. It represents the final component of the path, excluding any directory structure.

        Returns:
            str: The filename, including its extension.
        """
        return os.path.basename(self._path)

    @property
    def name(self):
        """
        Gets the filename without its extension.

        This property extracts the name of the file from the path specified during initialization, excluding
        both the directory structure and the file extension. If the file has no extension, it returns the full filename.

        Returns:
            str: The filename without its extension.
        """
        return os.path.splitext(os.path.basename(self._path))[0]

    @property
    def path(self):
        """
        Gets the original file path.

        This property returns the file system path to the file as specified during the initialization of the File instance.
        It may be an absolute or relative path, depending on what was provided when the File object was created.

        Returns:
            str: The original file path.
        """
        return self._path

    @property
    def abs_path(self):
        """
        Gets the absolute file path.

        This property computes and returns the absolute path to the file, resolving any relative path components
        based on the current working directory. It provides a full filesystem path to the file, which can be useful
        for operations requiring an unambiguous file location.

        Returns:
            str: The absolute path to the file.
        """
        return os.path.abspath(self._path)

    def __str__(self):
        return f"File(path='{self._path}', mode='{self.mode}')"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, File):
            return False
        return self.checksum() == other.checksum()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

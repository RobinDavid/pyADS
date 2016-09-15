pyADS
=====

Python module to manipulate NTFS Alternate Data Stream (ADS) of files and directories in Python.

How it works?
-------------

On Windows Vista, Windows Server 2003 and later, NTFS Alternate Data Streams can be accessed using the
FindFirstStreamW and FindNextStreamW functions. So this module is a direct interface to this function
using ctypes and the kernel32 function.
The functionalities are:

* List Alternate streams
* Add a stream to a file
* Remove a stream from a file
* Extract a stream from a file

Methods
-------

All methods are grouped in an ADS class that allow doing multiple operations on the given file.
Available methods are:

* **getFileName** return the file name on which the ADS manager belong to
* **getStreams** return a list of streams names
* **containStreams** return True if the file have alternate Streams
* **addStream** allow to add a stream to the file
* **removeStream** remove the given stream of the file
* **getStreamContent** return the content of the given stream
* **extractStream** extract the content of a stream in file with the same name
* **extractAllStreams** quick way to extract all stream attached to a file


Basic example
-------------

    >>> from pyads import ADS
    >>> file = "myfile.txt"

    >>> handler = ADS(file)
    >>> if handler.containStreams():
    ...     for stream in handler.getStreams():
    ...         print stream
    ...
    helloworld.txt
    secondfile.jpg

    >>> fh = open("attached.txt","w").write("This is the content of an attached file.")
    >>> fh.close()
    >>> handler.addStream("attached.txt")
    True
    >>> handler.getStreams()
    [u'helloworld.txt', u'secondfile.jpg', 'attached.txt']
    >>> print handler.getStreamContent("attached.txt")
    This is the content of an attached file.

    >>> handler.removeStream("attached.txt")
    True
    >>> handler.getStreams()
    [u'helloworld.txt', u'secondfile.jpg']

License
-------

This software is MIT-Licensed

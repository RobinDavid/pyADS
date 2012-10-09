pyADS
=====

Python module to manipulate NTFS Alternate Data Stream (ADS) of files and directories in Python.
Article link: http://robindavid.comli.com/pyads/

How it works?
-------------

On Windows Vista, Windows Server 2003 and later, NTFS Alternate Data Streams can be accessed using the
FindFirstStreamW and FindNextStreamW functions. So this module is a direct interface to this function
using ctypes.
The functionalities are:

* List Alternate streams
* Add a stream to a file
* Remove a stream from a file
* Extract a stream from a file


Basic example
-------------

    >>> from pyads import ADS
    >>> file = "myfile.txt"

    >>> handler = ADSStream(file)
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
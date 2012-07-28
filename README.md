pyADS
=====

Python module to manipulate Windows Alternate Data Stream (ADS) in Python.
Article link: http://robindavid.comli.com/pyads/

How it works?
-------------

To access Alternate Data Streams of NTFS almost the only function(if not the only) is FindFirstStreamW
of Windows. So this module is a direct interface to this function using ctypes.
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
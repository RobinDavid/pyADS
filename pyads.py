from ctypes import *

import sys, os
kernel32 = windll.kernel32

LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 164
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]

class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]

class WIN32_FIND_STREAM_DATA(Structure):
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]
    '''
    typedef struct _WIN32_FIND_STREAM_DATA {
      LARGE_INTEGER StreamSize;
      WCHAR         cStreamName[MAX_PATH + 36];
    } WIN32_FIND_STREAM_DATA, *PWIN32_FIND_STREAM_DATA;
    ''' 

class ADS():
    def __init__(self, file):
        self.filename = file
        self.streams = self.retrieveStreams()
          
        
    def retrieveStreams(self):
        file_infos = WIN32_FIND_STREAM_DATA()
        streamlist = list()
        myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)
        '''
        HANDLE WINAPI FindFirstStreamW(
          __in        LPCWSTR lpFileName,
          __in        STREAM_INFO_LEVELS InfoLevel, (0 standard, 1 max infos)
          __out       LPVOID lpFindStreamData, (return information about file in a WIN32_FIND_STREAM_DATA if 0 is given in infos_level
          __reserved  DWORD dwFlags (Reserved for future use. This parameter must be zero.) cf: doc
        );
        http://msdn.microsoft.com/en-us/library/aa364424(v=vs.85).aspx
        '''
        
        if not file_infos.cStreamName:
            return streamlist #directories don't have default ADS
        else:
            streamname = file_infos.cStreamName.split(":")[1]
            if streamname: streamlist.append(streamname)
        
            while kernel32.FindNextStreamW(myhandler, byref(file_infos)):
                streamlist.append(file_infos.cStreamName.split(":")[1])

        return streamlist
    
    def getFileName(self):
        return self.filename
    
    def getStreams(self):
        return self.streams
    
    def containStreams(self):
        return len(self.getStreams()) != 0
    
    def addStream(self,newfile):
        #Read in the file content
        if not os.path.exists(newfile):
            return False
        if os.path.exists("%s:%s" % (self.filename, newfile)):
            print "A Stream with the same name already exist."
            return False
        
        fd = open(newfile, "rb")
        content = fd.read()
        fd.close()
        #Now write it as stream ADS
        fd = open("%s:%s" % (self.filename, newfile), "wb")
        fd.write(content)
        fd.close()
        self.streams.append(newfile)
        return True
    
    def removeStream(self,stream):
        try:
            os.remove("%s:%s" % (self.filename, stream))
            self.streams.remove(stream)
            return True
        except Exception as e:
            return False
    
    def getStreamContent(self,stream):
        fd = open("%s:%s" %(self.filename, stream), "rb")
        content = fd.read()
        fd.close()       
        return content
    
    def extractStream(self, stream):
        fd = open("%s:%s" %(self.filename, stream), "rb")
        content = fd.read()
        fd.close()
        if not os.path.exists(stream):
            fd = open(stream, "wb")
            fd.write(content)
            fd.close()
        else:
            print "File with the same name already exist"
    
    def extractAllStreams(self):
        for s in self.streams:
            self.extractStream(s)    
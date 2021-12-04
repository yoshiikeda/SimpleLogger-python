import sys

from simple_logger_common import DomainError
from simple_logger_log import Log


class Logger:
    def __init__(self, threshold_):
        if threshold_ not in Log().Severity:
            raise DomainError()
        
        self._threadhold = threshold_
        
        
    def Close(self):
        pass
    
    
    def Write(self, severity_, content_):
        pass
    
    
class NullLogger(Logger):
    pass


class ConsoleLogger(Logger):
    CONSTANTS = { 'pipe': { Log().Severity.Trace: sys.stdout,
                            Log().Severity.Debug: sys.stdout,
                            Log().Severity.Info: sys.stdout,
                            Log().Severity.Warning: sys.stdout,
                            Log().Severity.Error: sys.stderr,
                            Log().Severity.Alert: sys.stderr,
                            Log().Severity.Critical: sys.stderr,
                            Log().Severity.Fatal: sys.stderr,
                            Log().Severity.Emergency: sys.stderr } }
    
    def __init__(self, threshold_, *, upward=True):
        super().__init__(threshold_)
        
        self._upward = upward
        
        
    def Write(self, severity_, content_):
        if self._upward:
            if Log().Severity[self._threshold] <= Log().Severity[severity_]:
                print(content_,
                      file=self.CONSTANTS['pipe'][severity_],
                      flush=True)
                
            else:
                # Empty
                pass
            
        else:
            if Log().Severity[severity_] <= Log().Severity[self._threshold]:
                print(content_,
                      file=self.CONSTANTS['pipe'][severity_],
                      flush=True)
                
            else:
                # Empty
                pass
            
            
class FileLogger(Logger):
    def __init__(self, threshold_, file_):
        super().__init__(threshold_)
        
        try:
            self._file = open(file_, 'wt')
            
        except Exception as ex_:
            raise
        
        
    def Close(self):
        self._file.close()
        
        
    def Write(self, severity_, content_):
        try:
            if Log().Severity[self._threshold] <= Log().Severity[severity_]:
                print(content_,
                      file=self._file,
                      flush=True)
                
        except Exception as ex_:
            raise
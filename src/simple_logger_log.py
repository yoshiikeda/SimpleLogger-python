import datetime
import os

from simple_logger_common import ( DomainError,
                                   Singleton )


class Log(metaclass=Singleton):
    class Severity(metaclass=Singleton):
        CONSTANTS = { 'severity': { 'Trace': 0,
                                    'Debug': 1,
                                    'Info': 2,
                                    'Notice': 3,
                                    'Warning': 4,
                                    'Alert': 5,
                                    'Error': 6,
                                    'Critical': 7,
                                    'Fatal': 8,
                                    'Emergency': 9 } }
        
        def __contains__(self, severity_):
            result = None
            
            result = (severity_ in self.CONSTANTS['severity'])
            
            return result
        
        def __getattr__(self, severity_):
            result = None
            
            if not self.__contains__(self, severity_):
                raise DomainError()
            
            result = severity_
            
            return result
        
        
        def __getitem__(self, severity_):
            result = None
            
            if not self.__contains__(self, severity_):
                raise DomainError()
            
            result = self.CONSTANTS['severity'][severity_]
            
            return result


    CONSTANTS = { 'log': { 'format': '[{TIMESTAMP}][{SEVERITY}][{PROCESS}] {MESSAGE}' } }
    
    _logs = {}
    _loggers = []

    def __init__(self):
        self.Severity = self.Severity()
        
        
    def __getattr__(self, severity_):
        result = None
        
        if severity_ not in self.Severity:
            raise DomainError()
        
        if severity_ in self._logs:
            # Empty
            pass
        
        else:
            self._logs[severity_] = self.LogFactory(severity_)
            
        result = self._logs[severity_]
        
        return result
    
    
    def Add(self, logger_):
        self._loggers.append(logger_)
        
        
    def Close(self):
        for logger in self._loggers:
            logger.Close()
            
            
    def LogFactory(self, severity_):
        result = None
        
        def Log(message_):
            TIMESTAMP = datetime.datetime.now().srtftime('%Y-%m-%d %H:%M:%S.%f')
        
            for logger in self._loggers:
                logger.Write(severity_,
                             self.CONSTANTS['log']['format'].format(TIMESTAMP=TIMESTAMP,
                                                                    SEVERITY=severity_.upper(),
                                                                    PROCESS=str(os.getpid()),
                                                                    MESSAGE=message_))
                
        result = Log
        
        return result
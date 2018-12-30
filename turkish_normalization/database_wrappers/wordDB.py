import redis
import pickle
import functools


class WordDB:
    def __init__(self, host, db=0, port=6379, password=None):
        self._rds = redis.Redis(host, db=db, port=port, password=password)

    def __getitem__(self, name):
        return self._rds.get(name).decode("utf8")
        
    def __getattr__(self, name):
        if name == "words":
            return WordsObject(self._rds)
        elif name == "initials":
            return InitialsObject(self._rds)
        else:
            raise AttributeError("WordsDB doesn't have an attribute named %s" % name)
    
    def query(self, rds_method, *args, **kwargs):
        args = ", ".join('"%s"' % a for a in args)
        if kwargs:
            args = ", "
            args += ", ".join('%s="%s"' % (k, v) for k, v in kwargs.items())
        return eval(f"self._rds.{rds_method}({args})")
    
    def get_rds_instance(self):
        return self._rds
    

class WordsObject:
    def __init__(self, rds):
        self._rds = rds
    
    @functools.lru_cache(maxsize=5)
    def __getitem__(self, name):
        pos = self._rds.lrange("w:%s:p" % name, 0, -1)
        pos = [pickle.loads(p) for p in pos]
        return pos
    
    def __setitem__(self, name, value):
        self._rds.rpush("w:%s:p" % name, pickle.dumps(value))
        self._rds.incr("w:%s:c" % name)

    @functools.lru_cache(maxsize=256)
    def count(self, name):
        return int(self._rds.get("w:%s:c" % name))


class InitialsObject:
    def __init__(self, rds):
        self._rds = rds
        self._counts = {}
    
    @functools.lru_cache(maxsize=5)
    def __getitem__(self, name):
        words = self._rds.smembers("i:%s:w" % name)
        words = [w.decode("utf8") for w in words]
        self._counts[name] = len(words)
        return words
    
    def __setitem__(self, name, value):
        self._rds.sadd("i:%s:w" % name, value)
        self._rds.incr("total:count")
        if name in self._counts:
            self._counts[name] += 1

    def count(self, name):
        if name not in self._counts:
            self.__getitem__(name)
        return self._counts[name]




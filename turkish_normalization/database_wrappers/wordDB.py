import redis
import pickle
import functools


class WordDB:
    def __init__(self, host, db=0, port=6379, password=None, only_valids=False):
        self._rds = redis.Redis(host, db=db, port=port, password=password, decode_responses=True)
        self._words = WordsObject(self._rds)
        self._initials = InitialsObject(self._rds, only_valids)

    def __getitem__(self, name):
        return self._rds.get(name)
        
    def __getattr__(self, name):
        if name == "words":
            return self._words
        elif name == "initials":
            return self._initials
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
    def __init__(self, rds, only_valids):
        self._rds = rds
        self._query = "i:%s:v" if only_valids else "i:%s:w"

    @functools.lru_cache(maxsize=5)
    def __getitem__(self, name):
        words = self._rds.smembers(self._query % name)
        words = [w for w in words]
        return words
    
    def __setitem__(self, name, value):
        self._rds.sadd("i:%s:w" % name, value)
        self._rds.incr("total:count")

    def get(self, name, default):
        res = self.__getitem__(name)
        return res if res else default

    @functools.lru_cache(maxsize=2)
    def get_range(self, name, beg, end):
        res = self.__getitem__(name)
        return res[beg:end]

    def get_counts(self, name):
        res = self.__getitem__(name)
        counts = []
        pipe = self._rds.pipeline()
        for w in res:
            pipe.get("w:%s:c" % w)
            if len(pipe) == 20000:
                c = pipe.execute()
                counts.extend(c)
        counts.extend(pipe.execute())
        counts = {w:int(c) for w, c in zip(res, counts)}
        return counts

    def count(self, name):
        return self._rds.scard("i:%s:w" % name)




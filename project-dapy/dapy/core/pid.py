from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Pid:
    """
    Class to represent a process identifier (PID).
    """
    id: int
    
    def __str__(self):
        return f"p{self.id}"


@dataclass(frozen=True, order=True)
class Channel:
    """
    Class to represent a communication channel between two processes.
    """
    s: Pid
    r: Pid
    directed: bool = True
    
    def __str__(self):
        return f"<{self.s.id},{self.r.id}>"
    
    def __eq__(self, other):
        if not isinstance(other, Channel):
            return False
        if self.directed and other.directed:
            return self.s == other.s and self.r == other.r
        else:
            return self.normalized() == other.normalized()
        
    def __cmp__(self, other) -> int:
        if not isinstance(other, Channel):
            raise TypeError("Cannot compare Channel with non-Channel object")
        if self.directed and other.directed:
            a = (self.s, self.r)
            b = (other.s, other.r)
        else:
            a = self.normalized()
            b = other.normalized()
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
        
    def __hash__(self):
        if self.directed:
            return hash((self.s, self.r))
        else:
            return hash(self.normalized())
        
    def normalized(self) -> tuple[Pid, Pid]:
        """
        Return a normalized representation of the channel.
        """
        if self.s < self.r:
            return (self.s, self.r)
        else:
            return (self.r, self.s)
    
    
if __name__ == "__main__":
    p1 = Pid(1)
    p2 = Pid(2)
    p3 = Pid(3)
    p4 = Pid(4)
    
    c1 = Channel(p1, p2, directed=False)
    c2 = Channel(p2, p1)
    c3 = Channel(p1, p3)
    c4 = Channel(p3, p1)
    
    print(c1.__cmp__(c2))  # Should be equal
    print(c1.__cmp__(c3))  # c1 Should be smaller

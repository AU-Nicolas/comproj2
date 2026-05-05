from datetime import datetime

class TimeStamp:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    # Returns the current time as a timestamp
    @staticmethod
    def now():
        now = datetime.now()
        return TimeStamp(now.hour, now.minute, now.second)


    def __lt__(self, other):
        return (self.hour, self.minute, self.second) < (other.hour, other.minute, other.second)
    
    def __eq__(self, other):
        return (self.hour, self.minute, self.second) == (other.hour, other.minute, other.second)
    
    def __gt__(self, other):
        return (self.hour, self.minute, self.second) > (other.hour, other.minute, other.second)

    def __ge__(self, other):
        return (self.hour, self.minute, self.second) >= (other.hour, other.minute, other.second)
    
    def __le__(self, other):
        return (self.hour, self.minute, self.second) <= (other.hour, other.minute, other.second)

    def __sub__(self, other):
        hours = 0
        minutes = 0
        seconds = 0
        seconds += other.second - self.second
        if(seconds < 0):
            seconds += 60
            minutes -= 1
        minutes += other.minute - self.minute
        if(minutes < 0):
            minutes += 60
            hours -= 1
        hours += other.hour - self.hour
        if(hours < 0):
            hours += 24
        return TimeStamp(hours, minutes, seconds)
    
    def print(self):
        print(f"Hours: {self.hour}, Minutes: {self.minute}, Seconds: {self.second}")
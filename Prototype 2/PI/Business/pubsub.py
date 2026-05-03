class Publisher:
    def __init__(self):
        self.subscribers = []

    def Subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def Publish(self, message):
        for subscriber in self.subscribers:
            subscriber.receive(message)

class Subscriber:
    def Receive(self, message):
        print(f"received message: {message}")
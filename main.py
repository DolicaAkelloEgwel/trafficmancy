from ask_question import ask_question
from traffic_counter import TrafficCounter

query = input("What is your question? ")

models = ["dolphin-phi"]

traffic_counter = TrafficCounter()
counts = traffic_counter.test()

ask_question(models[0], query, counts)

print(counts)

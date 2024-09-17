from traffic_counter import get_traffic_count
from ask_question import ask_question

question = "What should I do with my life?"

traffic_count = get_traffic_count()
print(traffic_count)
print(ask_question(question, traffic_count))
import json
from difflib import get_close_matches


def load_knowledge_base(file_path):
  with open(file_path, 'r') as file:
    return json.load(file)


def save_to_knowledge_base(file_path, dataset):
  with open(file_path, 'w') as file:
    json.dump(dataset, file, indent=2)


def find_best_match(user_question, questions):
  ques = get_close_matches(user_question, questions, n=1, cutoff=0.6)
  return ques[0] if ques else None


def find_answer(question, knowledge_base):
  for q in knowledge_base['questions']:
    if q['question'] == question:
      return q['answer']


def chat_bot():
  knowledge_base = load_knowledge_base("chatbot/knowledge_base.json")

  while True:
    user_input = input("You : ")

    if user_input.lower() == "exit":
      break

    all_question = [q['question'] for q in knowledge_base['questions']]
    best_match_question = find_best_match(user_input, all_question)

    if best_match_question:
      answer = find_answer(best_match_question, knowledge_base)
      print("ChatBot :", answer)
    else:
      print("ChatBot : I don't know the answer. Can you teach me the answer?")
      your_ans = input(
          "Chatbot :Enter the answer or 'skip' to skip the question :")
      if (your_ans.lower() != "skip"):
        knowledge_base["questions"].append({
            "question": user_input,
            "answer": your_ans
        })
        save_to_knowledge_base("chatbot/knowledge_base.json", knowledge_base)
        print("ChatBot : Thankyou, I learnt a new response today")


if __name__ == '__main__':
  print("Welcome to mini chatbot, To exit the from code type 'exit'")
  chat_bot()

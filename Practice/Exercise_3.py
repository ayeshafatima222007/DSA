# KBC Quiz Game

questions = [
    {
        "question": "What is the capital of Pakistan?",
        "options": ["A) Lahore", "B) Karachi", "C) Islamabad", "D) Quetta"],
        "answer": "C"
    },
    {
        "question": "Which language is used for Python programming?",
        "options": ["A) HTML", "B) Python", "C) CSS", "D) SQL"],
        "answer": "B"
    },
    {
        "question": "How many continents are there in the world?",
        "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
        "answer": "C"
    },
    {
        "question": "Who is known as the father of computers?",
        "options": [
            "A) Charles Babbage",
            "B) Alan Turing",
            "C) Bill Gates",
            "D) Steve Jobs"
        ],
        "answer": "A"
    }
]

prize_money = [1000, 5000, 10000, 50000]

total_amount = 0

print("***** Welcome to KBC Quiz Game *****\n")

for i in range(len(questions)):

    print(f"Question {i+1}: {questions[i]['question']}")

    for option in questions[i]["options"]:
        print(option)

    user_answer = input("Enter your answer (A/B/C/D): ").upper()

    if user_answer == questions[i]["answer"]:
        total_amount = prize_money[i]
        print("Correct Answer!")
        print(f"You won Rs. {total_amount}\n")

    else:
        print("Wrong Answer!")
        break

print("Game Over!")
print(f"Your final amount is Rs. {total_amount}")
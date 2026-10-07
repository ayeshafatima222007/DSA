#----------Function Definitions----------

def gamePlaying(quiz, prize_money):
    totalAmount = 0
    score = 0

    for i in range(len(quiz)):
        print(f"\n--Question {i + 1}--")
        print(quiz[i]["question"])

        for option in quiz[i]["options"]:
            print(option)

        answer = input("Enter your answer: ").upper()

        if answer == quiz[i]["answer"]:
            score += 1
            totalAmount += prize_money[i]
            print("\n     *Correct!*")
            print("You earned Rs.", prize_money[i])
            print("You won Rs.", totalAmount)

        else:
            print("\n!!!Wrong Answer!!!")
            print("Correct Answer:", quiz[i]["answer"])

    print("\n\tYour final amount is Rs.", totalAmount)


def quitGame():
    print("Thank you for playing!")


#----------Main Function----------

def main():

    #---Local Data Types---
    quiz = [
        {
            "question": "What is the capital of Pakistan?",
            "options": ["A. Lahore", "B. Islamabad", "C. Karachi", "D. Peshawar"],
            "answer": "B"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["A. Earth", "B. Venus", "C. Mars", "D. Jupiter"],
            "answer": "C"
        },
        {
            "question": "How many days are there in a leap year?",
            "options": ["A. 365", "B. 364", "C. 366", "D. 367"],
            "answer": "C"
        },
        {
            "question": "Which animal is known as the King of the Jungle?",
            "options": ["A. Tiger", "B. Lion", "C. Elephant", "D. Leopard"],
            "answer": "B"
        },
        {
            "question": "Which programming language are you learning?",
            "options": ["A. Java", "B. Python", "C. C++", "D. JavaScript"],
            "answer": "B"
        },
        {
            "question": "How many continents are there on Earth?",
            "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
            "answer": "C"
        },
        {
            "question": "Which is the largest ocean?",
            "options": ["A. Atlantic", "B. Indian", "C. Pacific", "D. Arctic"],
            "answer": "C"
        },
        {
            "question": "Which fruit keeps the doctor away if eaten every day?",
            "options": ["A. Banana", "B. Apple", "C. Mango", "D. Orange"],
            "answer": "B"
        },
        {
            "question": "What is the national language of Pakistan?",
            "options": ["A. Punjabi", "B. English", "C. Urdu", "D. Sindhi"],
            "answer": "C"
        },
        {
            "question": "How many legs does a spider have?",
            "options": ["A. 6", "B. 8", "C. 10", "D. 12"],
            "answer": "B"
        }
    ]

    prize_money = [1000,1000,1000,2000,2000,3000,3000,3000,4000,4000]

    print("-----------------------------")
    print("-         Quiz Game         -")
    print("-----------------------------")

    playing = input("Do you want to play? (Yes/No): ")

    if playing.lower() == "yes":
        gamePlaying(quiz, prize_money)
    else:
        quitGame()


#----------Main----------
main()
print("--Quiz Completed--")
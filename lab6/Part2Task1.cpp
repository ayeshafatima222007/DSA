#include <iostream>
#include <string>
using namespace std;

// ---------------- Stack of characters (array based) ----------------
class Stack
{
    char* arr;
    int top;            // index of the top item (-1 means empty)
    int capacity;

public:
    Stack(int size)
    {
        capacity = size;
        arr = new char[capacity];
        top = -1;
    }

    ~Stack()
    {
        delete[] arr;
    }

    bool isEmpty() { return top == -1; }
    bool isFull()  { return top == capacity - 1; }

    bool push(char x)               // O(1)
    {
        if (isFull())
        {
            cout << "Stack Overflow" << endl;
            return false;
        }
        arr[++top] = x;
        return true;
    }

    bool pop()                      // O(1)
    {
        if (isEmpty())
        {
            cout << "Stack Underflow" << endl;
            return false;
        }
        top--;
        return true;
    }

    char peek()                     // returns the top item (stack must not be empty)
    {
        return arr[top];
    }
};

// Reverse the words of a sentence. Only characters are visited and only a
// stack is used (no tokenizing).
// Step 1: push every character, pop them all => whole sentence reversed.
// Step 2: in that reversed text every word is backwards, so for each word push
//         its letters and pop them at the space => each word is correct again.
string reverseWords(string s)
{
    Stack st((int)s.size() + 1);

    // step 1: reverse the whole sentence
    for (size_t i = 0; i < s.size(); i++)
        st.push(s[i]);

    string rev = "";
    while (!st.isEmpty())
    {
        rev += st.peek();
        st.pop();
    }

    // step 2: fix the letters inside each word
    string result = "";
    for (size_t i = 0; i <= rev.size(); i++)
    {
        if (i == rev.size() || rev[i] == ' ')       // word ended
        {
            while (!st.isEmpty())                   // pop letters => word in right order
            {
                result += st.peek();
                st.pop();
            }
            if (i != rev.size()) result += ' ';     // keep the space
        }
        else
        {
            st.push(rev[i]);                        // letter of the current word
        }
    }
    return result;
}

int main()
{
    string s;
    cout << "Enter sentence: ";
    getline(cin, s);
    cout << reverseWords(s) << endl;
    return 0;
}
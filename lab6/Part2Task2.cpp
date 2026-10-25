#include <iostream>
#include <string>
#include <sstream>
using namespace std;

// ---------------- Stack of integers (array based) ----------------
class Stack
{
    long long *arr;
    int top; // index of the top item (-1 means empty)
    int capacity;

public:
    Stack(int size)
    {
        capacity = size;
        arr = new long long[capacity];
        top = -1;
    }

    ~Stack()
    {
        delete[] arr;
    }

    bool isEmpty() { return top == -1; }
    bool isFull() { return top == capacity - 1; }
    int size() { return top + 1; }

    bool push(long long x) // O(1)
    {
        if (isFull())
        {
            cout << "Stack Overflow" << endl;
            return false;
        }
        arr[++top] = x;
        return true;
    }

    bool pop() // O(1)
    {
        if (isEmpty())
        {
            cout << "Stack Underflow" << endl;
            return false;
        }
        top--;
        return true;
    }

    long long peek() // returns the top item (stack must not be empty)
    {
        return arr[top];
    }

    string toString() // bottom ... top, e.g. [1, 2, 3]
    {
        ostringstream out;
        out << "[";
        for (int i = 0; i <= top; i++)
        {
            out << arr[i];
            if (i != top)
                out << ", ";
        }
        out << "]";
        return out.str();
    }
};

bool isInteger(const string &t) // 1, 64738, -42 are valid; "-" alone is not
{
    size_t i = 0;
    if (t[0] == '-' && t.size() > 1)
        i = 1;
    for (; i < t.size(); i++)
        if (t[i] < '0' || t[i] > '9')
            return false;
    return true;
}

bool isOperator(const string &t)
{
    return t.size() == 1 && (t[0] == '+' || t[0] == '-' || t[0] == '*' ||
                             t[0] == '/' || t[0] == '%');
}

int main()
{
    Stack st(100);
    string tok;

    cout << "Enter postfix tokens (? = show stack, ^ = pop and print, ! = exit)" << endl;

    while (cin >> tok)
    {
        if (isInteger(tok)) // operand: push it
        {
            try
            {
                st.push(stoll(tok));
            }
            catch (...)
            {
                cout << "Number too large: " << tok << endl;
            }
        }
        else if (isOperator(tok)) // operator: pop two, push result
        {
            if (st.size() < 2)
            {
                cout << "Error: operator " << tok << " needs two operands" << endl;
                continue;
            }
            long long b = st.peek();
            st.pop(); // right operand (top)
            long long a = st.peek();
            st.pop(); // left operand
            long long r = 0;
            bool ok = true;

            switch (tok[0])
            {
            case '+':
                r = a + b;
                break;
            case '-':
                r = a - b;
                break;
            case '*':
                r = a * b;
                break;
            case '/':
                if (b == 0)
                    ok = false;
                else
                    r = a / b;
                break;
            case '%':
                if (b == 0)
                    ok = false;
                else
                    r = a % b;
                break;
            }
            if (ok)
                st.push(r);
            else
            {
                cout << "Error: division by zero" << endl;
                st.push(a); // restore the operands
                st.push(b);
            }
        }
        else if (tok == "?") // print the whole stack
        {
            cout << st.toString() << endl;
        }
        else if (tok == "^") // pop and print the top
        {
            if (st.isEmpty())
                cout << "Error: stack is empty" << endl;
            else
            {
                cout << st.peek() << endl;
                st.pop();
            }
        }
        else if (tok == "!") // exit
        {
            break;
        }
        else
        {
            cout << "Invalid input: " << tok << endl;
        }
    }
    return 0;
}
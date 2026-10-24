#include <iostream>
using namespace std;

class Stack
{
    int* arr;       // array to hold the items
    int top;        // index of the top item (-1 means empty)
    int capacity;   // maximum number of items

public:
    Stack(int size)             // constructor
    {
        capacity = size;
        arr = new int[capacity];
        top = -1;               // stack starts empty
    }

    ~Stack()                    // destructor
    {
        delete[] arr;
    }

    bool isEmpty()
    {
        return top == -1;
    }

    bool isFull()
    {
        return top == capacity - 1;
    }

    bool push(int x)            // Time Complexity = O(1)
    {
        if (isFull())
        {
            cout << "Stack Overflow" << endl;
            return false;
        }
        top++;                  // move top up
        arr[top] = x;           // place the item
        return true;
    }

    bool pop()                  // Time Complexity = O(1)
    {
        if (isEmpty())
        {
            cout << "Stack Underflow" << endl;
            return false;
        }
        top--;                  // item is removed logically
        return true;
    }

    int peek()                  // Time Complexity = O(1)
    {
        if (isEmpty())
        {
            cout << "Stack is empty" << endl;
            return -1;          // -1 means "no value"
        }
        return arr[top];
    }
};

int main()
{
    Stack s(3);

    s.push(10);
    s.push(20);
    s.push(30);
    s.push(40);                         // Stack Overflow

    cout << s.peek() << endl;           // 30
    s.pop();
    cout << s.peek() << endl;           // 20
    s.pop();
    s.pop();
    s.pop();                            // Stack Underflow
    cout << s.isEmpty() << endl;        // 1
}
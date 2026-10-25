#include <iostream>
using namespace std;

// Circular queue using an array
class Queue
{
    int* arr;       // array to hold the items
    int front;      // index of the first item
    int rear;       // index of the last item
    int count;      // current number of items
    int capacity;   // maximum number of items

public:
    Queue(int size)             // constructor
    {
        capacity = size;
        arr = new int[capacity];
        front = 0;
        rear = capacity - 1;    // so the first enqueue lands on index 0
        count = 0;
    }

    ~Queue()                    // destructor
    {
        delete[] arr;
    }

    bool isEmpty()
    {
        return count == 0;
    }

    bool isFull()
    {
        return count == capacity;
    }

    bool enqueue(int x)         // Time Complexity = O(1)
    {
        if (isFull())
        {
            cout << "Queue Overflow" << endl;
            return false;
        }
        rear = (rear + 1) % capacity;   // wrap around at the end of the array
        arr[rear] = x;
        count++;
        return true;
    }

    bool dequeue()              // Time Complexity = O(1)
    {
        if (isEmpty())
        {
            cout << "Queue Underflow" << endl;
            return false;
        }
        front = (front + 1) % capacity; // wrap around at the end of the array
        count--;
        return true;
    }

    int peek()                  // returns the front item
    {
        if (isEmpty())
        {
            cout << "Queue is empty" << endl;
            return -1;          // -1 means "no value"
        }
        return arr[front];
    }
};

int main()
{
    Queue q(3);

    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);
    q.enqueue(40);                      // Queue Overflow

    cout << q.peek() << endl;           // 10
    q.dequeue();
    cout << q.peek() << endl;           // 20

    q.enqueue(40);                      // works: reuses the freed slot (wrap around)

    q.dequeue();                        // removes 20
    q.dequeue();                        // removes 30
    q.dequeue();                        // removes 40
    q.dequeue();                        // Queue Underflow
    cout << q.isEmpty() << endl;        // 1
}
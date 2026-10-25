#include <iostream>
using namespace std;

// ---------------- Node ----------------
class Node
{
public:
    int data;
    Node* next;

    Node(int val)
    {
        data = val;
        next = NULL;
    }
};

// ---------------- LinkList (only the functions the queue needs) ----------------
class LinkList
{
    Node* head;
public:
    LinkList()                  // constructor
    {
        head = NULL;
    }

    ~LinkList()                 // destructor
    {
        while (head != NULL)
        {
            Node* t = head;     // save current node
            head = head->next;  // move head forward
            delete t;           // free old node
        }
    }

    bool isEmpty()
    {
        return head == NULL;
    }

    Node* getHead()
    {
        return head;
    }

    Node* insertAtEnd(int x)    // O(n) because only head is stored
    {
        Node* newNode = new Node(x);

        if (head == NULL)       // empty list
        {
            head = newNode;
            return newNode;
        }

        Node* temp = head;
        while (temp->next != NULL)  // go to the last node
        {
            temp = temp->next;
        }
        temp->next = newNode;       // attach after the last node
        return newNode;
    }

    bool deleteFromStart()      // O(1)
    {
        if (head == NULL)
        {
            return false;
        }
        Node* temp = head;
        head = head->next;
        delete temp;
        return true;
    }
};

// ---------------- Queue using LinkList ----------------
class Queue
{
    LinkList list;          // head = front of queue, end = rear of queue
    int count;              // current number of items
    int capacity;           // maximum items allowed (to show Overflow)

public:
    Queue(int size)
    {
        count = 0;
        capacity = size;
    }                       // no destructor needed: ~LinkList() cleans up

    bool isEmpty()
    {
        return list.isEmpty();
    }

    bool isFull()
    {
        return count == capacity;
    }

    bool enqueue(int x)     // uses insertAtEnd
    {
        if (isFull())
        {
            cout << "Queue Overflow" << endl;
            return false;
        }
        list.insertAtEnd(x);
        count++;
        return true;
    }

    bool dequeue()          // uses deleteFromStart
    {
        if (isEmpty())
        {
            cout << "Queue Underflow" << endl;
            return false;
        }
        list.deleteFromStart();
        count--;
        return true;
    }

    int peek()              // uses getHead
    {
        if (isEmpty())
        {
            cout << "Queue is empty" << endl;
            return -1;      // -1 means "no value"
        }
        return list.getHead()->data;
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

    q.enqueue(40);                      // works: one slot is free now

    q.dequeue();                        // removes 20
    q.dequeue();                        // removes 30
    q.dequeue();                        // removes 40
    q.dequeue();                        // Queue Underflow
    cout << q.isEmpty() << endl;        // 1
}
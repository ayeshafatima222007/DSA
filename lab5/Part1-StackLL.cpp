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

// ---------------- LinkList (only the functions the stack needs) ----------------
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

    Node* insertAtHead(int x)   // O(1)
    {
        Node* newNode = new Node(x);
        newNode->next = head;   // link new node in front of old head
        head = newNode;         // new node becomes head
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

// ---------------- Stack using LinkList ----------------
class Stack
{
    LinkList list;          // head of this list = top of the stack
    int count;              // current number of items
    int capacity;           // maximum items allowed (to show Overflow)

public:
    Stack(int size)
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

    bool push(int x)        // uses insertAtHead
    {
        if (isFull())
        {
            cout << "Stack Overflow" << endl;
            return false;
        }
        list.insertAtHead(x);
        count++;
        return true;
    }

    bool pop()              // uses deleteFromStart
    {
        if (isEmpty())
        {
            cout << "Stack Underflow" << endl;
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
            cout << "Stack is empty" << endl;
            return -1;      // -1 means "no value"
        }
        return list.getHead()->data;
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
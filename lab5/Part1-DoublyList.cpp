#include <iostream>
using namespace std;

// ---------------- Node with Data, Next and Prev ----------------
class DNode
{
public:
    int data;
    DNode* next;    // pointer to the next node
    DNode* prev;    // pointer to the previous node

    DNode(int val)
    {
        data = val;
        next = NULL;
        prev = NULL;
    }
};

// ---------------- helper functions ----------------
void printNodes(DNode* p)       // prints a list given only its head
{
    while (p != NULL)
    {
        cout << p->data << " ";
        p = p->next;
    }
    cout << endl;
}

// adds value v at the end of a list described by head h and tail t
void addEnd(DNode*& h, DNode*& t, int v)
{
    DNode* n = new DNode(v);
    if (h == NULL)
    {
        h = t = n;          // first node of the new list
    }
    else
    {
        t->next = n;        // attach after the tail
        n->prev = t;        // and link back to the old tail
        t = n;
    }
}

bool existsIn(DNode* list, int v)   // true if v exists in the list
{
    while (list != NULL)
    {
        if (list->data == v) return true;
        list = list->next;
    }
    return false;
}

// ---------------- DoublyLinkList ----------------
class DoublyLinkList
{
    DNode* head;
    DNode* tail;            // tail makes end operations O(1)

    // removes node p from the list in O(1) (p must belong to this list)
    void unlink(DNode* p)
    {
        if (p->prev != NULL) p->prev->next = p->next;   // skip p going forward
        else head = p->next;                            // p was the head

        if (p->next != NULL) p->next->prev = p->prev;   // skip p going backward
        else tail = p->prev;                            // p was the tail

        delete p;
    }

public:
    DoublyLinkList()        // constructor
    {
        head = NULL;
        tail = NULL;
    }

    ~DoublyLinkList()       // destructor
    {
        while (head != NULL)
        {
            DNode* t = head;
            head = head->next;
            delete t;
        }
    }

    bool isEmpty()
    {
        return head == NULL;
    }

    DNode* getHead()
    {
        return head;
    }

    DNode* insertAtHead(int x)      // O(1)
    {
        DNode* n = new DNode(x);
        n->next = head;
        if (head != NULL) head->prev = n;   // old head points back to the new node
        else tail = n;                      // list was empty
        head = n;
        return n;
    }

    DNode* insertAtEnd(int x)       // O(1) (singly list: O(n))
    {
        DNode* n = new DNode(x);
        n->prev = tail;
        if (tail != NULL) tail->next = n;   // old tail points forward to the new node
        else head = n;                      // list was empty
        tail = n;
        return n;
    }

    DNode* insertNode(int index, int x)     // O(n)
    {
        if (index < 0) return NULL;
        if (index == 0) return insertAtHead(x);

        DNode* temp = head;
        for (int i = 0; i < index - 1; i++)     // go to node (index-1)
        {
            if (temp == NULL) return NULL;
            temp = temp->next;
        }
        if (temp == NULL) return NULL;          // index is out of range
        if (temp->next == NULL) return insertAtEnd(x);  // insert after the tail

        DNode* n = new DNode(x);
        n->next = temp->next;       // new -> after
        n->prev = temp;             // new <- before
        temp->next->prev = n;       // after <- new
        temp->next = n;             // before -> new
        return n;
    }

    bool findNode(int x)            // O(n)
    {
        for (DNode* t = head; t != NULL; t = t->next)
            if (t->data == x) return true;
        return false;
    }

    bool deleteNode(int x)          // delete all occurrences of x, O(n)
    {
        bool found = false;
        DNode* cur = head;
        while (cur != NULL)
        {
            DNode* nxt = cur->next;     // save next before cur may be deleted
            if (cur->data == x)
            {
                unlink(cur);            // O(1), no special head/middle cases
                found = true;
            }
            cur = nxt;
        }
        return found;
    }

    bool deleteFromStart()          // O(1)
    {
        if (head == NULL) return false;
        unlink(head);
        return true;
    }

    bool deleteFromEnd()            // O(1) (singly list: O(n))
    {
        if (tail == NULL) return false;
        unlink(tail);
        return true;
    }

    void displayList()              // forward, O(n)
    {
        for (DNode* t = head; t != NULL; t = t->next)
            cout << t->data << " ";
    }

    void displayReverse()           // backward using tail and prev, O(n)
    {
        for (DNode* t = tail; t != NULL; t = t->prev)
            cout << t->data << " ";
    }

    DNode* reverseList()            // returns a NEW reversed list, O(n)
    {
        DNode* newHead = NULL;
        for (DNode* c = head; c != NULL; c = c->next)
        {
            DNode* n = new DNode(c->data);  // copy the node
            n->next = newHead;              // put the copy in front
            if (newHead != NULL) newHead->prev = n;
            newHead = n;
        }
        return newHead;
    }

    DNode* sortList(DNode* list)    // O(n^2), swaps data
    {
        for (DNode* i = list; i != NULL; i = i->next)
            for (DNode* j = i->next; j != NULL; j = j->next)
                if (i->data > j->data)
                {
                    int t = i->data;
                    i->data = j->data;
                    j->data = t;
                }
        return list;
    }

    DNode* removeDuplicates(DNode* list)    // O(n^2)
    {
        for (DNode* i = list; i != NULL; i = i->next)
        {
            DNode* cur = i->next;
            while (cur != NULL)
            {
                DNode* nxt = cur->next;
                if (cur->data == i->data)       // duplicate of i
                {
                    cur->prev->next = cur->next;            // unlink using prev
                    if (cur->next != NULL) cur->next->prev = cur->prev;
                    delete cur;
                }
                cur = nxt;
            }
        }
        if (list == head)           // if this object's own list was used, fix tail
        {
            tail = head;
            while (tail != NULL && tail->next != NULL) tail = tail->next;
        }
        return list;
    }

    DNode* mergeLists(DNode* list1, DNode* list2)   // O(n + m), new list
    {
        DNode* h = NULL;
        DNode* t = NULL;
        for (DNode* c = list1; c != NULL; c = c->next) addEnd(h, t, c->data);
        for (DNode* c = list2; c != NULL; c = c->next) addEnd(h, t, c->data);
        return h;
    }

    DNode* interestLists(DNode* list1, DNode* list2)    // O(n * m), new list
    {
        DNode* h = NULL;
        DNode* t = NULL;
        for (DNode* c = list1; c != NULL; c = c->next)
            if (existsIn(list2, c->data) && !existsIn(h, c->data))
                addEnd(h, t, c->data);
        return h;
    }
};

int main()
{
    DoublyLinkList d;
    d.insertAtEnd(20);
    d.insertAtEnd(30);
    d.insertAtHead(10);
    d.insertNode(3, 40);
    cout << (d.insertNode(10, 99) == NULL) << endl;     // 1
    d.displayList(); cout << endl;                      // 10 20 30 40
    d.displayReverse(); cout << endl;                   // 40 30 20 10

    d.deleteFromStart();
    d.deleteFromEnd();
    d.displayList(); cout << endl;                      // 20 30

    d.insertAtEnd(20);
    d.insertAtEnd(40);
    cout << d.deleteNode(20) << endl;                   // 1
    d.displayList(); cout << endl;                      // 30 40
    d.displayReverse(); cout << endl;                   // 40 30
    cout << d.findNode(30) << d.findNode(99) << endl;   // 10

    printNodes(d.reverseList());                        // 40 30

    DoublyLinkList a, b, c;
    a.insertAtEnd(1); a.insertAtEnd(2); a.insertAtEnd(2); a.insertAtEnd(3);
    b.insertAtEnd(2); b.insertAtEnd(3); b.insertAtEnd(4);

    DNode* m = c.mergeLists(a.getHead(), b.getHead());
    printNodes(m);                                      // 1 2 2 3 2 3 4
    printNodes(c.sortList(m));                          // 1 2 2 2 3 3 4
    printNodes(c.removeDuplicates(m));                  // 1 2 3 4
    printNodes(c.interestLists(a.getHead(), b.getHead()));  // 2 3
}
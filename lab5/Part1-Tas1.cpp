#include <iostream>
using namespace std;


class Node{
public :        //it is a public class
    int data;
    Node* next;   //this is the next pointer which will store the address of next pointer


    Node(int val){     //this is node constructure
        data = val;    //data is initialized with a val
        next = NULL;    //next is initialized with a null value
    };

};

//helper function for reversing the list
void printNodes(Node* p)
{
    while (p != NULL)
    {
        cout << p->data << " ";
        p = p->next;
    }
    cout << endl;
}

// adds value v at the end of a list described by head h and tail t
void addEnd(Node*& h, Node*& t, int v)
{
    Node* n = new Node(v);
    if (h == NULL)
    {
        h = t = n;          // first node of the new list
    }
    else
    {
        t->next = n;        // attach after the current tail
        t = n;              // new node becomes the tail
    }
}

// Helper function to remove the Duplicates=returns true if value v exists in the given list
bool existsIn(Node* list, int v)
{
    while (list != NULL)
    {
        if (list->data == v) return true;
        list = list->next;
    }
    return false;
}

class LinkList
{
    Node* head;
public:
    //---1---
    LinkList()    // constructor
    {
        head = NULL; 
    }

    //---2---
    ~LinkList()  // destructor
    {           
        while (head != NULL) {
            Node* t = head;        //saves current node
            head = head->next;     //move head to next place
            delete t;              //delete prev node
        }
    }  

    //---3---
    bool isEmpty()
    {
        return head == NULL;
    }

    Node* getHead() 
    {
        return head;
    }

    //---4---
    Node* insertNode(int index, int x) {
        if (index < 0)
        {
            return NULL;
        }

        else if (index == 0)
        {
            return insertAtHead(x);   
        }

        else
        {
            Node* temp = head;

            for (int i = 0; i < index - 1; i++) 
            {
                if (temp == NULL)
                {
                    return NULL;
                }
                temp = temp->next;
            }
            if (temp == NULL) 
            {
                return NULL;
            }

            Node* newNode = new Node(x);
            newNode->next = temp->next;
            temp->next = newNode;
            return newNode;
        }
         
    }

    //---5---
    Node* insertAtHead(int x)
    {
        Node* newNode = new Node(x);
        newNode->next = head;    
        head = newNode;
        return newNode;
    }

    //---6---
    Node* insertAtEnd(int x)
    {
        Node* newNode = new Node(x);

        if (head == NULL)       //if list is empty
        {
            head = newNode;
            return newNode;
        }

        Node* temp = head;
        while (temp->next != NULL)     //treverse to last node
        {
            temp = temp->next;
        }
        temp->next = newNode;          //connect last node to the new one
        return newNode;
    }

    //---7---
    bool findNode(int key)         //Time Complexity=O(n)
    {
        Node* temp = head;
        int index = 0;
        while (temp!=NULL)
        {
            if (temp->data == key)
            {
                return true;
            }
            temp=temp->next;
        }
        return false;
    }

    //---8---
    bool deleteNode(int x)      // Time Complexity = O(n)
    {
        bool found = false;     //true if at least one node is deleted
 
        while (head != NULL && head->data == x)    //if x is at the head
        {
            Node* t = head;         //save the node to delete
            head = head->next;    
            delete t;              //free the old head
            found = true;
        }

         
        Node* cur = head;           //x is in the middle or at the end
        while (cur != NULL && cur->next != NULL)
        {
            if (cur->next->data == x)
            {
                Node* t = cur->next;    // node to delete
                cur->next = t->next;    // unlink it from the list
                delete t;               // free it
                found = true;
                
            }
            else
            {
                cur = cur->next;        // no match, move forward
            }
        }
        return found;           // false if x was never found
    }


    //---9---
    bool deleteFromStart()      //Time Complexity=O(1)
    {
        if (head==NULL)
        {
            return false;
        }
        else
        {
            Node* temp = head;
            head = head->next;
            temp->next = NULL;

            delete temp;
            return true;
        }
    }

    //---10---
    bool deleteFromEnd()        // Time Complexity = O(n)
    {
        if (head == NULL)          
        {
            return false;
        }

        if (head->next == NULL)    //if only one node exists
        {
            delete head;
            head = NULL;
            return true;
        }

        Node* temp = head;              //if more then 2 nodes exist
        while (temp->next->next != NULL)
        {
            temp = temp->next;          //treverse to 2nd last node
        }
        delete temp->next;              //del last node
        temp->next = NULL;       
        return true;
    }

    //---11---
    void displayList()      //Time Complexity=O(n)
    {
        Node* temp = head;
        while(temp!=NULL)
        {
            cout << temp->data<<" ";
            temp=temp->next;
        } 
    }

    //---12---
    Node* reverseList()         // Time Complexity = O(n)
    {
        Node* newHead = NULL;               // head of the new (reversed) list

        Node* cur = head;
        while (cur != NULL)
        {
            Node* n = new Node(cur->data);  // copy the current node
            n->next = newHead;              // link the copy in front of the new list
            newHead = n;                    // the copy becomes the new head
            cur = cur->next;                // move to the next original node
        }
        return newHead;                     // original list is unchanged
    }

    //---13---
    Node* sortList(Node* list)      // Time Complexity = O(n^2)
    {
        for (Node* i = list; i != NULL; i = i->next)
        {
            for (Node* j = i->next; j != NULL; j = j->next)
            {
                if (i->data > j->data)      // out of order
                {
                    int t = i->data;        // swap the data values
                    i->data = j->data;
                    j->data = t;
                }
            }
        }
        return list;                        // same head, now sorted
    }

    //---14---
    Node* removeDuplicates(Node* list)      // Time Complexity = O(n^2)
    {
        for (Node* i = list; i != NULL; i = i->next)
        {
            Node* prev = i;                     // node just before the one we check
            while (prev->next != NULL)
            {
                if (prev->next->data == i->data)    // duplicate of i
                {
                    Node* t = prev->next;
                    prev->next = t->next;           // unlink it
                    delete t;
                    // do NOT move prev: the next node may also be a duplicate
                }
                else
                {
                    prev = prev->next;              // no match, move forward
                }
            }
        }
        return list;                            // same head, duplicates removed
    }

    //---15---
    Node* mergeLists(Node* list1, Node* list2)
    {
        Node* h = NULL;         // head of the merged list
        Node* t = NULL;         // tail of the merged list

        for (Node* c = list1; c != NULL; c = c->next)
            addEnd(h, t, c->data);      // copy list1

        for (Node* c = list2; c != NULL; c = c->next)
            addEnd(h, t, c->data);      // copy list2

        return h;
    }

    //---16---
    Node* interestLists(Node* list1, Node* list2)
    {
        Node* h = NULL;
        Node* t = NULL;

        for (Node* c = list1; c != NULL; c = c->next)
        {
            if (existsIn(list2, c->data) && !existsIn(h, c->data))
                addEnd(h, t, c->data);  // common value, not added before
        }
        return h;
    }

};


int main()
{
    LinkList ll;
    ll.insertNode(0, 10);        // 10
    ll.insertNode(1, 30);        // 10 30
    ll.insertNode(1, 20);        // 10 20 30
    cout << (ll.insertNode(10, 99) == NULL)<<endl;    
    ll.displayList();                // 10 20 30

    ll.insertAtEnd(40);
    ll.insertAtEnd(50);
    ll.displayList();    // 10 20 30 40 50
    cout<<endl;

    cout << ll.findNode(20) << endl;   // 1
    cout << ll.findNode(99) << endl;   // 0

    cout << ll.deleteFromStart() << endl;   // 0
    ll.displayList();

    cout << ll.deleteFromEnd() << endl;
    ll.displayList();  

    Node* r = ll.reverseList();
    printNodes(r);          // 3 2 1
    ll.displayList();       // 1 2 3  

    LinkList a, b, c;

    a.insertAtEnd(1);
    a.insertAtEnd(2);
    a.insertAtEnd(2);
    a.insertAtEnd(3);
    b.insertAtEnd(2);
    b.insertAtEnd(3);
    b.insertAtEnd(4);
    
    Node* m = c.mergeLists(a.getHead(), b.getHead());
    printNodes(m);                          // 1 2 2 3 2 3 4

    Node* d = c.removeDuplicates(m);
    printNodes(d);                          // 1 2 3 4

    Node* x = c.interestLists(a.getHead(), b.getHead());
    printNodes(x);  
}
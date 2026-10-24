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

class List{       //this class connects  all nodes
    //these are not declared as public or protected so these are private by default
    Node* head;
    Node* tail;
    Node* middle;
public:
    List()
    {
        head=NULL;
        tail=NULL;
        middle=NULL;
    }                   //till here an empty linklist created

    void push_front(int val)       //Time Complexity=O(1)
    {
        Node* newNode = new Node(val);
        if (head==NULL)     //if the list is empty,means adding 1st element
        {
            head=tail=newNode;
            return;
        }
        else    //if already any element exist
        {
            newNode->next=head;         //(*newNode).next=head
            head=newNode;
        }
    }

    void push_back(int val)    //Time Complexity=O(1)
    {
        Node* newNode = new Node(val);
        if (tail==NULL)     //if the list is empty,means adding 1st element
        {
            head=tail=newNode;
            return;
        }
        else    //if already any element exist
        {
            tail->next=newNode;        
            tail=newNode;
        }
    }

    void pop_front()      //Time Complexity=O(1)
    {
        if (head==NULL)
        {
            cout<<"LL is empty";
            return;
        }
        else
        {
            Node* temp = head;
            head = head->next;
            temp->next = NULL;

            delete temp;
        }
    }

    void pop_back()         //Time Complexity=O(n)
    {
        if (head == NULL)
        {
            cout<<"LL is empty";
            return;
        }
        else
        {
            Node* temp=head;
            while(temp->next!=tail)
            {
                temp=temp->next;
            }
            temp->next=NULL;
            delete tail;
            tail=temp;

        }
    }

    void insert(int value,int pos)        //Time Complexity=O(n)
    {
        if(pos<0)
        {
            return;
        }
        else if(pos==0)
        {
            push_front(value);
        }
        else
        {
            Node* temp = head;
            for (int i=0 ; i<pos-1 ; i++)
            {
                temp=temp->next;
                if (temp==NULL)
                {
                    return;
                }
            }

            Node* newNode = new Node(value);
            newNode->next = temp->next;
            temp->next = newNode;
        }
    }

    int search(int key)         //Time Complexity=O(n)
    {
        Node* temp = head;
        int index = 0;
        while (temp!=NULL)
        {
            if (temp->data == key)
            {
                return index;
            }
            temp=temp->next;
            index++;
        }
        return -1;
    }

    void reverse()   //Time Complexity=O(n)        space complexit=O(1)
    {
        Node* prev = NULL;
        Node* curr = head;
        Node* next = NULL;

        while (curr != NULL) {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        head = prev;
    }

    void MiddleLL()
    {
        Node* slow = head;
        Node* fast = head;

        while(fast!=NULL && fast->next!=NULL)
        {
            slow = slow->next;
            fast = fast->next->next;
        }
        middle = slow;
    }

    void printMiddle()
    {
        MiddleLL();

        if (middle != NULL)
            cout << "Middle Node: " << middle->data << endl;
        else
            cout << "LL is empty" << endl;
    }


    void printLL()      //Time Complexity=O(n)
    {
        Node* temp = head;
        while(temp!=NULL)
        {
            cout << temp->data<<" ";
            temp=temp->next;
        } 
    }
};

int main()
{
    List ll;
    ll.push_front(1);
    ll.push_front(2);
    ll.push_front(3);

    ll.push_back(4);

    ll.pop_front();
    ll.pop_back();

    ll.push_front(4);
    ll.push_front(5);
    ll.push_front(6);

    ll.insert(3,2);
    ll.insert(3,0);    //this also works as push_front,like inserting in start
    ll.printLL();

    cout << ll.search(2)<<endl;

    ll.reverse();
    cout << "Reversed Linked List is: ";
    ll.printLL();

    ll.printMiddle();
}
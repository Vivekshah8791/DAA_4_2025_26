#include<iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    Node* prev;
    Node(int val){
        data=val;
        next=prev=NULL;
    }
};

class DoublyLinkedList {
private:
    Node* head;
public:
    DoublyLinkedList(){
        head=NULL;
    }
    
    void insert(int val) {
        Node* newNode = new Node(val);
        if (!head) {
            head = newNode;
            return;
        }
        Node* temp = head;
        while (temp->next) {
            temp = temp->next;
        }
        temp->next = newNode;
        newNode->prev = temp;
    }
    
    void deleteNode(int val) {
        if (!head) return;
        Node* temp = head;
        while (temp) {
            if (temp->data == val) {
                if (temp->prev) {
                    temp->prev->next = temp->next;
                } else {
                    head = temp->next;
                }
                if (temp->next) {
                    temp->next->prev = temp->prev;
                }
                delete temp;
                return;
            }
            temp = temp->next;
        }
    }
    
    void display() {
        Node* temp = head;
        while (temp!=NULL) {
            cout << temp->data << " <-> ";
            temp = temp->next;
        }
        cout << "NULL\n";
    }
};

int main(){
    DoublyLinkedList list;
    list.insert(10);
    list.insert(20);
    list.insert(30);
    list.insert(40);
    
    list.display();
    
    list.deleteNode(20);
    list.display();
    
    list.deleteNode(10);
    list.display();
    
    return 0;
}
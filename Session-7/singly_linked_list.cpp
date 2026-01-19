#include<iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    Node(int val) {
        data = val;
        next = NULL;
    }
};

class LinkedList {
private:
    Node* head;

public:
    LinkedList() {
        head = NULL;
    }

    void insertend(int value) {
        Node* newNode = new Node(value);
        if (head == NULL) {
            head = newNode;
            return;
        }
        Node* temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newNode;
    }

    void deleteEnd(int value) {
        if (head == NULL) return;

        if (head->data == value) {
            Node* temp = head;
            head = head->next;
            delete temp;
            return;
        }

        Node* curr = head;
        while (curr->next != NULL && curr->next->data != value) {
            curr = curr->next;
        }

        if (curr->next == NULL) return;

        Node* temp = curr->next;
        curr->next = temp->next;
        delete temp;
    }

    void display() {
        Node* temp = head;
        while (temp != NULL) {
            cout << temp->data << "->";
            temp = temp->next;
        }
        cout << "NULL\n";
    }
};

int main() {
    LinkedList l;
    l.insertend(12);
    l.insertend(1);
    l.insertend(2);

    l.deleteEnd(2);
    l.deleteEnd(1);
    l.deleteEnd(12);

    l.insertend(23);
    l.insertend(3);
    l.insertend(32);
    l.display();
}

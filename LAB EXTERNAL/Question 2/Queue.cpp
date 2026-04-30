#include<iostream>
using namespace std;
class Node{
    public:
    int data;
    Node* next;
    Node(int val){
        data=val;
        next=NULL;
    }
};
class Queue{
    private:
    Node* head;
    Node* tail;
    int count=0;
    public:
    Queue(){
        head=tail=NULL;
        count=0;
    }
    void Enqueue(int val){
        Node* newNode=new Node(val);
        if (tail==NULL){
            head=tail=newNode;
            count++;

        }
        tail->next=newNode;
        tail=newNode;
        count++;

    }
    void Dequeue(){
        if(head==NULL){
            cout<<"Underflow";
            return;
    }
    Node* temp=head;
    head=head->next;
    delete temp;
    count--;
    if (head==NULL){
        tail=NULL;
        count--;
    }
}
int size(){
    return count-1;
}
void diplay(){
    if(head==NULL){
        cout<<"empty";
        return;
    }
    Node* temp=head;
    while (temp!=NULL)
    {
        cout<<temp->data<<"->";
        temp=temp->next;
    }
    cout<<"NULL\n";
    
}
void lastelement(){
    if(tail==NULL){
        cout<<"Queue is empty";
        return;
    }
    cout<<"\nThe last element of the queue is "<<tail->data;
}

};
int main(){
    Queue q;
    q.Enqueue(10);
    q.Enqueue(20);
    q.Enqueue(30);
    q.Enqueue(40);
    q.Enqueue(50);
    q.diplay();
    cout<<q.size()<<endl;
    q.Dequeue();
    q.diplay();
    cout<<q.size();
    q.lastelement();
    
return 0;
}
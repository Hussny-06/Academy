#include<iostream>
#include"utils.h"
using namespace std;

int main() {
    cout<<"Hello World"<<endl;
    string user;
    cout<<"Enter a name :";
    cin>>user;
    greet(user);
    return 0;
}
#include<iostream>
#include<cstdlib> // for calling malloc and free
using namespace std;

static int global = 1;
int main(){

    // showing the memory regions
    int Stackvar = 2;
    int* heapvar = new int;
    *heapvar = 10;

    cout<<"Address of global "<<&global<<endl;
    cout<<"Address of Stackvar "<<&Stackvar<<endl;
    cout<<"Address of heapvar "<<heapvar<<endl;

    // showing the padding and alignment
    struct BadLayout{
        char a;     // 1 byte + 7 padding
        double b;    // 8 bytes
        char c;      // 1 byte + 7 padding
    };  // sizeof = 24 (but only 10 bytes of actual data!)
    struct GoodLayout{
        double b;     // 8 bytes
        char a;       // 1 byte
    char c;      // 1 byte + 6 padding
};  // sizeof = 16
    cout<<"Size of BadLayout : "<<sizeof(BadLayout)<<endl;
    cout<<"Size of GoodLayout : "<<sizeof(GoodLayout)<<endl;
    cout<<"Alignment Requirement of BadLayout : "<<alignof(BadLayout)<<endl;
    cout<<"Alignment Requirement of GoodLayout : "<<alignof(GoodLayout)<<endl;

    // heap allocation
    int* array = new int[100];
    cout<<"Address of array allocated on heap is : "<<array<<endl;
    delete[] array;

    int* carray = (int*) malloc(100*sizeof(int));
    cout<<"Address of array allocated on heap in c style is : "<<carray<<endl;
    free(carray);

}
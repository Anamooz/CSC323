#include <random>
#include<iostream>
#include <array>
/**
 * Name : Brian Kwong and Trycia Vong
 */


int main(int argc, char* argv[])
{
    using namespace std;

    if(argc < 2){
        cout << "Please provide a seed" << endl;
        return 1;
    }

    unsigned int seed = std::stoi(argv[1]);
    array<unsigned int,10> number;
    mt19937 gen(seed);
    for(int i = 0; i < 10; i++){
        number[i] = gen();
        cout << number[i] << endl;
    }
}
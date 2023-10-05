// Online C++ compiler to run C++ program online
#include <bits/stdc++.h>
using namespace std;

void search(char* pattern, char* text){
    int M = strlen(pattern);
    int N = strlen(text);
    
    for(int i = 0;i <= N-M; i++){
        int j;
    
        for(j = 0;j < M;j++)
            if(text[i + j] != pattern[j])
                break;
        
            if(j == M)
            cout << "Pattern is found in the index " << i << endl;
      }
}

int main() {
    char text[] = "SBIUEQBIQEVUNEVNU";
    char pattern[] = "QBIQ";
    search(pattern,text);
    return 0;
    
}

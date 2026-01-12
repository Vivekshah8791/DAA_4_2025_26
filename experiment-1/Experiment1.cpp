#include <bits/stdc++.h>
using namespace std::chrono;
using namespace std;


void complexRec(int n,int count) {
    auto start=high_resolution_clock::now();
    int depth=0;
   if (n <= 2) {
       return;
   }


   int p = n;
   while (p > 0) {
       vector<int> temp(n);
       for (int i = 0; i < n; i++) {
           temp[i] = i ^ p;
           count++;
       }
       p >>= 1;
       count++;
   }


   vector<int> small(n);
   for (int i = 0; i < n; i++) {
       small[i] = i * i;
       count++;
   }


   if (n % 3 == 0) {
       reverse(small.begin(), small.end());
   } else {
       reverse(small.begin(), small.end());
   }
   auto end=high_resolution_clock::now();
   auto duration=duration_cast<milliseconds>(end-start);
   cout<<"duration "<<duration.count()<<endl;
   depth++;
   complexRec(n / 2,count);
   complexRec(n / 2,count);
   complexRec(n / 2,count);
   cout<<"depth "<<n/depth<<endl; 
   cout<<"count "<<count;
}
// recurrence relation ---> T(n)=3T(n/2)+n+n+(n**2)/2
//Time complexity using master theorem ---> O(n**2)     Case P>=0
int main(){
    complexRec(8,0);

}

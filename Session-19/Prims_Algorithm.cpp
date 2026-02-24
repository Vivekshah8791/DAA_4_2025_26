#include<bits/stdc++.h>
using namespace std;

int main(){

    int V = 5;

    vector<vector<pair<int,int>>> adj(V);

    adj[0].push_back({1,2});
    adj[1].push_back({0,2});

    adj[0].push_back({3,6});
    adj[3].push_back({0,6});

    adj[1].push_back({2,3});
    adj[2].push_back({1,3});

    adj[1].push_back({4,5});
    adj[4].push_back({1,5});

    adj[2].push_back({4,7});
    adj[4].push_back({2,7});

    adj[3].push_back({4,9});
    adj[4].push_back({3,9});

    vector<bool> visited(V,false);

    priority_queue<
        pair<int,int>,
        vector<pair<int,int>>,
        greater<pair<int,int>>
    > pq;

    pq.push({0,0});

    int minCost = 0;

    while(!pq.empty()){

        int wt = pq.top().first;
        int u  = pq.top().second;
        pq.pop();

        if(visited[u]) continue;

        visited[u] = true;
        minCost += wt;

        for(auto it : adj[u]){
            int v = it.first;
            int w = it.second;

            if(!visited[v]){
                pq.push({w,v});
            }
        }
    }

    cout<<"Minimum Cost = "<<minCost;
}
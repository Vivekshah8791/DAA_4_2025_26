#include<bits/stdc++.h>
using namespace std;

class DSU{
public:
    vector<int> parent, rank1;

    DSU(int n){
        parent.resize(n);
        rank1.resize(n,0);
        for(int i=0;i<n;i++)
            parent[i]=i;
    }

    int findPar(int node){
        if(parent[node]==node)
            return node;
        return parent[node]=findPar(parent[node]);
    }

    void unionRank(int u,int v){
        u=findPar(u);
        v=findPar(v);

        if(u==v) return;

        if(rank1[u]<rank1[v])
            parent[u]=v;
        else if(rank1[u]>rank1[v])
            parent[v]=u;
        else{
            parent[v]=u;
            rank1[u]++;
        }
    }
};

int main(){

    int V=4;

    vector<vector<int>> edges={
        {0,1,10},{1,3,15},{2,3,4},{2,0,6},{0,3,5}
    };

    sort(edges.begin(),edges.end(),
        [](vector<int>&a,vector<int>&b){
            return a[2]<b[2];
        });

    DSU dsu(V);

    int cost=0;

    for(auto e:edges){
        int u=e[0];
        int v=e[1];
        int w=e[2];

        if(dsu.findPar(u)!=dsu.findPar(v)){
            cost+=w;
            dsu.unionRank(u,v);
        }
    }

    cout<<"MST Cost = "<<cost;
}
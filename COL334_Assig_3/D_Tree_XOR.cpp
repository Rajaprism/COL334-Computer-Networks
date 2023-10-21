#include<bits/stdc++.h>
using namespace std;

#define int long long

int n;
vector<vector<int>> G;
vector<int> ai;
vector<int> sz;
vector<int> cost;
vector<int> ans;

void calc(int node,int parent){
    sz[node]=1;
    for(int child : G[node]){
        if(child==parent)continue;
        calc(child,node);
        sz[node]+=sz[child];
        cost[node]+=(sz[child])*(ai[node]^ai[child])+cost[child];
    }
}
void calcans(int node,int parent){

    int val=cost[node];
    int sc=sz[node];

    ans[node]=cost[node]+(n-sz[node])*(ai[node]^ai[parent])+(ans[parent]-(sz[node]*(ai[node]^ai[parent])+cost[node]));

    for(int child : G[node]){
        if(child==parent)continue;
        calcans(child,node);
    }

    sz[node]=sc;
    cost[node]=val;
}

void solve( )
{
    cin>>n;
    ai.assign(n+1,0);
    G.assign(n+1,vector<int>());
    cost.assign(n+1,0);
    sz.assign(n+1,0);
    ans.assign(n+1,0);

    for(int i=1;i<=n;i++)cin>>ai[i];

    for(int i=1;i<n;i++){
        int a,b;cin>>a>>b;
        G[a].push_back(b);
        G[b].push_back(a);
    }

    calc(1,0);
    ai[0]=ai[1];
    ans[0]=cost[1];
    calcans(1LL,0LL);

    for(int  i=1;i<=n;i++)cout<<ans[i]<<" ";
    cout<<endl;

}
 
 
int32_t main()
{
    ios::sync_with_stdio(0); cin.tie(0);
    int t=1;    
    cin>>t;
    while(t-->0)
    {
        solve();
    }
}

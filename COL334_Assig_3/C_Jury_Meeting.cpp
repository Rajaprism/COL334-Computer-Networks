#ifndef ONLINE_JUDGE
// #include "debugger.hpp"
#else
#define debug(...) 
#endif
#include<bits/stdc++.h>
using namespace std;


// ===================================#define==============================================
#define dbg(v)                                                                 \
    cout << "Line(" << __LINE__ << ") -> " << #v << " = " << (v) << endl;
#define int long long
#define cyes cout<<"YES\n"
#define cno cout<<"NO\n"
#define ed "\n"

 
const int inf=(int)1e17+5;
const int mod=(int)998244353;
const int N=2*(1e5+5);

vector<int> m;
// ===================functions========================
void pstr(string s){cout<<s<<endl;}
void pint(int n){cout<<n<<endl;}

int compute(int n,int x){
    int u=1;
    for(int i=1;i<=n;i++){
        if(i==x+1)continue;
        u=(u*i)%mod;
    }
    return u;
}

void solve( )
{
    int n;cin>>n;
    vector<int> v(n);
    map<int,int> u;
    int mx1=-1,mx2=-1;
    for(int i=0;i<n;i++){
        cin>>v[i];
        u[v[i]]++;
    }
    sort(v.begin(),v.end());
    mx1=v[n-1],mx2=v[n-2];
    if(mx1-mx2>1){
        cout<<0<<endl;
    }else{
        
        if(mx1==mx2)cout<<compute(n,0LL)<<endl;
        else cout<<(u[mx2]*compute(n,u[mx2]))%mod<<endl;
    }
}
 
 
int32_t main()
{
    #ifndef ONLINE_JUDGE
    freopen("Error.txt", "w", stderr);
    #endif
    ios::sync_with_stdio(0); cin.tie(0);
    int t=1;    
    cin>>t;
    while(t-->0)
    {
        solve();
    }
}

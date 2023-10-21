#ifndef ONLINE_JUDGE
//#include "debugger.hpp"
#else
#define debug(...) 42
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
const int mod=(int)1e9+7;
const int N=2*(1e5+5);

// ===================functions========================
void pstr(string s){cout<<s<<endl;}
void pint(int n){cout<<n<<endl;}



void solve( )
{
    int l,r;
    cin>>l>>r;
    int powi=ceil(log10(r));
    int i=0;
    int ans=0;
    while(i<powi+1)
    {
        int y=pow(10LL,i);
        int a=l/y;
        int b=r/y;
        i++;
        ans+=b-a;
    }
    cout<<ans<<endl;
}
 
 
int32_t main()
{
    #ifndef ONLINE_JUDGE
    freopen("Error.txt", "w", stderr);
    #endif
    ios::sync_with_stdio(0); cin.tie(0);
    int t=1;    cin>>t;
    while(t-->0)
    {
        solve();
    }
}

#ifndef ONLINE_JUDGE
// #include "debugger.hpp"
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
    string s;
    cin>>s;
    int n=s.size();
    int ans=n;
    for(char i='0';i<='9';i++){
        for(char j='0';j<='9';j++){
            bool t=true;
            int e=0,o=0;
            for(int k=0;k<n;k++){
                if(t && s[k]==i){
                    o++;
                    t=false;
                }else if(!t && s[k]==j){
                    e++;
                    t=true;
                }
            }
            if(i==j)ans=min(ans,n-(o+e));
            else{
                if((o+e)%2)ans=min(ans,n-(o+e)+1);
                else ans=min(ans,n-(o+e));
            }
        }
    }
    cout<<ans<<endl;
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

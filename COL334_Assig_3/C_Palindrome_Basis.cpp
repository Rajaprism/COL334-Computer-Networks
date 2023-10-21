#include<iostream>
#include<cmath>
#include<algorithm>
#include<vector>
#include<string>
#include<set>
#include<numeric>
#include<bitset>
#include<map>
#include<utility>
#include<cstdlib>
#include<deque>
#include<stack>
#include<queue>
#include<unordered_map>
#include<unordered_set>
#include<string.h>
#include<iomanip>
#include<time.h>
 
using namespace std;
 
const long long MOD = 1000000007;
#define FASTINOUT cin.tie(0); ios::sync_with_stdio(false); cout.tie(0);
#define int long long int // Change this if there is a memory issue;
#define ll long long 
#define pint pair<int,int>
#define vint vector<int>
#define sint set<int>
#define endl "\n"
#define Max_heap priority_queue<int> 
#define Min_heap priority_queue<int,vector<int>,greater<int>> 

signed main ()
{   std::ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    int t;
    cin>>t;
    vint palin;
    int N=4e4+1;
    for(int i=1;i<=4e4+1;i++)
    {
        string s = to_string(i);
        string x=s;
        reverse(x.begin(),x.end());
        if(x==s)
        {
            palin.push_back(i);
        }
    }
    int dp[N+1][(int)palin.size()+1];
    memset(dp,(int)0,sizeof dp);
    for(int i=0;i<=palin.size();i++)
    {
        dp[0][i]=1;
    }
    for(int i=1;i<=N;i++)
    {
        for(int j=1;j<=palin.size();j++)
        {
            if(i-palin[j-1]>=0)
            {
                dp[i][j]=(dp[i-palin[j-1]][j]+dp[i][j-1])%MOD;
            }
            else
            {
                dp[i][j]=dp[i][j-1];
            }
        }
    }
    while(t--)
    {   
        int n;
        cin>>n;
        int sum=0;
        cout<<dp[n][palin.size()]<<endl;
    }
}

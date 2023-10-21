#include<bits/stdc++.h>
using namespace std;

#define int long long

const int mod=(int)998244353;

int findval(vector<vector<int>> &dp,int i,int l,int r,int t){
    if(t)return (dp[i][r]-dp[i][l-1]+mod)%mod;;
    return ((r*(r+1)/2-dp[i][r])-(l*(l-1)/2-dp[i][l-1])+mod)%mod;
}

void solve( )
{
    int n;cin>>n;
    vector<int> v(n+1);

    for(int i=1;i<=n;i++)cin>>v[i];

    vector<vector<int>> dp(32,vector<int>(n+1,0LL));
    vector<vector<int>> xorval(32,vector<int>(n+1,0LL));
    vector<vector<int>> count(32,vector<int>(n+1,0LL));

    for(int i=0;i<32;i++){
        int u=(1<<i);

        for(int j=1;j<=n;j++){

            if(u&v[j])xorval[i][j]=xorval[i][j-1]^(1LL);
            else xorval[i][j]=xorval[i][j-1];

            count[i][j]=count[i][j-1]+xorval[i][j];

            if(xorval[i][j])dp[i][j]=j;
            dp[i][j]=(dp[i][j]+dp[i][j-1])%mod;
        }
    }

    int ans=0;
    for(int i=0;i<32;i++){

        int u=(1<<i);

        for(int j=1;j<=n;j++){
            
            int val=findval(dp,i,j,n,(xorval[i][j-1])^1);

            int ual=count[i][n]-count[i][j-1];
            if(!((xorval[i][j-1])^1))ual=(n-j+1)-ual;
            ual=ual*(j-1);

            ans=(ans+(u*((val-ual+mod)%mod))%mod)%mod;
        }

    }
    cout<<ans<<endl;
}
 
 
int32_t main()
{
    solve();
}

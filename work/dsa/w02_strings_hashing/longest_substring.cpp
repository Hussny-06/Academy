using namespace std;
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int l = 0, r = 0, MaxLen = 0;
        bool in_window[256] = {0};
        while(r<s.size()){
            if( in_window[ s[r] ] == false ){
                in_window[ s[r] ] = true;
                MaxLen = max( MaxLen, r-l+1);
                r++;
            }else{
                in_window[ s[l] ] = false;
                l++;
            }
        }
        return MaxLen;
    }
};
using namespace std;
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        int freqS[26] = {0}, freqP[26] = {0};
        vector<int> result;
        
        if( s.size() < p.size())
            return {};
        
        for(int i=0; i<p.size(); i++){
            freqP[p[i]-'a']++;
            freqS[s[i]-'a']++;
        }
        if( equal( begin(freqS), end(freqS), begin(freqP), end(freqP)) )
            result.push_back(0);

        int l = 0, r = p.size();

        while( r<s.size()){
            freqS[s[l]-'a']--;
            freqS[s[r]-'a']++;
            if( equal( begin(freqS), end(freqS), begin(freqP), end(freqP)) )
                result.push_back(l+1);
            l++;
            r++;
        }
        
        
        return result;
    }
};
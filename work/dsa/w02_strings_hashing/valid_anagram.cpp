using namespace std;
class Solution {
public:
    bool isAnagram(string s, string t) {
        int freq[26] = {0};

        if(s.size() == t.size()){

            for(int i=0; i<s.size(); i++){
                freq[s[i]-97]++;
                freq[t[i]-97]--;
            }
            
            bool allzero = all_of(begin(freq), end(freq), [] (int i){
                return i == 0;
            });

            if(allzero)
                return true;
        }
        
        return false;
    }
};
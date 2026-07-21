using namespace std;
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        
        unordered_map <string, vector<string>> mp;
        for( int i = 0; i < strs.size(); i++){

            int freq[26] = {0};
            
            for( int j =0; j< strs[i].size(); j++){
                freq[strs[i][j]-'a']++; 
            }
            
            string key;
            
            for (const auto& elem : freq) {
                key += to_string(elem) + "#";
            }
            
            mp[key].push_back(strs[i]);
        }
        vector<vector<string>> answer;

        for( const auto& elem : mp){
            answer.push_back(elem.second);
        }
        return answer;
    }
};
class Solution {
public:
    string minWindow(string s, string t) {
        int r = 0 , l = 0, required = 0, formed = 0;
        size_t Minlen = INT_MAX, StartIdx = INT_MAX;
        int freqT[58] = {0}, freqS[58] = {0};

        if(s.size() < t.size()){
            return "";

        }else{

            for( int i=0; i<t.size(); i++){
                freqT[ t[i] - 'A']++;
                if( freqT[ t[i] - 'A'] == 1 )
                    required++;
            }

            while( r<s.size() ){
                freqS[ s[r] - 'A']++;
                if( freqS[ s[r] - 'A'] == freqT[ s[r] - 'A']){
                    formed++;
                }
                while(formed == required){
                    if( r-l+1 < Minlen){
                        Minlen = r-l+1;
                        StartIdx = l;
                    }
                    if( freqS[ s[l] - 'A'] == freqT[ s[l] - 'A']){
                        formed--;
                        freqS[ s[l] - 'A']--;
                        l++;
                    }else{
                        freqS[ s[l] - 'A']--;
                        l++;
                    }
                }
                r++;   
            }
        }
        return (StartIdx == INT_MAX) ? "":s.substr( StartIdx, Minlen);
    }
};
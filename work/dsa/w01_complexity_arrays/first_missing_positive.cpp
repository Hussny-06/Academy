class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size(), temp;
        bool contains1 = false;

        for(int i=0; i<n; i++){

            if(nums[i] == 1){
                contains1 = true;
            }else if( nums[i] <= 0 || nums[i] > n){
                nums[i] = 1;
            }

        }

        if(contains1 == false){

            return 1;

        }else{

            for(int i=0; i<n; i++){
                temp = abs(nums[i]);

                if(nums[temp-1] < 0)
                    continue;
                else
                    nums[temp-1] *= -1;
            }

        }
        for(int i=1; i<n; i++){

            if( nums[i]>0 )
                return i+1;

        }
        return n+1;
        
    }
};
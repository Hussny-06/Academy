#include <gtest/gtest.h>
#include "utils.h"

// Test that greet doesn't crash (basic smoke test)
TEST(UtilsTest, GreetDoesNotCrash) {
    EXPECT_NO_THROW(greet("TestUser"));
}

TEST(UtilsTest, GreetWithEmptyString) {
    EXPECT_NO_THROW(greet(""));
}
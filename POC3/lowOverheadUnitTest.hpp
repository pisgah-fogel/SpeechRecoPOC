#pragma once

#ifdef UNIT

#include <iostream>
#include <vector>

class UnitTest
{
    public:
        UnitTest(const char* testname, int (*testfunction)(void), size_t line, const char* filename) {
            rTests += 1;

            std::cout<<"Testcase "<<testname<<"... "<<std::endl;
            int result = (*testfunction)();
            if (result == 0) {
                rPassed ++;
                std::cout<<"Passed"<<std::endl;
            }
            else if (result == 1)
            {
                rFailed ++;
                std::cout<<"Failed ( "<<filename<<":"<<line<<" )"<<std::endl;
            }
            else
            {
                rMissing ++;
                std::cout<<"Missing"<<std::endl;
            }
            
        }
        static size_t getPassedTest() {
            return rPassed;
        }
        static size_t getFailedTest() {
            return rFailed;
        }
        static size_t getMissingTest() {
            return rMissing;
        }
    private:
        inline static unsigned int rTests = 0;
        inline static unsigned int rPassed = 0;
        inline static unsigned int rFailed = 0;
        inline static unsigned int rMissing = 0;
};

#define START_TEST(X) static UnitTest _test_ ## X = UnitTest( #X , &X , __LINE__, __FILE__);

class _Singleton
{
    public:
        ~_Singleton () {
            std::cout<<std::endl<<"Unit test results:"<<std::endl;
            std::cout<<"Passed: "<<UnitTest::getPassedTest()<<std::endl;
            std::cout<<"Missing: "<<UnitTest::getMissingTest()<<std::endl;
            std::cout<<"Failed: "<<UnitTest::getFailedTest()<<std::endl<<std::endl;
        }
};

static _Singleton _donotfreeme;

#else

#define START_TEST(X)

#endif
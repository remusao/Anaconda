#include <iostream>
#include "coroutine.h"
#include "yield.h"
#include "generator.h"

template <typename T0, typename T1, typename T2>
auto fun(T0 a, T1 b, T2 c) -> decltype(a + b + c + a + b)
{
    auto var1 = a + b;
    auto var2 = a + b + c;
    auto var3 = a + b + c + a + b;
    return var3;
}

template <typename T0, typename T1, typename T2>
auto myRang(T0 a, T1 b, T2 c) -> __Generator<decltype(a)>
{
    struct myRangFunctor
    {
        T0 a;
        T1 b;
        T2 c;
        coroutine __coroutine;

        myRangFunctor() = delete;
        myRangFunctor(const myRangFunctor&) = delete;
        myRangFunctor& operator=(const myRangFunctor&) = delete;

        myRangFunctor(myRangFunctor&&) = default;
        myRangFunctor& operator=(myRangFunctor&&) = default;
        myRangFunctor(const T0 a, const T0 b, const T1 c)
        {
            this->a = a;
            this->b = b;
            this->c = c;
        }

        decltype(a) operator()()
        {
            reenter(this->__coroutine)
            {
                yield return this->a;
                yield return this->b;
                yield return this->c;
            }
            throw __EndOfGenerator();
        }
    };
    return __Generator<decltype(a)>(myRangFunctor(a, b, c));
}


auto main() -> int
{
	__Generator<int> r = myRang(42, 69, 12);
	auto it =  r.begin(), end = r.end();
    for (; it != end; ++it)
    {
		std::cout << *it << std::endl;
    }
}

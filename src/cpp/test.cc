#include <vector>
#include "generator.h"
#include "yield.h"
#include "coroutine.h"



auto myrange() -> Generator<void>
{
    coroutine c;
    return Generator<long int>([=]() mutable -> long int
    {
        reenter(c)
        {
            yield return 42;
            yield return 1138;
			std::vector<long int> vec = {1, 2, 3, 4};
            for (auto it = vec.begin(); it != vec.end(); ++it)
            {
                yield return *it;
            }
        }
        throw EndOfGenerator();
    });
}

int main()
{
    for (auto x : myrange())
    {
        print(x);
    }

}

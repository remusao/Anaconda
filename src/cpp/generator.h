#ifndef GENERATOR_H
# define GENERATOR_H

#include <iostream>
# include <functional>


class EndOfGenerator
{
	public:
		EndOfGenerator() {}
};

template <typename Value>
class GeneratorIterator
{
	public:
	GeneratorIterator()
		: end_(true)
	{
	}

	// Move
	GeneratorIterator(GeneratorIterator&&) = default;
	GeneratorIterator& operator=(GeneratorIterator&&) = default;

	// Copy
	GeneratorIterator(const GeneratorIterator&) = delete;
	GeneratorIterator& operator=(const GeneratorIterator&) = delete;

	GeneratorIterator(const std::function<Value ()>& gen)
		: end_(false),
		  gen_(gen)
	{
		++(*this);
	}
	
	bool operator==(const GeneratorIterator& it) const
	{
		return end_ == it.end_;
	}

	bool operator!=(const GeneratorIterator& it) const
	{
		return end_ != it.end_;
	}

	GeneratorIterator<Value>& operator++()
	{
		try
		{
			val_ = gen_();
		}
		catch (...)
		{
			end_ = true;
		}

		return *this;
	}

	const Value& operator*() const
	{
		return val_;
	}

	private:
		bool end_;
		std::function<Value ()> gen_;
		Value val_;
};


template <typename Value>
class Generator
{
	public:
		// Must be initialized with an iterator
		Generator() = delete;
		~Generator() = default;
		Generator(Generator&&) = default;
		Generator& operator=(Generator&&) = default;

		Generator(const std::function<Value ()>& gen) : gen_(gen) {}

		// Copy is forbiden
		Generator(const Generator&) = delete;
		Generator& operator=(const Generator&) = delete;


		auto begin() const -> GeneratorIterator<Value> 
		{
			return GeneratorIterator<Value>(gen_);
		}

		auto end() const -> GeneratorIterator<Value> 
		{
			return GeneratorIterator<Value>();
		}

	private:
		std::function<Value ()> gen_;
};

#endif /* ndef GENERATOR_H */


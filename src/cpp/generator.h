#ifndef GENERATOR_H
# define GENERATOR_H

#include <iostream>
# include <functional>


template <typename Value>
class GeneratorIterator
{
	public:
	GeneratorIterator() : end_(true) {}
	GeneratorIterator(GeneratorIterator&&) = default;
	GeneratorIterator& operator=(GeneratorIterator&&) = default;

	GeneratorIterator(const std::function<Value (bool&)>& gen)
		: end_(false),
		  gen_(gen),
		  val_(gen_(end_))
	{
		std::cout << val_ << std::endl;
		std::cout << end_ << std::endl;
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
		val_ = gen_(end_);
		return *this;
	}

	const Value& operator*() const
	{
		return val_;
	}

	private:
		bool end_;
		std::function<Value (bool&)> gen_;
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

		Generator(const std::function<Value (bool&)>& gen) : gen_(gen) {}

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
		std::function<Value (bool&)> gen_;
};

#endif /* ndef GENERATOR_H */


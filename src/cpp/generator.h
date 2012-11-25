#pragma once
#ifndef GENERATOR_H
# define GENERATOR_H

# include <functional>

class __EndOfGenerator
{
	public:
		__EndOfGenerator() {}
};


template <typename ValueType>
class __GeneratorIterator
{
	public:
	__GeneratorIterator()
		: end_(true),
		  gen_(*((std::function<ValueType ()>*)(0)))
	{
	}

	// Move
	__GeneratorIterator(__GeneratorIterator&&) = default;
	__GeneratorIterator& operator=(__GeneratorIterator&&) = default;

	// Copy
	__GeneratorIterator(const __GeneratorIterator&) = delete;
	__GeneratorIterator& operator=(const __GeneratorIterator&) = delete;

	// Normal constructor
	__GeneratorIterator(const std::function<ValueType ()>& gen)
		: end_(false),
		  gen_(gen)
	{
		// init the first value
		++(*this);
	}
	
	bool operator==(const __GeneratorIterator& it) const
	{
		return end_ == it.end_;
	}

	bool operator!=(const __GeneratorIterator& it) const
	{
		return end_ != it.end_;
	}

	__GeneratorIterator<ValueType>& operator++()
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

	const ValueType& operator*() const
	{
		return val_;
	}

	private:
		bool end_;
		const std::function<ValueType ()>& gen_;
		ValueType val_;
};


template <typename ValueType>
class __Generator
{
	public:
		typedef ValueType type;
		// Must be initialized with an iterator
		~__Generator() = default;
		__Generator(__Generator&&) = default;
		__Generator& operator=(__Generator&&) = default;

		__Generator(std::function<ValueType ()>&& gen)
			: gen_(std::move(gen))
		{
		}

		// Copy is forbiden
		__Generator() = delete;
		__Generator(const __Generator&) = delete;
		__Generator& operator=(const __Generator&) = delete;

		__GeneratorIterator<ValueType> 
		begin() const
		{
			return __GeneratorIterator<ValueType>(gen_);
		}

		__GeneratorIterator<ValueType> 
		end() const
		{
			return __GeneratorIterator<ValueType>();
		}

	private:
		std::function<ValueType ()> gen_;
};

#endif /* ndef GENERATOR_H */


/**
 * @file   metal/decomposer.hpp
 * @date   22.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#ifndef METAL_TEST_DECOMPOSER_HPP
#define METAL_TEST_DECOMPOSER_HPP

#include <metal/unit.h>
#include <type_traits>

namespace metal
{

namespace unit
{

template<typename T, bool Relative = false>
struct epsilon
{
    T value;

    constexpr epsilon<T, true>     operator~() const {return { value};}
    constexpr epsilon<T, Relative> operator-() const {return {-value};};

};

constexpr epsilon<unsigned long long int> operator""_eps( unsigned long long int value) {return {value};}
constexpr epsilon<long double>            operator""_eps( long double value) {return {value};}

enum class expression_type
{
    equal, not_equal, ge, le, greater, lesser, plain, close, close_relative
};

template<typename T, typename U, bool Relative>
struct epsilon_expression
{
    T value;
    U tolerance;
};

template<typename T, typename U, bool Relative>
constexpr epsilon_expression<const T &, U, Relative> operator+(const T & value, const epsilon<U, Relative> & eps) {return {value, eps.value};}


template<typename T, typename U, typename V, bool Relative>
struct ternary_expression
{
    T lhs;
    U rhs;
    V tolerance;

    constexpr static expression_type type = Relative ? expression_type::close_relative : expression_type::close;

    constexpr bool eval() const {
        return _eval_impl(std::integral_constant<bool, Relative>{});
    }
    constexpr operator bool() const {return eval();}
    constexpr std::remove_reference_t<V> abs_tolerance() const {return tolerance < 0 ? -tolerance : tolerance;}
private:
    constexpr bool _eval_impl(std::true_type)   const {return ((lhs <= (rhs * (static_cast<V>(1) + abs_tolerance()))) && (lhs >= (rhs * (static_cast<V>(1) - abs_tolerance()))));}
    constexpr bool _eval_impl(std::false_type)  const {return ((lhs <= (rhs + tolerance)) && (lhs >= (rhs - tolerance)));}
};

template<typename T, typename U, expression_type Type>
struct binary_expression
{
    T lhs;
    U rhs;
    constexpr static expression_type type = Type;

    constexpr bool eval() const {
        return _eval_impl(std::integral_constant<expression_type, Type>{});
    }
    constexpr operator bool() const {return eval();}
private:
    constexpr bool _eval_impl(std::integral_constant<expression_type, expression_type::equal>)      const {return lhs == rhs;}
    constexpr bool _eval_impl(std::integral_constant<expression_type, expression_type::not_equal>)  const {return lhs != rhs;}
    constexpr bool _eval_impl(std::integral_constant<expression_type, expression_type::ge>)         const {return lhs >= rhs;}
    constexpr bool _eval_impl(std::integral_constant<expression_type, expression_type::le>)         const {return lhs <= rhs;}
    constexpr bool _eval_impl(std::integral_constant<expression_type, expression_type::greater>)    const {return lhs >  rhs;}
    constexpr bool _eval_impl(std::integral_constant<expression_type, expression_type::lesser>)     const {return lhs <  rhs;}
};

template<typename T, typename U, typename V, bool Relative>
constexpr ternary_expression<T, U, V, Relative> operator+(const binary_expression<T, U,expression_type::equal> & ex, const epsilon<V, Relative> & eps)
{
    return {ex.lhs, ex.rhs, eps.value};
}


template<typename T>
struct unary_expression
{
    T value;

    constexpr static expression_type type = expression_type::plain;

    template<typename = std::enable_if_t<std::is_convertible<T, bool>::value>>
    constexpr bool eval() const {return static_cast<bool>(value);}

    template<typename = std::enable_if_t<std::is_convertible<T, bool>::value>>
    constexpr operator bool() const {return static_cast<bool>(value);}

    template<typename U> constexpr binary_expression<T, const U&, expression_type::equal>     operator==(const U & rhs) const {return {value, rhs};}
    template<typename U> constexpr binary_expression<T, const U&, expression_type::not_equal> operator!=(const U & rhs) const {return {value, rhs};}
    template<typename U> constexpr binary_expression<T, const U&, expression_type::ge>        operator>=(const U & rhs) const {return {value, rhs};}
    template<typename U> constexpr binary_expression<T, const U&, expression_type::le>        operator<=(const U & rhs) const {return {value, rhs};}
    template<typename U> constexpr binary_expression<T, const U&, expression_type::greater>   operator> (const U & rhs) const {return {value, rhs};}
    template<typename U> constexpr binary_expression<T, const U&, expression_type::lesser>    operator< (const U & rhs) const {return {value, rhs};}

    template<typename U, typename V, bool Relative> constexpr ternary_expression<T, const U&, const V&, Relative>
        operator==(const epsilon_expression<U, V, Relative> & eps) const {return {value, eps.value, eps.tolerance};}

};


struct decomposer_t
{
    template<typename T> constexpr unary_expression<const T &> operator <=(const T & value) const { return {value}; }
    constexpr unary_expression<bool> operator <=(bool condition) const { return {condition}; }
};

constexpr static decomposer_t decomposer;


}

}

#endif //METAL_TEST_DECOMPOSER_HPP

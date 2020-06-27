# -*- coding: utf-8 -*-
from typing import Any, Union
from core.helpers.validator import Validator


class ReaMath:

    @staticmethod
    def summation(first_number, second_number):
        if Validator.number_control([first_number, second_number])[0]:
            first_number = Validator.number_control([first_number, second_number])[1][0]
            second_number = Validator.number_control([first_number, second_number])[1][1]
            return first_number + second_number
        else:
            return False

    @staticmethod
    def summation_list(number_list):
        total = 0
        if Validator.number_control(number_list)[0]:
            number_list = Validator.number_control(number_list)[1]
            for number in number_list:
                total += number
            return total, type(total)

    @staticmethod
    def extraction(first_number, second_number):
        if Validator.number_control([first_number, second_number])[0]:
            first_number = Validator.number_control([first_number, second_number])[1][0]
            second_number = Validator.number_control([first_number, second_number])[1][1]
            if first_number < second_number:
                return second_number - first_number
            else:
                return first_number - second_number
        else:
            return False

    @staticmethod
    def multiplication(multiplicand, multiplier):
        if Validator.number_control([multiplicand, multiplier])[0]:
            multiplicand = Validator.number_control([multiplicand, multiplier])[1][0]
            multiplier = Validator.number_control([multiplicand, multiplier])[1][1]
            return multiplicand * multiplier
        else:
            return False

    @staticmethod
    def multiplication_list(multiplier_list):
        multiply = 1
        if Validator.number_control(multiplier_list)[0]:
            multiplier_list = Validator.number_control(multiplier_list)[1]
            for number in multiplier_list:
                multiply *= number
            return multiply
        else:
            return False

    @staticmethod
    def division(divided, divisor):
        if Validator.number_control([divided, divisor])[0]:
            divided = Validator.number_control([divided, divisor])[1][0]
            divisor = Validator.number_control([divided, divisor])[1][1]
            if divided != 0 and divisor != 0:
                if divided > divisor:
                    return divided / divisor
                else:
                    return divisor / divided
            else:
                return False
        else:
            return False

    @staticmethod
    def division_floor(divided, divisor):
        if Validator.number_control([divided, divisor])[0]:
            divided = Validator.number_control([divided, divisor])[1][0]
            divisor = Validator.number_control([divided, divisor])[1][1]
            if divided != 0 and divisor != 0:
                if divided > divisor:
                    return divided // divisor
                else:
                    return divisor // divided
            else:
                return False
        else:
            return False

    @staticmethod
    def remainder(first_number, second_number):
        if Validator.number_control([first_number, second_number])[0]:
            first_number = Validator.number_control([first_number, second_number])[1][0]
            second_number = Validator.number_control([first_number, second_number])[1][1]
            return first_number % second_number
        else:
            return False

    @staticmethod
    def percent(number, ratio):
        if Validator.number_control([number, ratio])[0]:
            number = Validator.number_control([number, ratio])[1][0]
            ratio = Validator.number_control(([number, ratio]))[1][1]
            return (number * ratio) / 100
        else:
            return False

    @staticmethod
    def different_percent(first_number, second_number, boolean):
        if Validator.number_control([first_number, second_number])[0]:
            first_number = Validator.number_control([first_number, second_number])[1][0]
            second_number = Validator.number_control([first_number, second_number])[1][1]
            if boolean:
                if first_number < second_number:
                    return (first_number / second_number) * 100
                else:
                    return (second_number / first_number) * 100
            else:
                if first_number > second_number:
                    return (first_number / second_number) * 100
                else:
                    return (second_number / first_number) * 100
        else:
            return False

    @staticmethod
    def exponentiation(number, exponent):
        if Validator.number_control([number, exponent])[0]:
            number = Validator.number_control([number, exponent])[1][0]
            exponent = Validator.number_control([number, exponent])[1][1]
            return number ** exponent
        else:
            return False

    @staticmethod
    def rea_abs(number):
        if Validator.number_control([number])[0]:
            number = Validator.number_control([number])[1][0]
            if number > 0:
                return number
            else:
                return -number
        else:
            return False

    @staticmethod
    def rea_sqrt(number, expo, boolean):
        if Validator.number_control([number, expo])[0]:
            number = Validator.number_control([number])[1][0]
            expo = Validator.number_control([number, expo])[1][1]
            if number > 0 and expo >= 0:
                sqrt_number: Union[float, Any] = number ** (1 / expo)
                return ReaMath.call_sqrt(sqrt_number, boolean)
            else:
                return False
        else:
            return False

    @staticmethod
    def call_sqrt(sqrt_number, boolean):
        number = 0
        for i in range(1, 100):
            if i >= sqrt_number:
                number = i
                break
        if boolean:
            return number
        else:
            return sqrt_number

    # noinspection PyTypeChecker
    @staticmethod
    def average(number_list):
        if Validator.number_control(number_list)[0]:
            number_list = Validator.number_control(number_list)[1]
            return ReaMath.summation_list(number_list) / len(number_list)
        else:
            return False

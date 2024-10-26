import re
import time
import sys

from bs4 import BeautifulSoup
from src.utils import log_c, log


def extract_attribute(function_or_regex, html):
    if callable(function_or_regex):
        result = function_or_regex(BeautifulSoup(html, features="html.parser"))
        return result
    result = re.findall(function_or_regex, html)
    if len(result) > 0:
        # TODO: debug stuff here.. remove in release build..
        if len(result) > 1:
            if len(result[0]) != len(result[1]) or (len(result[0]) == len(result[1]) and result[0] != result[1]):
                print(f"WARNIG: got more than one match ({len(result)}), matched {result}. taking first one..")
        return result[0]
    log(f"WARNING: regex didn't match html: '{function_or_regex}'")
    return None

# data_to_extract:
#    key   -> name
#    value -> either a function that takes the soup object and returns the value
#             or     a regex that extracts a specific text

def extract_all(data_to_extract: dict, html: str):
    result = {}
    for key, value in data_to_extract.items():
        result[key] = extract_attribute(value, html)
    return result


def number_from_class(bfs, tag, classname, prop = 'class'):
    found = bfs.find_all(tag, {prop: classname})

    if len(found) < 1:
        log("WARNING: didn't find {},{},{}".format(tag, classname, prop))
        return None

    text = found[0].get_text()
    matches = re.findall(r'\d+[\.\,]?\d*[\.\,]?\d*[\.\,]?\d*[\.\,]?\d*[\.\,]?\d*[\.\,]?\d*[\.\,]?\d*', text)

    if len(matches) > 0:
        return matches[0]
    log("WARNING: didn't match any number in {},{},{}".format(tag, classname, prop))
    return None


#TODO: remove!
#TODO make more rubost currency reading functions that maybe also read in the currency format
def currency_dot_means_dot(bfs, tag, classname, prop = 'class'):
    text = number_from_class(bfs, tag, classname, prop)
    if text == None:
        return None
    supposed_float = text.replace(",", "")
    return supposed_float

def currency_comma_means_dot(bfs, tag, classname, prop = 'class'):
    text = number_from_class(bfs, tag, classname, prop)
    if text == None:
        return None
    supposed_float = text.replace(".", "").replace(",", ".")
    return supposed_float

def text_from_class(bfs, tag, classname, prop = 'class', key = None):
    elem = bfs.find_all(tag, {prop: classname})
    if len(elem) == 0:
        return "https://commons.wikimedia.org/wiki/File:Rickrolling_QR_code.png"
    if key == None:
        return elem[0].get_text()
    return elem[0][key]

# might be useful regex from https://stackoverflow.com/questions/354044/what-is-the-best-u-s-currency-regex

# re_currency_amount_us = r"[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}"
# re_currency_amount_us_cents_opt =  r"[+-]?[0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?"
# re_currency_amount_us_and_eu =  r"[+-]?[0-9]{1,3}(?:[0-9]*(?:[.,][0-9]{2})?|(?:,[0-9]{3})*(?:\.[0-9]{2})?|(?:\.[0-9]{3})*(?:,[0-9]{2})?)"


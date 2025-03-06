"""
Toy grammars to illustrate derivation and parsing.
"""
import random
# We always use Python type annotations to enforce stricter checking.
from typing import Dict, List, Optional
import re
import sys

# #1: the first grammar.
english_productions: Dict[str, List[str]] = {
    "<句子>": ["<主语><谓语><宾语>"],
    "<主语>": ["牛", "羊"],
    "<谓语>": ["吃", "喝"],
    "<宾语>": ["水", "草"],
}


# #2: a toy expression grammar that contains recursions.
exp_productions: Dict[str, List[str]] = {
    "<表达式>": ["<表达式><运算符><表达式>", "<整数>", "(<表达式>)"],
    "<运算符>": ["+", "-", "*", "/"],
    "<整数>": ["<数字><整数>", "<数字>"],
    "<数字>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


#3:
# Proposition grammar.
proposition_productions: Dict[str, List[str]] = {
    "<P>": ["True", "False", "<P> <B> <P>", "~<P>", "(<P>)", "<X>"],
    "<B>": ["/\\", "\\/", "->"],
    "<X>": ["x_<N>"],
    "<N>": ["<D><N>", "<D>"],
    "<D>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


## Part I: to derive a sentence from the start non-terminal.

# the number of terminals in a sentence
def num_of_non_terminals(s: str) -> int:
    return s.count("<")


# find any non-terminals in current sentence
def find_non_terminals(s: str) -> Optional[str]:
    the_match: Optional[re.Match[str]] = re.search(r"<[^>]*>", s)
    match the_match:
        case None: return None
        case _: return the_match.group(0)


def derive(productions: Dict[str, List[str]], sentence: str) -> str:
    # we control how many non-terminals can manifest in a sentence
    # otherwise, the algorithm may not terminate.
    threshold: int = 10
    current_num_of_nonterms: int = 1
    target: str = ""
    while True:
        # try to find the next non-terminal
        the_match: Optional[str] = find_non_terminals(sentence)
        if the_match is None: # find nothing, return the string
            return sentence
        else: # find one non-terminal,
            # then replace this non-terminal with one of its right-hand
            # first, get all the right hands for the non-terminal
            right_hands: List[str] = productions[the_match]
            # choose one right hand randomly
            found: bool = False
            while not found:
                target = random.choice(right_hands)
                num_non_terms: int = num_of_non_terminals(target)
                if current_num_of_nonterms -1 + num_non_terms < threshold:
                    current_num_of_nonterms += num_non_terms - 1
                    found = True

            # substitute the right hand
            sentence = sentence.replace(the_match, target, 1)

## Part II: 语法分析，即给定任意一个句子，判定其是否合法。
cursor: int = 0
numErrors: int = 0

def error(want: List[str], got: List[str]):
    global cursor
    global numErrors
    numErrors += 1
    # a dirty hack
    offset = 6*cursor + 2
    for i in range(0, offset):
        print(" ", end="")
    print("^")
    print(f"在位置{cursor}发现语法错误")
    print("只允许: ", end="")
    print(want, sep=", ")
    print("但发现: ", end="")
    print(got, sep=", ")
    cursor += 1

def parse_juzi(s: List[str]):
    global cursor
    global numErrors
    cursor = 0
    numErrors = 0
    print(f"正在分析句子：\n{s}")
    parse_zhu(s)
    parse_wei(s)
    parse_bin(s)
    if numErrors == 0:
        print("分析成功！")

def parse_zhu(s: List[str]):
    global cursor
    match s[cursor]:
        case "牛" | "羊":
            cursor += 1
            return
        case _:
            error(["牛", "羊"], [s[cursor]])

def parse_wei(s: List[str]):
    global cursor
    match s[cursor]:
        case "吃" | "喝":
            cursor += 1
            return
        case _:
            error(["吃", "喝"], [s[cursor]])

def parse_bin(s: List[str]):
    global cursor
    match s[cursor]:
        case "水" | "草":
            cursor += 1
            return
        case _:
            error(["水", "草"], [s[cursor]])


def print_productions(productions: Dict[str, List[str]],
                      argv,
                      start: str,
                      item: str):
    num_sentences: int = int(argv[1]) if len(sys.argv) > 1 else 10
    print(f"随机生成{num_sentences}个{item}：")
    for i in range(num_sentences):
        s: str = derive(productions, start)
        print(s)

if __name__ == '__main__':
    # Part I: 造若干个句子（默认10）
    print_productions(english_productions,sys.argv, "<句子>", "句子")
    print_productions(exp_productions, sys.argv, "<表达式>", "表达式")
    print_productions(proposition_productions, sys.argv, "<P>", "命题")

    # Part II: 语法分析
    parse_juzi(["牛", "吃", "牛"])
    parse_juzi(["牛", "吃", "水"])





















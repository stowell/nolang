import collections
import decimal


class Empty(object):
    def word(self, word, sym2val):
        try:
            return Number(decimal.Decimal(word))
        except decimal.InvalidOperation:
            if 'is' == word:
                #TODO: How do we handle this omission?
                return Error('What is is?')
            elif word in sym2val:
                return sym2val[word][-1]
            else:
                return Symbol(word)

    def response(self):
        return 'Empty expression'


class Program(object):
    def __init__(self):
        self.messages = []
        self.responses = []
        self.sym2val = collections.defaultdict(list)

    def message(self, message):
        words = message.split()
        if len(words) == 0:
            return ''
        if 0 == len(self.sym2val['that']):
            last = Empty()
            for word in words:
                last = last.word(word, self.sym2val)
            response = last.response()
        else:
            last = self.sym2val['that'][-1]
            word = words[0]
            last = last.word(word, self.sym2val)
            if isinstance(last, Error):
                #TODO: earlier line may have polluted sym2val
                last = Empty().word(word, self.sym2val)
            for word in words[1:]:
                last = last.word(word, self.sym2val)
            response = last.response()

        self.messages.append(message)
        self.responses.append(response)
        if isinstance(last, Number):
            self.sym2val['that'].append(last)

        return response


class Symbol(object):
    def __init__(self, symbol):
        self.symbol = symbol

    def word(self, word, sym2val):
        if 'is' == word:
            return Is(self.symbol)
        else:
            #TODO: do we handle numbers differently?
            return Error("Sorry, I don't (yet) know what to do with '%s' and '%s' together" % (self.symbol, word))

    def response(self):
        return 'Symbol ' + self.symbol


class Is(object):
    def __init__(self, symbol):
        self.symbol = symbol

    def word(self, word, sym2val):
        try:
            number = Number(decimal.Decimal(word))
            sym2val[self.symbol].append(number)
            return number #TODO: this prevents complex expressions
        except decimal.InvalidOperation:
            if word in sym2val:
                number = sym2val[word][-1]
                sym2val[self.symbol].append(number)
                return number
            else:
                #TODO: can symbols point to symbols?
                return Error("Sorry, I don't want to point '%s' to '%s' when I don't know what '%s' means" %  (self.symbol, word, word))

    def response(self):
        return self.symbol + ' is . . .'

class Error(object):
    def __init__(self, message):
        self.message = message

    def word(self, word, sym2val):
        return self

    def response(self):
        return self.message


class Number(object):
    def __init__(self, number):
        self.number = number

    def word(self, word, sym2val):
        if 'times' == word:
            return Times(self.number)
        elif 'over' == word:
            return Over(self.number)
        elif 'minus' == word:
            return Minus(self.number)
        else:
            return Error("I don't know what to do with the number %s and the word %s" % (str(self.number), word))

    def response(self):
        return str(self.number)


class Times(object):
    def __init__(self, left):
        self.left = left

    def word(self, word, sym2val):
        try:
            number = decimal.Decimal(word)
            return Number(self.left * number)
        except decimal.InvalidOperation:
            if word in sym2val:
                return Number(self.left * sym2val[word][-1].number)
            else:
                return Error("I don't know how to multiply %s and %s" % (self.left, word))

    
    def response(self):
        return str(self.left) + ' times . . .'


class Over(object):
    def __init__(self, left):
        self.left = left

    def word(self, word, sym2val):
        try:
            number = decimal.Decimal(word)
            return Number(self.left / number)
        except decimal.InvalidOperation:
            if word in sym2val:
                return Number(self.left / sym2val[word][-1].number)
            else:
                return Error("I don't know how to divide %s by %s" % (self.left, word))

    def response(self):
        return str(self.left) + ' over . . .'


class Minus(object):
    def __init__(self, left):
        self.left = left

    def word(self, word, sym2val):
        try:
            number = decimal.Decimal(word)
            return Number(self.left - number)
        except decimal.InvalidOperation:
            if word in sym2val:
                return Number(self.left - sym2val[word][-1].number)
            else:
                return Error("I don't know how to subtract %s from %s" % (word, self.left))

    def response(self):
        return str(self.left) + ' minus . . .'


def main():
    program = Program()
    while True:
        try:
            message = raw_input('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            print
            continue
        print program.message(message)


if __name__ == '__main__':
    main()
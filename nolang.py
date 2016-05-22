import collections
import pprint

def noeval(s, env):
    words = s.split()
    nwords = len(words)
    for i in xrange(nwords):
        word = words[i]
        if 'is' == word and (i > 0) and (i + 1 < nwords):
            last = words[i - 1]
            rest = tuple(words[i + 1:])
            env[last].append(rest)
    return env


def main():
    env = collections.defaultdict(list)
    while True:
        try:
            s = raw_input('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            print
            continue
        env = noeval(s, env)
        pprint.pprint(env)


if __name__ == '__main__':
    main()
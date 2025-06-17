import re

def test_allow_ascii():
    pwd = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    assert bool(re.match(r'^[\x00-\x7F]*$', pwd))


def test_letter_not_repeating():
    regex = re.compile(r'(\w)\1+')
    assert bool(re.match(regex, 'abbc'))
    assert bool(re.match(regex, 'aa'))


# def test_not_allow_consecutive():
#     regex = re.compile(r'^(\w).*')
#     assert bool(re.match(regex, 'aaaa'))
#     assert not bool(re.match(regex, 'abcd'))
#     assert not bool(re.match(regex, 'dcba'))
#     assert not bool(re.match(regex, 'badc'))
#     assert not bool(re.match(regex, 'acbd'))
#     assert not bool(re.match(regex, 'aceg'))
#     assert not bool(re.match(regex, '1111'))
#     assert not bool(re.match(regex, '1234'))
#     assert not bool(re.match(regex, '1432'))


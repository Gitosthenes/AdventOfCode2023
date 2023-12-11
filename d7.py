import inputs
from dataclasses import dataclass, field
from collections import defaultdict

CARD_RANKS = '- J 2 3 4 5 6 7 8 9 T Q K A'.split()
HAND_RANKS = 'HC 1P 2P 3K FH 4K 5K'.split()


@dataclass(order=True)
class Card:
    msort_idx: int = field(init=False, repr=False)
    mval: str

    def __post_init__(self):
        self.msort_idx = CARD_RANKS.index(self.mval)

    def __str__(self) -> str:
        return f'{self.mval}'

    def __hash__(self) -> int:
        return hash(self.mval)


@dataclass(order=True)
class Hand:
    mtype_score: int = field(init=False, repr=False)
    mcard_score: int = field(init=False, repr=False)

    mcards: list[Card, int]
    mtype: str
    mbet: int

    def __post_init__(self):
        self.mtype_score = HAND_RANKS.index(self.mtype)
        self.mcard_score = get_score(self.mcards)


# Helper Functions ==============================
def parse_line(as_str: str) -> (list[Card], int):
    (c_str, b_str) = tuple(as_str.split())

    parsed_cards = [Card(v) for v in list("".join(_ for _ in c_str))]
    parsed_type = get_hand_type(parsed_cards)
    parsed_bet = int(b_str)

    return parsed_cards, parsed_type, parsed_bet


def get_hand_type(pcards: list[Card]) -> str:
    checks = [
        (is_five_of_a_kind, '5K'),
        (is_four_of_a_kind, '4K'),
        (is_full_house, 'FH'),
        (is_three_of_a_kind, '3K'),
        (is_two_pair, '2P'),
        (is_one_pair, '1P')
    ]
    hand_type = 'HC'

    if Card('J') in pcards:
        for card_type in CARD_RANKS[2:]:
            subbed = [c if c != Card('J') else Card(card_type) for c in pcards]

            for fn, htype in checks:
                if fn(subbed) and HAND_RANKS.index(htype) > HAND_RANKS.index(hand_type):
                    hand_type = htype
    else:
        for fn, htype in checks:
            if fn(pcards):
                hand_type = htype
                break

    return hand_type


def get_score(pcards: list[Card]) -> int:
    score = 0
    magnitude = 13**5

    for card in pcards:
        score += magnitude * CARD_RANKS.index(card.mval)
        magnitude /= 13

    return score


def get_counts(pcards: list[Card]) -> defaultdict[Card, int]:
    card_counts = defaultdict(lambda: 0)

    for card in pcards:
        card_counts[card] += 1

    return card_counts


def is_five_of_a_kind(pcards: list[Card]) -> bool:
    test = sorted(
        get_counts(pcards)
        .values()
    )

    return sorted(
        get_counts(pcards)
        .values()
    ) == [5]


def is_four_of_a_kind(pcards: list[Card]) -> bool:
    test = sorted(
        get_counts(pcards)
        .values()
    )

    return sorted(
        get_counts(pcards)
        .values()
    ) == [1, 4]


def is_full_house(pcards: list[Card]) -> bool:
    test = sorted(
        get_counts(pcards)
        .values()
    )

    return sorted(
        get_counts(pcards)
        .values()
    ) == [2, 3]


def is_three_of_a_kind(pcards: list[Card]) -> bool:
    test = set(
        get_counts(pcards)
        .values()
    )

    return set(
        get_counts(pcards)
        .values()
    ) == {1, 3}


def is_two_pair(pcards: list[Card]) -> bool:
    test = sorted(
        get_counts(pcards)
        .values()
    )

    return sorted(
        get_counts(pcards)
        .values()
    ) == [1, 2, 2]


def is_one_pair(pcards: list[Card]) -> bool:
    test = set(
        get_counts(pcards)
        .values()
    )

    return set(
        get_counts(pcards)
        .values()
    ) == {1, 2}


# MAIN ==========================================
if __name__ == '__main__':
    # puzzle_input = '32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483'.split('\n')

    puzzle_input = inputs \
        .get_input(7) \
        .split('\n')

    hands = []
    for line in puzzle_input:
        cards, typ, bet = parse_line(line)
        hands.append(Hand(cards, typ, bet))

    sorted_hands = sorted(hands)
    ranked_hands = list(zip(sorted_hands, range(1, 1001)))
    p1 = sum(h[0].mbet*h[1] for h in ranked_hands)
    print(p1)

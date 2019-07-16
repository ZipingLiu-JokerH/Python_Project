import random


class Card(object):
    # A single card

    def __init__(self, suite, value):
        self._suit = suite
        self._value = value

    @property
    def suite(self):
        return self._suite

    @property
    def value(self):
        return self._value

    def __str__(self):
        if self._value == 1:
            face_str = 'A'
        elif self._value == 11:
            face_str = 'J'
        elif self._value == 12:
            face_str = 'Q'
        elif self._value == 13:
            face_str = 'K'
        else:
            face_str = str(self._value)
        return f'{self._suit}{face_str}'

    def __repr__(self):
        return self.__str__()


class Poker(object):
    # A deck of card

    def __init__(self):
        self._cards = [Card(suite, value) for suite in "♠♥♣♦" for value in range(1,14)]
        self._count = 0

    def shuffle(self):
        self._count = 0
        random.shuffle(self._cards)

    def deal(self):
        card = self._cards[self._count]
        self._count += 1
        return card


class Player(object):

    def __init__(self, name):
        self._name = name
        self._cards_on_hand = []

    @property
    def name(self):
        return self._name

    @property
    def cards_on_hand(self):
        return self._cards_on_hand

    def draw(self, card):
        self._cards_on_hand.append(card)

    def current_point(self):
        point = 0
        has_A = False
        for card in self._cards_on_hand:
            if card.value >= 10:
                point += 10
            else:
                point += card.value

            if card.value == 1:
                has_A = True

        A_point = point+10 if has_A else point
        return[point, A_point]


def find_winner(players):
    potential = []
    for player in players:
        p_scorer = player.current_point()
        if p_scorer[0] > 21 and p_scorer[1] > 21:
            pass
        else:
            potential.append(player)

    diff = {}
    min_diff = 21
    for player in potential:
        p_scorer = player.current_point()
        max_score = max(p_scorer[0], p_scorer[1])
        min_score = min(p_scorer[0], p_scorer[1])
        valid_score = max_score if max_score <= 21 else min_score
        diff[player.name] = 21 - valid_score
        if 21 - valid_score < min_diff:
            min_diff = 21 - valid_score

    winner = []
    for p in diff:
        if diff[p] == min_diff:
            winner.append(p)
    return winner

def main():
    p = Poker()
    p.shuffle()
    players = [Player('H'), Player('J'), Player('M')]
    for player in players:
        player.draw(p.deal())

    waiting_player = []
    while True:
        for player in players:
            if player in waiting_player:
                continue
            print(f"{player.name}'s Turn")
            p_point = player.current_point()
            print(f"You have cards {player.cards_on_hand}")
            print(f'Total score is: {p_point}')
            if p_point[0] > 21 and p_point[1] > 21:
                print(f'Sorry {player.name} loss')
                print('------------------------------')
                waiting_player.append(player)
                continue
            while True:
                reply = input(f'{player.name}, Do you want another card?(Yes/No)')
                if reply.lower() == 'yes':
                    card = p.deal()
                    print(f'You get card {card}')
                    player.draw(card)
                    break
                elif reply.lower() == 'no':
                    waiting_player.append(player)
                    break
                else:
                    print('Please enter Yes/No')

            print('------------------------------')
        if len(waiting_player) == len(players):
            break

    winner = find_winner(waiting_player)
    if len(winner) == 1:
        print(f'Congratulation {winner[0]} win the Game')
    else:
        print('Ops! There is a tie between ', end='')
        for name in winner:
            print(name, end=' ')
    print()
    print('------------------------------')

    print('Game summary')
    for player in waiting_player:
        print(player.name)
        print(player.cards_on_hand)
        print(player.current_point())



if __name__ == '__main__':
    main()
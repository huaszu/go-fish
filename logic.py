from random import shuffle


def deal_cards(deck, num_players):
    shuffle(deck)
    num_cards_per_hand: int = len(deck) // num_players

    hands: list[list] = []

    for i in range(num_players):
        hand: list = deck[:num_cards_per_hand]
        deck = deck[num_cards_per_hand:]
        hands.append(hand)
    
    return hands, deck


def get_hand_of_player(player, players, hands):
    index_in_players = players.index(player)
    index_in_hands = index_in_players
    hand = hands[index_in_hands]

    return hand


def get_rank_counts_of_hand(hand):
    rank_counts: dict[str, int] = dict()

    for card_rank in hand:
        rank_counts[card_rank] = rank_counts.get(card_rank, 0) + 1 

    return rank_counts


def get_books_from_rank_counts(rank_counts):
    player_books = []

    for card_rank, count in rank_counts.items():
        if count == 4:
            player_books.append(card_rank)

    return player_books


def assemble_books_of_all_players(players, hands):
    # Dictionary showing each player and that player's number of books
    books_status: dict[str: int] = dict()

    for player in players:
        hand = get_hand_of_player(player=player, players=players, hands=hands)
        rank_counts = get_rank_counts_of_hand(hand=hand)
        books = get_books_from_rank_counts(rank_counts=rank_counts)
        num_books = len(books)

        books_status[player] = len(books)

    return books_status


def identify_winner(books_status):
    max_books = max(books_status.values())

    # There can be more than one player with the same number of max books
    winners = [player for player, num_books in books_status.items() if num_books == max_books]

    return winners


def set_up_game():
    deck = [
        'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
        'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
        'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
        'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
    ]
    
    num_players: int = int(input("How many people are playing?  Please enter an integer: "))

    players: list = []
    for i in range(num_players):
        player = f"Player {str(i)}"
        players.append(player)

    # `deck` keeps track of the state of the deck at any moment
    # `hands` keeps track of the state of each player's hand at any moment
    hands, deck = deal_cards(deck, num_players)

    return players, hands, deck


def play_game():
    players, hands, deck = set_up_game()

    for player in players:
        # Show whose turn it is
        print(f"{player}'s turn")

        # Give information on current player's hand and books
        player_hand: list = get_hand_of_player(player=player,
                                                players=players,
                                                hands=hands)
        print(f"Your hand: {player_hand}")

        rank_counts = get_rank_counts_of_hand(player_hand)

        player_books: list = get_books_from_rank_counts(rank_counts)
        print(f"Your books: {player_books}")

        if len(deck) > 0:
            print(f"Deck has {len(deck)} cards left")
        else:
            print("Deck is empty")

        # Let player fish
        opponent: str = input("Choose a player to fish from: ")
        while opponent not in players or opponent == players:
            print("Invalid choice.  Be sure to enter your choice as, for example, Player 0.  Try again.")
            opponent = input("Choose a player to fish from: ")
        
        card_rank: str = input("Enter a rank to ask for: ")
        # Validate that player has that card rank in hand
        while card_rank not in player_hand:
            print("You do not have that rank in your hand.  You can only ask for a rank that you have in hand.  Try again.")
            card_rank = input("Enter a rank to ask for: ")
        
        opponent_hand: list = get_hand_of_player(player=opponent,
                                                    players=players,
                                                    hands=hands)
        cards_fished: list = [card for card in opponent_hand if card == card_rank]

        if len(cards_fished) > 0:
            print(f"{opponent} gave you cards {cards_fished}")

            # Update player's hand
            player_hand.extend(cards_fished)

            # Update hands with player's hand
            index_in_players = players.index(player)
            index_in_hands = index_in_players
            hands[index_in_hands] = player_hand

            # Update opponent's hand
            opponent_hand = [card for card in opponent_hand if card != card_rank]

            # Update hands with opponent's hand
            index_in_players = players.index(opponent)
            index_in_hands = index_in_players
            hands[index_in_hands] = opponent_hand

        else:
            print(f"{opponent} said Go Fish!")
            if len(deck) > 0:
                drawn_card = deck.pop() # deck gets updated

                # Update player's hand
                player_hand.append(drawn_card)
                print(f"You drew {drawn_card}")

                # Update hands with player's hand
                index_in_players = players.index(player)
                index_in_hands = index_in_players
                hands[index_in_hands] = player_hand

            else:
                print("Deck is empty")

        # Exit condition
        if len(deck) == 0:
            break
    
    books_status = assemble_books_of_all_players(players=players, hands=hands)
    winners = identify_winner(books_status=books_status)
    print(f"Deck is empty.  Game over!  {winners} won.") 
    # TODO: Edit text to show winners in more readable way


if __name__ == "__main__":
    play_game()
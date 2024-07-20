from nada_dsl import *

def return_val_if_any_false(list_of_bool, val):
    """
    Returns val if any boolean inside list_of_bool is false.
    """
    final_value = UnsignedInteger(0)
    for bool in list_of_bool:
        final_value = bool.if_else(final_value, val)
    return final_value

def initialize_bidders(nr_bidders):
    """
    Initialize bidders with unique identifiers.
    """
    bidders = []
    for i in range(nr_bidders):
        bidders.append(Party(name="Bidder" + str(i)))
    return bidders

def inputs_initialization(nr_bidders, bidders):
    """
    Initialize inputs for bids per bidder.
    """
    bids = []
    for b in range(nr_bidders):
        bids.append(SecretUnsignedInteger(Input(name="Bid" + str(b), party=bidders[b])))
    return bids

def find_highest_bid(nr_bidders, bids, outparty):
    """
    Find the highest bid and the winner.
    """
    highest_bid = bids[0]
    winner = UnsignedInteger(0)
    for b in range(1, nr_bidders):
        is_higher = bids[b] > highest_bid
        highest_bid = is_higher.if_else(bids[b], highest_bid)
        winner = is_higher.if_else(UnsignedInteger(b), winner)
    return Output(highest_bid, "HighestBid", outparty), Output(winner, "Winner", outparty)

def bid_validation(bids, outparty):
    """
    Validate bids to ensure they meet a minimum value.
    """
    minimum_bid = UnsignedInteger(1)
    valid_bids = []
    for bid in bids:
        is_valid = bid >= minimum_bid
        valid_bids.append(Output(is_valid, "ValidBid", outparty))
    return valid_bids

def nada_main():

    # 0. Compiled-time constants
    nr_bidders = 3

    # 1. Parties initialization
    bidders = initialize_bidders(nr_bidders)
    outparty = Party(name="OutParty")

    # 2. Inputs initialization
    bids = inputs_initialization(nr_bidders, bidders)

    # 3. Computation
    # Find the highest bid and the winner
    highest_bid_output, winner_output = find_highest_bid(nr_bidders, bids, outparty)
    # Validate bids
    valid_bids = bid_validation(bids, outparty)

    # 4. Output
    results = [highest_bid_output, winner_output] + valid_bids
    return results

# Call the main function to run the auction process
nada_main()

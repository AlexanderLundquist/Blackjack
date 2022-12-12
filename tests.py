# test the main loop

from main import Player, BJ_Game, BJ_Card, BJ_Deck, BJ_Player

def test_hand():
    player = BJ_Player("test")
    player.hand = [BJ_Card(2, "Hearts"), BJ_Card(3, "Hearts")]
    assert player.total == 5
    
    
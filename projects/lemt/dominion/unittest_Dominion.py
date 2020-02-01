from unittest import TestCase
import Dominion
import testUtility


class TestAction(TestCase):

    def set_up(self):
        self.player = Dominion.Player('Thomas')
        self.action_card = Dominion.Village()
        self.trash = []

    def test_init(self):
        # initialize test data
        self.set_up()

        # assert action card values
        self.assertEqual("Village", self.action_card.name)
        self.assertEqual(3, self.action_card.cost)
        self.assertEqual(2, self.action_card.actions)
        self.assertEqual(1, self.action_card.cards)
        self.assertEqual(0, self.action_card.buys)
        self.assertEqual(0, self.action_card.coins)

    def test_use(self):
        # initialize test data
        self.set_up()

        # instantiate the Action_card object an verify number of cards in hand
        self.assertEqual('Village', self.action_card.name)
        self.assertEqual(5, len(self.player.hand))

        # add action card to hand and use the action card
        self.player.hand.append(self.action_card)
        self.assertEqual(6, len(self.player.hand))
        self.action_card.use(self.player, self.trash)

        # verify that the length of the hand has decreased
        self.assertEqual(5, len(self.player.hand))

    def test_augment(self):
        # initialize test data
        self.set_up()
        self.player.buys = 1
        self.player.actions = 0
        self.player.purse = 100
        self.player.cards = 1

        # augment action card, verify change in player values
        self.action_card.augment(self.player)
        self.assertEqual(2, self.player.actions)
        self.assertEqual(1, self.player.cards)
        self.assertEqual(1, self.player.buys)
        self.assertEqual(100, self.player.purse)


class TestPlayer(TestCase):

    def set_up(self):
        # Data setup
        self.player = Dominion.Player('Thomas')

    def test_action_balance(self):
        # set up and instantiate action card
        self.set_up()
        self.player.balance = self.player.action_balance()

        # player begins with no action card, so value should return 0
        self.assertEqual(0, self.player.balance)

        # instantiate an action card and add to player stack
        action_card = Dominion.Festival()
        self.player.deck.append(action_card)

        # call action_balance should return a value not equal to 0
        self.player.balance = self.player.action_balance()
        self.assertIsNot(0, self.player.balance)

    def test_calcpoints(self):
        # set up and instantiate Garden card
        self.set_up()
        self.player.points = 0

        # 1 victory point for every 10 cards in stack
        # assert change in value with different size stacks
        # first assert player begins game with 3 victory points
        self.player.points = self.player.calcpoints()
        self.assertEqual(3, self.player.points)

        # test 11 cards in stack, including 1 gardens
        # assert victory points equal to 4
        self.player.deck.append(Dominion.Gardens())
        self.assertEqual(11, len(self.player.stack()))
        self.player.points = self.player.calcpoints()
        self.assertEqual(4, self.player.points)

        # test 21 card stack, assert victory points equal to 5
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.player.deck.append(Dominion.Copper())
        self.assertEqual(21, len(self.player.stack()))
        self.player.points = self.player.calcpoints()
        self.assertEqual(5, self.player.points)

    def test_draw(self):
        # data set up
        self.set_up()

        # verify hand begins with 5 cards, assert 6 after draw
        self.assertEqual(5, len(self.player.hand))
        self.player.draw()
        self.assertEqual(6, len(self.player.hand))

        # test for deck to replenish, add cards to discard pile
        self.player.deck = []
        self.assertEqual(0, len(self.player.deck))
        self.player.discard.append(Dominion.Cellar)
        self.player.discard.append(Dominion.Cellar)
        self.player.discard.append(Dominion.Cellar)
        self.player.discard.append(Dominion.Cellar)
        self.player.discard.append(Dominion.Cellar)

        # draw card, total in hand should equal to 7
        self.player.draw()
        self.assertEqual(7, len(self.player.hand))

    def test_cardsummary(self):
        # data setup
        self.set_up()
        card_summary = self.player.cardsummary()
        self.assertEqual(3, card_summary['VICTORY POINTS'])

        # add a card to the player stack and verify change in value
        # province has a victory point value of 6, total equal to 9
        self.player.deck.append(Dominion.Province())
        card_summary = self.player.cardsummary()
        self.assertEqual(9, card_summary['VICTORY POINTS'])


class TestGameOver(TestCase):

    def set_up(self):
        self.player_names = testUtility.getPlayers()
        self.nV = testUtility.getVictoryCards(self.player_names)
        self.nC = testUtility.getCurseCards(self.player_names)
        self.box = testUtility.getBoxes(self.nV)
        self.supply = testUtility.getSupply(self.nV, self.nC, self.player_names, self.box)

    def test_gameover(self):
        # set up data
        self.set_up()
        game_over = Dominion.gameover(self.supply)
        self.assertEqual(False, game_over)

        # set province cards to 0 sets gameover to true
        self.supply["Province"] = [Dominion.Province()] * 0
        game_over = Dominion.gameover(self.supply)
        self.assertEqual(True, game_over)

        # set three supply piles to empty sets gameover to true
        self.supply = testUtility.getSupply(self.nV, self.nC, self.player_names, self.box)
        self.supply["Gold"] = [Dominion.Gold()] * 0
        self.supply["Estate"] = [Dominion.Estate()] * 0
        self.supply["Duchy"] = [Dominion.Duchy()] * 0
        game_over = Dominion.gameover(self.supply)
        self.assertEqual(True, game_over)



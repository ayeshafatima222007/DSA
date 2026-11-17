from Test import test_setup
from Test import test_game_logic


def main():
    print("Running setup tests:")
    test_setup.testStackIsLifo()
    test_setup.testQueueIsFifo()
    test_setup.testLinkedListSplitAndExtend()
    test_setup.testDeckHas52DifferentCards()
    test_setup.testStartingDeal()
    test_setup.testNewGameResetsEverything()

    print("Running game logic tests:")
    test_game_logic.testTableauRules()
    test_game_logic.testFoundationRules()
    test_game_logic.testMoveGroupAndFlip()
    test_game_logic.testInvalidMoveChangesNothing()
    test_game_logic.testDrawRecycleAndUndo()
    test_game_logic.testDrawThree()
    test_game_logic.testWin()
    test_game_logic.testHint()
    test_game_logic.testHintsAreLegal()
    test_game_logic.testScoring()
    test_game_logic.testRedo()
    test_game_logic.testRandomGames()

    print()
    print("ALL TESTS PASSED (18 test groups)")


if __name__ == "__main__":
    main()
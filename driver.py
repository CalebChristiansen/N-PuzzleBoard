'''
Created on Jan 25, 2018

@author: mroch
'''

from tileboard import TileBoard


def driver():
    size = 8  # N puzzle
    
    # Check
    
    # Create a new board and see if we got lucky
    #b3 = TileBoard(size, multiple_solutions=True,verbose=True)
    #b1 = TileBoard(size, multiple_solutions=True,verbose=True)
    #b2 = TileBoard(size, multiple_solutions=True,force_state=(1,2,3,4,5,6,7,8, None),verbose=True)
    b = TileBoard(size, multiple_solutions=False, force_state=(1, 2, 3, 4, 5, 6, None, 7, 8), verbose=False)


    #if (b3 == b2):
    #    print("the boards are equal")
    #else:
    #    print("the boards are not equal")


    #print(b1.solved())
    #b3.move([0, -1])
    #print(b1.get_actions())

    solved = b.solved()
    
    while not solved:
        print(b)        # show the board
        
        # Generate possible actions and corresponding labels a, b, c
        actions = b.get_actions()
        action_labels = [chr(ord('a')+idx) for idx in range(len(actions))]
        
        # Print list of actions, end="" means no newline
        print("Valid actions (delta row, delta col): ")
        for (label, move) in zip(action_labels, actions):
            print("{}: {}.  ".format(label, move), end="")
        print()
        
        # Let user select a valid choice
        useraction = None
        prompt = "move choice:  "
        while useraction not in action_labels:
            useraction = input(prompt)
            prompt = "bad choice, try again: "
        print(useraction)
        
        # Convert choice to index and execute move
        actionidx = ord(useraction) - ord('a')
        b = b.move(actions[actionidx])
        
        solved = b.solved()  # all done?
        
    print("Congratulations, you did it!")

        
        
    
if __name__ == '__main__':
    driver()
# The Brooklyn 99 Captain Holt conundrum
# There are 12 islanders on an island 11 weigh exactly the same but one is either slightly heavier or slightly lighter.
# You must find which one. There are no scales on the island, but there is a see saw, however, you may only use it 3 times.
# How do you find them?

from enum import Enum
import random

# Lets define an islander, let's be callous and just give them an id and a weight
class Islander:
    def __init__(self, id, name, weight):
        self.id = id
        self.name = name
        self.weight = weight
    def __repr__(self):
        return self.name

# And a seesaw
# First its enumerated possible results
class SeeSawResult(Enum):
    BALANCED = 1
    TILT_LEFT = 2
    TILT_RIGHT = 3

# Then the seesaw itself
class SeeSaw:
    def __init__(self):
        self.count = 0
        pass

    def weigh(self, left_side_group, right_side_group):
        self.count += 1
        sum_left = sum([i.weight for i in left_side_group])
        sum_right = sum([i.weight for i in right_side_group])
        result = None

        left = ", ".join([i.name for i in left_side_group])
        right = ", ".join([i.name for i in right_side_group])
        line_1 = "%s    %s"
        line_2 = "%s /\ %s"

        print("Seesaw Use #%d" % self.count)
        if sum_left == sum_right:
            print(line_1 % (left, right))
            print(line_2 % (" "*len(left), " "*len(right)))
            result = SeeSawResult.BALANCED
        elif sum_left > sum_right:
            print(line_1 % (" " * len(left), right))
            print(line_2 % (left, " " * len(right)))
            result = SeeSawResult.TILT_LEFT
        elif sum_right > sum_left:
            print(line_1 % (left, " " * len(right)))
            print(line_2 % (" " * len(left), right))
            result = SeeSawResult.TILT_RIGHT
        print("")
        return result

# Now let's define our island:
class Island:
    ISLANDER_NAMES = ["Andy", "Brad", "Carl", "Dave", "Erik", "Fred", "Greg", "Hank", "Iain", "John", "Kyle", "Luke"]
    def __init__(self):
        self.islanders = {}
        self.seesaw = SeeSaw()

        default_weight = 2
        ids = range(1, 13)
        # Select an id at random to be our odd one out
        odd_ball = random.choice(ids)
        # And randomly decide if they're heavier or lighter
        oddball_weight = random.choice((1, 3))
        # Now create all the islanders
        random.shuffle(self.ISLANDER_NAMES)

        for id in ids:
            name = self.ISLANDER_NAMES[id-1]
            # Either they're the odd ball
            if id == odd_ball:
                islander = Islander(id, name, oddball_weight)
                self.cheat_id = id
            # Or a regular joe
            else:
                islander = Islander(id, name, 2)
            #add the islander to the set of islanders with an unknown weight
            self.islanders[id] = islander

    # We've recorded which islander is the odd one our, so we can cheat to get the answer without doing the calculations
    # (though really we'll just use this to check our answer)
    def cheat(self):
        return self.islanders[self.cheat_id]

    def find_oddball(self):
        # Step one, lets divide the islanders into three groups of 4, we'll weigh the first group of 4 against the second
        # group of 4
        left = set([self.islanders[1], self.islanders[2], self.islanders[3], self.islanders[4]])
        right = set([self.islanders[5], self.islanders[6], self.islanders[7], self.islanders[8]])
        other = set([self.islanders[9], self.islanders[10], self.islanders[11], self.islanders[12]])
        print("Initially divide the Islanders into 3 groups:")
        print("[%s] [%s] [%s]" % (", ".join([i.name for i in left]), ", ".join([i.name for i in right]),
                                  ", ".join([i.name for i in other])))
        print("")

        result = self.seesaw.weigh(left, right)

        # If the seesaw is balanced
        if result == SeeSawResult.BALANCED:
            # Islanders 1 through 8 are safe, they all must weigh the same, the culprit must be 9 to 12 group
            # Create two new groups using three islanders of known weight and 3 from the 3rd group. Leave one of the
            # 3rd group of islanders out.
            left = set([self.islanders[1], self.islanders[2], self.islanders[9]])
            right = set([self.islanders[3], self.islanders[10], self.islanders[11]])
            result = self.seesaw.weigh(left, right)

            if result == SeeSawResult.BALANCED:
                #If we're balanced then the culprit is the one missing from the scale: 12
                return self.islanders[12]
            else:
                # if we're unbalanced then one of 9, 10, 11 is the culprit, so drop one, shuffle and try
                # again
                left = set([self.islanders[1], self.islanders[2], self.islanders[11]])
                right = set([self.islanders[3], self.islanders[4], self.islanders[10]])

                # We need to remember what the seesaw did last time so we can compare it the result time around
                last_result = result
                result = self.seesaw.weigh(left, right)

                if result == SeeSawResult.BALANCED:
                    # If the seesaw now balances the islander we dropped was the odd one out
                    return self.islanders[9]
                elif result == last_result:
                    # if the seesaw still tilts in the same direction then the islander that remained in place is the culprit
                    return self.islanders[10]
                else:
                    # Otherwise the islander that swapped positions is at fault:
                    return self.islanders[11]
        else:
            # the other group, the one we didn't weigh (9, 10, 11, 12) must be normal
            last_result = result
            # Drop two elements from the left hand side and one from the other, shuffle and replace them with known quanities:
            left = set([self.islanders[9], self.islanders[10], self.islanders[11], self.islanders[1]])
            right = set([self.islanders[2],  self.islanders[3],self.islanders[5], self.islanders[6]])
            result = self.seesaw.weigh(left, right)

            if result == SeeSawResult.BALANCED:
                # One of the disposed islanders is at fault (4,7,8), use the same trick as last time to determine which of the three
                # is the culprit
                left = set([self.islanders[9], self.islanders[7]])
                right = set([self.islanders[11], self.islanders[8]])
                result = self.seesaw.weigh(left, right)
                if result == SeeSawResult.BALANCED:
                    # If they balance the one we didn't weigh is the odd one out
                    return self.islanders[4]
                elif result != last_result:
                    # If it tilts in the same direction it's the one that stayed in place
                    return self.islanders[7]
                else:
                    # If it tilts in the opposite direction it's the one we swapped over
                    return self.islanders[8]
            elif result == last_result:
                # It's one of the elements that didn't move (1, 5, 6)
                # Use the same trick again
                left = set([self.islanders[9], self.islanders[10]])
                right = set([self.islanders[1],  self.islanders[5]])
                result = self.seesaw.weigh(left, right)
                if result == SeeSawResult.BALANCED:
                    return self.islanders[6]
                elif result != last_result:
                    return self.islanders[1]
                else:
                    return self.islanders[5]
            else:
                # Its one of the transient ones (2 or 3)
                # Similar but with 2 we won't need to worry about the direction of the seesaw
                left = set([self.islanders[9]])
                right = set([self.islanders[2]])
                result = self.seesaw.weigh(left, right)
                if result == SeeSawResult.BALANCED:
                    return self.islanders[3]
                return self.islanders[2]
        return None


if __name__ == "__main__":
    success = 0
    iterations = 1000
    print("We're going to try this %d times, with a randomised islander who's randomly heavier or lighter than the others to show it working:\n" % iterations)
    print("The comments in the code of main.py should explain how the method works.\n\n")
    for i in range(0, iterations):
        island = Island()
        #Use the seesaw method to determine the odd one out
        odd_ball = island.find_oddball()
        # Then just use a programmatic lookup to find the correct islander, so should the seesaw method fail,
        # we can show who it should have been.
        correct = island.cheat()
        if odd_ball is not None:
            if odd_ball.weight != 2:
                success += 1
                print("Found the odd one out: %s" % odd_ball)
                weight_str = "ligher"
                if odd_ball.weight > 2:
                    weight_str = "heavier"
                print("Yup, %s was %s than the others" % (odd_ball, weight_str))
            else:
                print("Didn't find the odd one out. Should have been: %s" % correct)
        else:
            print("Undecided after %d uses of the seesaw" % island.seesaw.count)
        print("\n-------------------------------------------------------------\n")

    print("Success Rate %f%%" % (success * 100/iterations))
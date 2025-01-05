from random import randint

class RollEngine:
    def roll(self, roll_string):
        """ 
        Roll XdY dice, where X is the number of dice 
        and Y the number of sides per die. 
        
        Args:
            roll_string (str): A dice string on the form XdY.
        Returns:
            int: The result of the roll. 
            
        """ 
        
        number, die_size = roll_string.split("d", 1)

        number = int(number)
        die_size = int(die_size)

        return sum(randint(1, die_size) for _ in range(number))

    def roll_with_advantage_or_disadvantage(self, advantage=False, disadvantage=False):
        if not (advantage or disadvantage) or (advantage and disadvantage):
            return self.roll("1d20")
        elif advantage:
            # advantage - highest of 2 rolls
            return max(self.roll("1d20"), self.roll("1d20"))
        else:
            # disadvantage - lowest of 2 rolls
            return min(self.roll("1d20"), self.roll("1d20"))

    def saving_throw():
        pass

    def opposed_saving_throw():
        pass

    def morale_check():
        pass

    def heal_from_rest():
        pass

dice = RollEngine()

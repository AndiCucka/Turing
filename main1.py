#!/usr/bin/env python3
"""
Created by: Andi Cucka2
Created on: Sept 2023
This is "Turing Machine" program that accepts the state machine rules
    and the initial "tape" and then runs
"""

import time

class Tape(object):
    
    blank_symbol = " "
    
    def __init__(self, tape_string=""):
        self.__tape = dict(enumerate(tape_string))
        
    def __str__(self):
        s = ""
        min_used_index = min(self.__tape.keys()) 
        max_used_index = max(self.__tape.keys())
        for i in range(min_used_index, max_used_index):
            s += self.__tape[i]
        return s    
   
    def __getitem__(self, index):
        if index in self.__tape:
            print("Read:  " + self.__tape[index] + " at position: " + str(index))
            return self.__tape[index]
        else:
            return Tape.blank_symbol

    def __setitem__(self, pos, char):
        print("Write: " + char + " at position: " + str(pos))
        self.__tape[pos] = char
        print("Current tape: ", end="")
        for key, value in self.__tape.items():
            print(value, end="")
        print()

        
class TuringMachine(object):
    
    def __init__(self, 
                 tape="",
                 blank_symbol=" ",
                 initial_state="",
                 final_states=None,
                 transition_function=None):
        self.__tape = Tape(tape)
        self.__head_position = 0
        self.__blank_symbol = blank_symbol
        self.__current_state = initial_state
        if transition_function is None:
            self.__transition_function = {}
        else:
            self.__transition_function = transition_function
        if final_states is None:
            self.__final_states = set()
        else:
            self.__final_states = set(final_states)
        
    def get_tape(self): 
        return str(self.__tape)
    
    def step(self):
        char_under_head = self.__tape[self.__head_position]
        x = (self.__current_state, char_under_head)
        if x in self.__transition_function:
            y = self.__transition_function[x]
            self.__tape[self.__head_position] = y[1]
            if y[2] == "R":
                self.__head_position += 1
                print("  ↣ Move head 1 right")
            elif y[2] == "L":
                self.__head_position -= 1
                print("  ↢ Move head 1 left")
            self.__current_state = y[0]
            print("             ", end="")
            for head_position_counter in range(self.__head_position):
                print(" ", end="")
            print("▲")
            time.sleep(1.0)

    def final(self):
        if self.__current_state in self.__final_states:
            return True
        else:
            return False

# State machine for counting from 11 to 16 in binary
state_machine = {
    ("init", "0"): ("init", "0", "R"),  # If seeing 0, keep it and move right
    ("init", "1"): ("init", "1", "R"),  # If seeing 1, keep it and move right
    ("init", " "): ("final", " ", "N"),  # If seeing blank, halt
    ("init", "#"): ("add1", " ", "L"),  # If seeing # (end of tape), go to the first bit and move left
    ("add1", "0"): ("init", "1", "N"),  # If seeing 0, change it to 1 and halt
    ("add1", "1"): ("add1", "0", "L"),  # If seeing 1, change it to 0 and move left
}

# Initial tape (starting from binary 11)
t = TuringMachine("11# ", initial_state="init", final_states={"final"}, transition_function=state_machine)

print("Input on Tape:\n              " + t.get_tape())
print("              ▲" + "\n")
original_tape = t.get_tape()

while not t.final():
    t.step()

print("\nResult of the Turing machine calculation:")
print("Original tape: " + original_tape)
print("Final tape   : " + t.get_tape())
print("\nDone.")
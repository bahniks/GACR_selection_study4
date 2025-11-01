#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from collections import OrderedDict

from common import InstructionsFrame
from gui import GUI
from constants import SVO_PROBABILITY

instructions = f"""Pod tímto oknem najdete 6 voleb, které zaznamenáte zvolením jednoho z tlačítek v každém z 6 řádků. Volby mění rozdělení odměn mezi vámi a jiným účastníkem studie, se kterým jste ještě nebyli spárováni. Jiný účastník bude podobně dělat rozhodnutí, která mohou ovlivnit Vaši odměnu. Neexistují žádné správné nebo špatné odpovědi, jde pouze o osobní preference.

Až tuto úlohu dokončíte, bude s pravděpodobností {int(SVO_PROBABILITY*100)} % vybráno náhodně jedno z rozhodnutí (každé se stejnou pravděpodobností) a realizováno. Výsledek se dozvíte na konci studie."""

class SVOTable(Canvas):
    def __init__(self, root, you_values=None, other_values=None, callback=None):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.root = root
        self.callback = callback
        
        # Values for the table
        self.you_values = you_values
        self.other_values = other_values

        self.selected_option = StringVar()
        
        # Create the table
        self.create_table(you_values, other_values)
    
    def create_table(self, you_values, other_values):
        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        
        # Header for "You receive"
        you_label = ttk.Label(self, text="Vy obdržíte:", font = "helvetica 15 bold", background = "white")
        you_label.grid(row=0, column=0, padx=10, pady=2, sticky="w")    

        # Header for "Other receives"
        other_label = ttk.Label(self, text="Jiný účastník obdrží:", font = "helvetica 15 bold", background = "white")
        other_label.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        for col in range(len(you_values)):
            # Radio buttons row (between the two data rows)
            radio = ttk.Radiobutton(self, variable=self.selected_option, value=col)
            radio.grid(row=1, column=col+1, padx=10)

            # Values for "Other receives" row
            label = ttk.Label(self, text=str(other_values[col]), font=("helvetica", 15), background="white", width = 3)
            label.grid(row=2, column=col+1, padx=10, pady=2)

            # Values for "You receive" row
            label = ttk.Label(self, text=str(you_values[col]), font=("helvetica", 15), background="white", width = 3)
            label.grid(row=0, column=col+1, padx=10, pady=2)

        # Right side "You receive" label
        you_label_right = ttk.Label(self, text="Vy obdržíte:", font=("helvetica", 15), background="white")
        you_label_right.grid(row=0, column=len(you_values)+1, padx=20, pady=2, sticky="e")

        # Right side "Other receives" header and dynamic value displays
        other_label_right = ttk.Label(self, text="Jiný účastník obdrží:", font=("helvetica", 15), background="white")
        other_label_right.grid(row=2, column=len(other_values)+1, padx=20, pady=2, sticky="e")

        # Vars and labels to show the currently selected values
        self.selected_you_var = StringVar(value="-")
        self.selected_other_var = StringVar(value="-")

        you_value_display = ttk.Label(self, textvariable=self.selected_you_var, font=("helvetica", 15), background="white", width = 3)
        you_value_display.grid(row=0, column=len(you_values)+2, pady=2, sticky="w")
        you_currency_label = ttk.Label(self, text="Kč", font=("helvetica", 15), background="white")
        you_currency_label.grid(row=0, column=len(you_values)+3, pady=2, sticky="w")

        other_value_display = ttk.Label(self, textvariable=self.selected_other_var, font=("helvetica", 15), background="white", width = 3)
        other_value_display.grid(row=2, column=len(other_values)+2, pady=2, sticky="w")
        other_currency_label = ttk.Label(self, text="Kč", font=("helvetica", 15), background="white")
        other_currency_label.grid(row=2, column=len(other_values)+3, pady=2, sticky="w")

        # Update the displays when a radio button is selected
        def update_selected(*_):
            val = self.selected_option.get()
            try:
                idx = int(val)
                self.selected_you_var.set(str(you_values[idx]))
                self.selected_other_var.set(str(other_values[idx]))
            except Exception:
                self.selected_you_var.set("-")
                self.selected_other_var.set("-")
            self.callback()

        # Trace changes to the selection variable
        self.selected_option.trace("w", update_selected)
    
    def get_selection(self):
        """Returns the selected option index"""
        try:
            return int(self.selected_option.get())
        except ValueError:
            return None


class SVO(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = instructions, proceed = True, height = "auto", savedata = True)
        
        # Data extracted from the image - six different scenarios
        scenarios = [
            # Scenario 1
            {
                'you_values': [85, 85, 85, 85, 85, 85, 85, 85, 85],
                'other_values': [85, 76, 68, 59, 50, 41, 33, 24, 15]
            },
            # Scenario 2  
            {
                'you_values': [85, 87, 89, 91, 93, 94, 96, 98, 100],
                'other_values': [15, 19, 24, 28, 33, 37, 41, 46, 50]
            },
            # Scenario 3
            {
                'you_values': [50, 54, 59, 63, 68, 72, 76, 81, 85],
                'other_values': [100, 98, 96, 94, 93, 91, 89, 87, 85]
            },
            # Scenario 4
            {
                'you_values': [50, 54, 59, 63, 68, 72, 76, 81, 85],
                'other_values': [100, 89, 79, 68, 58, 47, 36, 26, 15]
            },
            # Scenario 5
            {
                'you_values': [100, 94, 88, 81, 75, 69, 63, 56, 50],
                'other_values': [50, 56, 63, 69, 75, 81, 88, 94, 100]
            },
            # Scenario 6
            {
                'you_values': [100, 98, 96, 94, 93, 91, 89, 87, 85],
                'other_values': [50, 54, 59, 63, 68, 72, 76, 81, 85]
            }
        ]
        
        # Create frame to hold all SVO tables
        self.svo_frame = Frame(self, bg="white")
        self.svo_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Create six SVO tables
        self.svo_tables = []
        for i, scenario in enumerate(scenarios):
            table = SVOTable(self.svo_frame, you_values=scenario['you_values'], other_values=scenario['other_values'], callback=self.checkAll) 
            table.grid(row=i, column=0, pady=15, sticky="ew")
            self.svo_tables.append(table)
        
        # Configure grid weights
        self.svo_frame.columnconfigure(0, weight=1)

        self.next["state"] = "disabled"
        self.next.grid(row=3, column=0, columnspan=3, pady=5)
    
    def checkAll(self):
        # Override to ensure at least one selection is made across all tables
        for table in self.svo_tables:
            if table.get_selection() is None:
                return
        else:
            self.next["state"] = "!disabled"        
    
    def write(self):
        # Write all selections to the file
        self.file.write("SVO\n")        
        for i, table in enumerate(self.svo_tables):
            selection = table.get_selection()            
            you_val = table.you_values[selection]
            other_val = table.other_values[selection]
            self.file.write(f"{i+1}_{selection}_{you_val}_{other_val}\t")       
        self.file.write("\n")             


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([SVO])
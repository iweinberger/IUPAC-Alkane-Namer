# Author: Ilan Weinberger
# Date: June 06 2025
# Description: Core molecular modeling classes and support functions. This module contains the Atom class (responsible for storing molecular structure and rendering) as well as helper utilities for collision detection and molecule serialization.


import pygame
from math import cos, sin, asin, radians, degrees, sqrt
from types import MethodType as method
import colors as color_scheme
from typing import Tuple
from heapq import nlargest
from pickle import Pickler, Unpickler

def collidepoint(rect: pygame.Rect, point: tuple[int, int]) -> bool:
    """Check if a point is inside a rectangle.

    Args:
        rect: The rectangle to check.
        point: The point to check (x, y).

    Returns:
        bool: True if the point is inside the rectangle, False otherwise.
    """
    return rect.left <= point[0] <= rect.right and rect.top <= point[1] <= rect.bottom

class Atom:
    # Initialize Pygame
    pygame.init()

    ###                                      ###
    ### BEGIN DEFINITION OF CLASS ATTRIBUTES ###
    ###                                      ###

    SECONDARY_BOND_LENGTH = 20 
    PRIMARY_BOND_LENGTH = 50

    PRIMARY_SYMBOL_FONT = pygame.font.Font('fonts/Orbitron_Bold.ttf', 12)
    SECONDARY_SYMBOL_FONT = pygame.font.Font('fonts/Orbitron_Bold.ttf', 8)

    SYMBOLS = {
        'C': PRIMARY_SYMBOL_FONT.render('C', True, color_scheme.GREEN),
        'CC': PRIMARY_SYMBOL_FONT.render('C', True, color_scheme.RED),
        'H': SECONDARY_SYMBOL_FONT.render('H', True, color_scheme.WHITE),
        'O': SECONDARY_SYMBOL_FONT.render('O', True, color_scheme.GREEN),
        'F': SECONDARY_SYMBOL_FONT.render('F', True, color_scheme.YELLOW),
        'Cl': SECONDARY_SYMBOL_FONT.render('Cl', True, color_scheme.YELLOW),
        'Br': SECONDARY_SYMBOL_FONT.render('Br', True, color_scheme.YELLOW),
        'I': SECONDARY_SYMBOL_FONT.render('I', True, color_scheme.YELLOW),
        'At': SECONDARY_SYMBOL_FONT.render('At', True, color_scheme.YELLOW)
    }
    CARBON_SYMBOL = SYMBOLS['C']

    # Globally define the periodic table (SOURCE: Chat GPT).
    PERIODIC_TABLE = [
        ["H", 1.008, 1],
        ["He", 4.002602, 0],
        ["Li", 6.94, 1],
        ["Be", 9.0121831, 2],
        ["B", 10.81, 3],
        ["C", 12.011, 4],
        ["N", 14.007, 3],
        ["O", 15.999, 2],
        ["F", 18.998403163, 1],
        ["Ne", 20.1797, 0],
        ["Na", 22.98976928, 1],
        ["Mg", 24.305, 2],
        ["Al", 26.9815385, 3],
        ["Si", 28.085, 4],
        ["P", 30.973761998, 3],
        ["S", 32.06, 2],
        ["Cl", 35.45, 1],
        ["Ar", 39.948, 0],
        ["K", 39.0983, 1],
        ["Ca", 40.078, 2],
        ["Sc", 44.955908, 3],
        ["Ti", 47.867, 4],
        ["V", 50.9415, 5],
        ["Cr", 51.9961, 6],
        ["Mn", 54.938044, 6],
        ["Fe", 55.845, 6],
        ["Co", 58.933194, 6],
        ["Ni", 58.6934, 4],
        ["Cu", 63.546, 2],
        ["Zn", 65.38, 2],
        ["Ga", 69.723, 3],
        ["Ge", 72.63, 4],
        ["As", 74.921595, 3],
        ["Se", 78.971, 2],
        ["Br", 79.904, 1],
        ["Kr", 83.798, 0],
        ["Rb", 85.4678, 1],
        ["Sr", 87.62, 2],
        ["Y", 88.90584, 3],
        ["Zr", 91.224, 4],
        ["Nb", 92.90637, 5],
        ["Mo", 95.95, 6],
        ["Tc", 98.0, 7],
        ["Ru", 101.07, 6],
        ["Rh", 102.90550, 4],
        ["Pd", 106.42, 4],
        ["Ag", 107.8682, 1],
        ["Cd", 112.414, 2],
        ["In", 114.818, 3],
        ["Sn", 118.71, 4],
        ["Sb", 121.76, 3],
        ["Te", 127.60, 2],
        ["I", 126.90447, 1],
        ["Xe", 131.293, 0],
        ["Cs", 132.90545196, 1],
        ["Ba", 137.327, 2],
        ["La", 138.90547, 3],
        ["Ce", 140.116, 3],
        ["Pr", 140.90766, 3],
        ["Nd", 144.242, 3],
        ["Pm", 145.0, 3],
        ["Sm", 150.36, 3],
        ["Eu", 151.964, 3],
        ["Gd", 157.25, 3],
        ["Tb", 158.92535, 3],
        ["Dy", 162.50, 3],
        ["Ho", 164.93033, 3],
        ["Er", 167.259, 3],
        ["Tm", 168.93422, 3],
        ["Yb", 173.045, 2],
        ["Lu", 174.9668, 3],
        ["Hf", 178.49, 4],
        ["Ta", 180.94788, 5],
        ["W", 183.84, 6],
        ["Re", 186.207, 7],
        ["Os", 190.23, 8],
        ["Ir", 192.217, 6],
        ["Pt", 195.084, 4],
        ["Au", 196.966569, 1],
        ["Hg", 200.592, 2],
        ["Tl", 204.38, 3],
        ["Pb", 207.2, 4],
        ["Bi", 208.98040, 3],
        ["Po", 209.0, 2],
        ["At", 210.0, 1],
        ["Rn", 222.0, 0],
        ["Fr", 223.0, 1],
        ["Ra", 226.0, 2],
        ["Ac", 227.0, 3],
        ["Th", 232.0377, 4],
        ["Pa", 231.03588, 5],
        ["U", 238.02891, 6],
        ["Np", 237.0, 6],
        ["Pu", 244.0, 6],
        ["Am", 243.0, 6],
        ["Cm", 247.0, 3],
        ["Bk", 247.0, 3],
        ["Cf", 251.0, 3],
        ["Es", 252.0, 3],
        ["Fm", 257.0, 3],
        ["Md", 258.0, 2],
        ["No", 259.0, 2],
        ["Lr", 266.0, 3],
        ["Rf", 267.0, 4],
        ["Db", 268.0, 5],
        ["Sg", 269.0, 6],
        ["Bh", 270.0, 7],
        ["Hs", 269.0, 0],
        ["Mt", 278.0, 0],
        ["Ds", 281.0, 0],
        ["Rg", 282.0, 0],
        ["Cn", 285.0, 2],
        ["Nh", 286.0, 0],
        ["Fl", 289.0, 0],
        ["Mc", 289.0, 0],
        ["Lv", 293.0, 0],
        ["Ts", 294.0, 1],
        ["Og", 294.0, 0]
    ]
    HALOGENTS = {9: 'floro', 17: 'chloro', 35: 'bromo', 53: 'iodo', 85: 'astato'}
    FUNCTIONAL_GROUP_PRIORITY = ['ester', 'carboxylic acid', 'aldehyde', 'ketone', 'alcohol', 'ether', 'halide']

    # IUPAC format greek numbers. (SOURCE: Chat GPT).
    ALKANE_STEMS = {
    1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non",
    10: "dec", 11: "undec", 12: "dodec", 13: "tridec", 14: "tetradec", 15: "pentadec", 16: "hexadec", 17: "heptadec", 18: "octadec", 19: "nonadec",
    20: "icos", 21: "methicos", 22: "ethicos", 23: "propicos", 24: "buticos", 25: "penticos", 26: "hexicos", 27: "hepticos", 28: "octicos", 29: "nonicos",
    30: "triacont", 31: "methtriacont", 32: "ethtriacont", 33: "proptriacont", 34: "butriacont", 35: "pentriacont", 36: "hexriacont", 37: "heptriacont", 38: "octriacont", 39: "nontriacont",
    40: "tetracont", 41: "methtetracont", 42: "ethtetracont", 43: "proptetracont", 44: "buttetracont", 45: "penttetracont", 46: "hextetracont", 47: "hepttetracont", 48: "octtetracont", 49: "nontetracont",
    50: "pentacont", 51: "methpentacont", 52: "ethpentacont", 53: "proppentacont", 54: "butpentacont", 55: "pentpentacont", 56: "hexpentacont", 57: "heptpentacont", 58: "octpentacont", 59: "nonpentacont",
    60: "hexacont", 61: "methhexacont", 62: "ethhexacont", 63: "prophexacont", 64: "buthexacont", 65: "penthexacont", 66: "hexhexacont", 67: "hepthexacont", 68: "octhexacont", 69: "nonhexacont",
    70: "heptacont", 71: "methheptacont", 72: "ethheptacont", 73: "propheptacont", 74: "butheptacont", 75: "pentheptacont", 76: "hexheptacont", 77: "heptheptacont", 78: "octheptacont", 79: "nonheptacont",
    80: "octacont", 81: "methoctacont", 82: "ethoctacont", 83: "propoctacont", 84: "butoctacont", 85: "pentoctacont", 86: "hexoctacont", 87: "heptoctacont", 88: "octoctacont", 89: "nonoctacont",
    90: "nonacont", 91: "methnonacont", 92: "ethnonacont", 93: "propnonacont", 94: "butnonacont", 95: "pentnonacont", 96: "hexnonacont", 97: "heptnonacont", 98: "octnonacont", 99: "nonnonacont"
    }
    PRE_NUMBERS = {1: '', 2: 'di', 3: 'tri', 4: 'tetra', 5: 'penta', 6: 'hexa', 7: 'hepta', 8: 'octa', 9: 'nona', 10: 'deca'}

    bond_rects = {}

    ###                                        ###
    ### BEGIN DEFINITION OF CONSTRUCTOR METHOD ###
    ###                                        ###

    def __init__(self, element: int, position: Tuple[int, int] = None, direction: int = None, bonds: dict = None, parent_object: 'Atom' = None) -> None:
        """
        Initialize an atom object.
        
        Arguments
        ---------
        element: The atomic number of the atom's element. For example 6 for Carbon or 1 for Hydrogen.

        position: The Cartesian Coordinate of where to display this atom. Provide in the form of a tuple (x, y). If None, it will be calculated based on direction.
        direction: The angle in degrees representing the direction of the atom from its parent atom. Required if position is None.
        An atom object can either have a position, in which case it is a master atom and the only reference point to all other atoms in the molecule, or it can have a direction, in which case it is a child atom and its position will be calculated based on its parent atom's position and the given direction.

        bonds: The bonds connected to the atom. The number of bonds possible changed based on the atom. For example carbon has the capacity for four bonds. 
        These positions can be filled in a number of different ways. They can be filled with bonds to another atom. In this case the bond position will be a pointer to said atom. If a bond position is filled with a null or None object it is signifying that the previosly mentioned bond in a double of triple bond. Lastly, if the bond position is filled with a function object it is refering to it's parent bond (IE the bond formed with itself and the parent object).
        If the atom is a carbon and is assigned no bonds, it will automatically be assigned four hydrogen atoms.

        The function returns nothing.
        """
        # Error Managment.
        if position == None and direction == None:
            raise Exception('Failed to determine atom position. Neither position or direction from a parent atom were provided. Please provided at least one of the above arguments.')
        

        # Globally Define Attribute Variables.
        self.element = element
        self.element_symbol = Atom.PERIODIC_TABLE[element-1][0]
        self.main_chain = []
        self.hydrogen_visibility = True

        self.position = position
        if direction is not None:
            self.direction = direction % 360
        else:
            self.direction = None
        

        # Figure out if this object is a main Atom (IE it has no parent bond). The result is stored in the attribute IS_MAIN.
        if bonds != None:
            self.IS_MAIN = False
        else:
            self.IS_MAIN = True


        # Globalize the parent object.
        if parent_object == None:
            self.parent_object = self
        else:
            self.parent_object = parent_object


        # Find object's Master Carbon.
        if self.parent_object != self:
            self.master_carbon = self.parent_object.master_carbon
        else:
            self.master_carbon = self


        # Process provided bonds
        if bonds is None:
            bonds = {}
        self.bonds = bonds
        if self.element != 1:
            self.__populate_hydrogens__()


        # If Atom has capacify for multiple bonds create a tracker for multiple bonds at one location.
        if Atom.PERIODIC_TABLE[self.element - 1][2] > 1:
            self.multi_bonds = {}
        
        
        # Calculate position if not given.
        if self.position == None:
            self.__calc_position__()
            
    ###                                    ###
    ### BEGIN DEFINITION OF HELPER METHODS ###
    ###                                    ###

    def __populate_hydrogens__(self) -> None:
        """
        Helper function to populate any available bonds of a carbon atom with hydrogen atoms.
        This function sets the bonds attribute of the atom and takes no arguments.
        """
        # Determine what bond positions are empty.
        available_bonds = []
        if Atom.PERIODIC_TABLE[self.element - 1][2] > len(self.bonds):
            # Make a list of all the possible bond positions dependant on the atom's element.
            available_bonds = list(range(1, Atom.PERIODIC_TABLE[self.element - 1][2] + 1))

            # Iterate through the list of bonds removing any unavailable positions from the list of available bond positions.
            for bond in self.bonds:
                if bond in available_bonds:
                    available_bonds.remove(bond)
                else:
                    available_bonds.remove(len(available_bonds) - 1)
        

        # Assign hydrogen atoms to empty bond positions.
        if available_bonds != []:
            for bond_position in available_bonds:
                self.bonds[bond_position] = Atom(1, direction = 90 * (bond_position - 1), parent_object = self, bonds = {1: self.__object__})
        
    def __calc_position__(self) -> None:
        """
        Helper function to calculate the position of a daughter atom based on its direction and parent atom's position.
        This function sets the position attribute of the atom and takes no arguments.
        """

        # Calculate the x and y offset of the hydrogen based on its direction from its parent carbon.
        if self.element == 1:
            x_offset = Atom.SECONDARY_BOND_LENGTH * cos(radians(self.direction))
            y_offset = Atom.SECONDARY_BOND_LENGTH * sin(radians(self.direction))
        else:
            x_offset = Atom.PRIMARY_BOND_LENGTH * cos(radians(self.direction))
            y_offset = Atom.PRIMARY_BOND_LENGTH * sin(radians(self.direction))

        # Calculate the hydrogen's position.
        self.position = (self.parent_object.position[0] + x_offset, self.parent_object.position[1] + y_offset)

    def __swap_bonds__(self, position1: int, position2: int) -> None:
        """
        Swap the atoms located at two provided bond positions.

        Arguments
        ---------
        position1: The first bond position swap candidate.
        position2: The second bond position swap candidate.
        Order for these arguments is not important.

        Returns nothing.
        """
        # Take a temporary copy of the atom object in bond position 1.
        temp1 = self.bonds[position1]
        # Replace bond position 1 with the contents of bond position 2 and bond position 2 with the temporary copy of the contents of bond position 1.
        self.bonds[position1] = self.bonds[position2]
        self.bonds[position2] = temp1

        # If bond position 1 is a hydrogen set its direction accordingly as well.
        if self.bonds[position1].element == 1:
            self.bonds[position1].direction = (position1 - 1) * 90

        # If bond position 3 is a hydrogen set its direction accordingly as well.
        if self.bonds[position2].element == 1:
            self.bonds[position2].direction = (position2 - 1) * 90

    def __calc_bond_direction__(self) -> float:
        """Calculate the bond direction (angle) between this atom and its parent.

        Returns:
            float: The angle in degrees (0-360) from the parent atom to this atom.
        """
        # Caclulate the pre-reqs for the angle (x, y, & hypotonus).
        x = self.position[0] - self.parent_object.position[0]
        y = self.position[1] - self.parent_object.position[1]
        h = sqrt(x**2 + y**2)

        # Calculate the preliminary angle (-90 -> 90).
        angle = degrees(asin(y/h))

        # Process the preliminary angle to produce an angle in between 0 & 360.
        if self.position[0] < self.parent_object.position[0]:
            angle = 180 - angle
        elif self.position[0] > self.parent_object.position[0] and self.position[1] < self.parent_object.position[1]:
            angle = 360 + angle


        # Return the resultant angle.
        return angle

    def __calc_bond_position__(self, direction: int) -> int:
        """
        Convert a direction in degrees to a bond position (1: right, 2: bottom, 3: left, 4: top).
        direction: The direction in degrees.
        Returns:
            int: The bond position (1: right, 2: bottom, 3: left, 4: top).
        """

        if 315 > direction >= 225:
            return 4 # Top
        elif 135 < direction <= 225:
            return 3 # Left
        elif 45 < direction <= 135:
            return 2 # Bottom
        elif direction >= 315 or direction < 45:
            return 1 # Right
    
    def __reverse_bond_position__(self, bond_position: int) -> int:
        """
        Reverse a bond position (1: right, 2: bottom, 3: left, 4: top) to its opposite position.
        bond_position: The bond position to reverse.
        Returns:
            int: The reversed bond position (1: right, 2: bottom, 3: left, 4: top).
        """

        if bond_position == 1:
            return 3 # Right -> Left
        elif bond_position == 2:
            return 4 # Bottom -> Top
        elif bond_position == 3:
            return 1 # Left -> Right
        elif bond_position == 4:
            return 2 # Top -> Bottom

    def __get_parent_bond_position__(self) -> int:
        """
        Identifies which bond position is linked to a parent atom.
        Takes no arguments but returns the bond position linked to the parent atom.
        """
        # Define the possible bond positions
        bond_positions = list(self.bonds.keys())
        
        # Iterate through the bond positions. Rule out any bonds linked to atoms (C, H, etc.).
        for bond in self.bonds:
            if isinstance(self.bonds[bond], Atom) or self.bonds[bond] is None:
                bond_positions.remove(self.__reverse_bond_position__(bond))
                
        # Return the parent bond position and handle errors is 1 (and only one) bond position is not found.
        if len(bond_positions) > 1:
            raise ValueError('More than one bond position candidates found.')
        elif len(bond_positions) < 1:
            raise ValueError('No valid parent bond positions could be found.')
        else:
            return bond_positions[0]

    def __index__(self, bond_address: list) -> 'Atom':
        """
        Index an atom by its address relative to the master atom.
        address: A list of integers representing the address of the atom to index. Each integer represents a bond position (1: right, 2: bottom, 3: left, 4: top).
        Returns the atom object at the specified address.
        """

        # Ensure that input is in a valid format (i.e. a list of integers).
        if type(bond_address) is not list:
            raise TypeError("Address must be a LIST of integers.")
        if all(isinstance(bond_locant, int) for bond_locant in bond_address) == False:
            raise TypeError("Address must be a list of INTEGERS.")
        
        # Return the atom at the specified address.
        if len(bond_address) < 1:
            return self
        elif len(bond_address) == 1:
            return self.bonds[bond_address[0]]
        else:
            return self.bonds[bond_address[0]].__index__(bond_address[1:])

    def __object__(self) -> 'Atom':
        """
        This function is a way to pass around a parent atom object without confusing it with a bonding atom. It is meant to be passed as an object and when run will return the Atom object it points to.
        
        Takes no arguments.

        Returns
        -------
        - Atom: the Atom object to which it belongs.
        """
        return self
    
    ###                                         ###
    ### BEGIN DEFINITION OF ENTRY-POINT METHODS ###
    ###                                         ###

    def show_hydrogens(self) -> None:
        """Make hydrogen atoms visible when rendering."""
        self.hydrogen_visibility = True

    def hide_hydrogens(self) -> None:
        """Hide hydrogen atoms when rendering."""
        self.hydrogen_visibility = False

    def render(self, screen: pygame.Surface = None) -> None:
        """
        Displays the atom and any daughter atoms on the provided pygame surface.

        Arguments
        ---------
        screen: The pygame Surface on which the atom or atoms will be displayed.

        Returns nothing.
        """
        # Index the element's symbol
        if self in self.master_carbon.main_chain and self.element == 6:
            symbol_texture = Atom.SYMBOLS['CC']
        else:
            symbol_texture = Atom.SYMBOLS[self.element_symbol]

        # If the atom only has the capacity for one bond draw its symbol at its position based on its direction from its parent atom. Then draw its bond line.
        if Atom.PERIODIC_TABLE[self.element - 1][2] == 1:
            # Get parent carbon's center
            c_center_x = self.parent_object.position[0] + Atom.CARBON_SYMBOL.get_width() / 2
            c_center_y = self.parent_object.position[1] + Atom.CARBON_SYMBOL.get_height() / 2
            
            # Calculate bond length and end point
            bond_end_x = c_center_x + Atom.SECONDARY_BOND_LENGTH * cos(radians(self.direction))
            bond_end_y = c_center_y + Atom.SECONDARY_BOND_LENGTH * sin(radians(self.direction))
            
            # Calculate hydrogen symbol position (centered on bond end point)
            symbol_x = bond_end_x - symbol_texture.get_width() / 2
            symbol_y = bond_end_y - symbol_texture.get_height() / 2
            
            # Place symbol
            if self.hydrogen_visibility:
                screen.blit(symbol_texture, (symbol_x, symbol_y))

            # Adjust parameters depending on bond_position.
            bond_position = self.__calc_bond_position__(self.direction)
            if bond_position == 4: # Top
                bond_end_y += symbol_texture.get_height() / 2
                c_center_y -= Atom.CARBON_SYMBOL.get_height() / 2
            elif bond_position == 3: # Left
                bond_end_x += symbol_texture.get_width()
                c_center_x -= Atom.CARBON_SYMBOL.get_width() / 2
            elif bond_position == 2: # Bottom
                bond_end_y -= symbol_texture.get_height() / 2
                c_center_y += Atom.CARBON_SYMBOL.get_height() / 2
            elif bond_position == 1: # Right
                bond_end_x -= symbol_texture.get_width()
                c_center_x += Atom.CARBON_SYMBOL.get_width() / 2

            # Draw the bond line from carbon center to bond end
            if screen is not None and self.hydrogen_visibility:
                pygame.draw.line(screen, 
                                color_scheme.WHITE,
                                (c_center_x, c_center_y),  # Start from carbon center
                                (bond_end_x, bond_end_y),  # End at bond end point
                                2)
            
            # Compute rectangle that covers the bond line between (c_center_x, c_center_y) and (bond_end_x, bond_end_y)
            x = min(c_center_x, bond_end_x)
            y = min(c_center_y, bond_end_y)
            width = abs(c_center_x - bond_end_x)
            height = abs(c_center_y - bond_end_y)

            if width >= height:
                rect = pygame.Rect(x, y - 3, width, max(6, height + 6))
            else:
                rect = pygame.Rect(x - 3, y, max(6, width + 6), height)

            # Log the bond location for hover events.
            Atom.bond_rects[self] = rect


        # If the atom has the capacity for more than one bond draw its symbol at its position. Then draw its children atoms and bond lines.
        else:
            # Place symbol.
            screen.blit(symbol_texture, self.position)

            # Draw all daughter atoms of the carbon.
            for bond in self.bonds:
                # If bond is an Atom, simply draw it.
                if isinstance(self.bonds[bond], Atom):
                    self.bonds[bond].render(screen)
                # If the bond is a method it is indicidative of a bond to a parent atom. Instead of drawing the entire atom on its own just draw the bond lines.
                elif isinstance(self.bonds[bond], method):
                    parent_object = self.bonds[bond]()
                    parent_bond_location = self.__get_parent_bond_position__()
                    
                    # Draw bond line based on parent bond location.
                    if parent_bond_location == 1:
                        carbon_bound = (self.position[0] - symbol_texture.get_width() / 2, self.position[1] + symbol_texture.get_height() / 2)
                        parent_bound = (parent_object.position[0] + symbol_texture.get_width(), parent_object.position[1] + symbol_texture.get_height() / 2)
                    elif parent_bond_location == 2:
                        carbon_bound = (self.position[0] + symbol_texture.get_width() / 2 - 1, self.position[1])
                        parent_bound = (parent_object.position[0] + symbol_texture.get_width() / 2 - 1, parent_object.position[1] + symbol_texture.get_height()) 
                    elif parent_bond_location == 3:
                        carbon_bound = (self.position[0] + symbol_texture.get_width(), self.position[1] + symbol_texture.get_height() / 2)
                        parent_bound = (parent_object.position[0] - 2, parent_object.position[1] + symbol_texture.get_height() / 2)
                    elif parent_bond_location == 4:
                        carbon_bound = (self.position[0] + symbol_texture.get_width() / 2 - 1, self.position[1] + symbol_texture.get_height())
                        parent_bound = (parent_object.position[0] + symbol_texture.get_width() / 2 - 1, parent_object.position[1])
                    
                    # Draw the bond line.
                    if screen is not None:
                        pygame.draw.line(screen, 
                                            color_scheme.WHITE,
                                            carbon_bound,
                                            parent_bound,
                                            2)
                        
                    # Render multiple bonds.
                    if screen is not None and self.__get_parent_bond_position__() in self.parent_object.multi_bonds:
                        # Render double bonds
                        if self.parent_object.multi_bonds[self.__get_parent_bond_position__()] >= 2:
                            carbon_bound_2 = list(carbon_bound)
                            parent_bound_2 = list(parent_bound)

                            diff_y = abs(parent_bound_2[1] - carbon_bound_2[1]) / Atom.PRIMARY_BOND_LENGTH
                            diff_x = abs(parent_bound_2[0] - carbon_bound_2[0]) / Atom.PRIMARY_BOND_LENGTH

                            if parent_bound_2[1] < carbon_bound_2[1] or parent_bound_2[0] < carbon_bound_2[0]:
                                carbon_bound_2[0] += 8 * diff_y - 8 * diff_x
                                carbon_bound_2[1] += 8 * diff_x - 8 * diff_y
                                parent_bound_2[0] += 8 * diff_y + 8 * diff_x
                                parent_bound_2[1] += 8 * diff_x + 8 * diff_y
                            else:
                                carbon_bound_2[0] += 8 * diff_y + 8 * diff_x
                                carbon_bound_2[1] += 8 * diff_x + 8 * diff_y
                                parent_bound_2[0] += 8 * diff_y - 8 * diff_x
                                parent_bound_2[1] += 8 * diff_x - 8 * diff_y

                            pygame.draw.line(screen, 
                                                color_scheme.WHITE,
                                                carbon_bound_2,
                                                parent_bound_2,
                                                1)
                        
                        # Render triple bonds.
                        if self.parent_object.multi_bonds[self.__get_parent_bond_position__()] >= 3:
                            carbon_bound_2 = list(carbon_bound)
                            parent_bound_2 = list(parent_bound)

                            diff_y = abs(parent_bound_2[1] - carbon_bound_2[1]) / Atom.PRIMARY_BOND_LENGTH
                            diff_x = abs(parent_bound_2[0] - carbon_bound_2[0]) / Atom.PRIMARY_BOND_LENGTH

                            if parent_bound_2[1] < carbon_bound_2[1] or parent_bound_2[0] < carbon_bound_2[0]:
                                carbon_bound_2[0] -= 6 * diff_y + 8 * diff_x
                                carbon_bound_2[1] -= 6 * diff_x + 8 * diff_y
                                parent_bound_2[0] -= 6 * diff_y - 8 * diff_x
                                parent_bound_2[1] -= 6 * diff_x - 8 * diff_y
                            else:
                                carbon_bound_2[0] -= 6 * diff_y - 8 * diff_x
                                carbon_bound_2[1] -= 6 * diff_x - 8 * diff_y
                                parent_bound_2[0] -= 6 * diff_y + 8 * diff_x
                                parent_bound_2[1] -= 6 * diff_x + 8 * diff_y

                            pygame.draw.line(screen, 
                                                color_scheme.WHITE,
                                                carbon_bound_2,
                                                parent_bound_2,
                                                1)
                    
                    # Compute rectangle that covers the bond line between parent_bound and carbon_bound
                    px, py = parent_bound
                    cx, cy = carbon_bound

                    x = min(px, cx)
                    y = min(py, cy)
                    width = abs(px - cx)
                    height = abs(py - cy)

                    if width >= height:
                        rect = pygame.Rect(x, y - 3, width, max(6, height + 6))
                    else:
                        rect = pygame.Rect(x - 3, y, max(6, width + 6), height)

                    # Log the bond location for hover events.
                    Atom.bond_rects[self] = rect

    def export_molocule(self, filename: str) -> None:
        """
        This function can be used to export an Atom object and any objects accosiated with it to an external file for re-using.
        
        Arguments
        ---------
        filename: The name and path of the file in which to export the objects.

        Returns nothing
        """
        # Open the file at the specified location.
        with open(filename, 'ab') as file:
            # Produce the pickler and export the object into the file.
            mol_pickler = Pickler(file)
            mol_pickler.dump(self)
            # Dispose of the file object.
            file.close()
    
    def import_molocule(filename: str) -> 'Atom':
        """
        This function can be used to import an Atom object and any objects accosiated with it from an external file.
        
        Arguments
        ---------
        filename: The name and path of the file which contains the Atom objects.

        Returns the Atom object.
        """
        # Open the file at the specified location.
        with open(filename, 'rb') as file:
            # Produce the unpickler and the object contained in the file.
            mol_pickler = Unpickler(file)
            obj = mol_pickler.load()
            # Dispose of the file.
            file.close()

        # Return the object.
        return obj

    def reposition(self, x: int, y: int) -> None:
        """
        This function will change the coordinate position of an atom and anything bonded to it.
        
        Arguments
        ---------
        x: The new x coordinate.
        y: The new y coordinate.

        Returns nothing.
        """
        # Calculate the change in position.
        offset = (x - self.position[0], y - self.position[1])

        # Actually change the atom's position.
        self.position = (x, y)
        self.__calc_bond_direction__()

        # Recalculate and reset bond position definition.
        
        self.direction = self.__calc_bond_direction__()
        new_bond_position = self.__calc_bond_position__(self.direction)
        old_bond_position = list(self.parent_object.bonds.keys())[list(self.parent_object.bonds.values()).index(self)]

        if new_bond_position != old_bond_position and self.element == 6:
            self.parent_object.__swap_bonds__(new_bond_position, old_bond_position)
            self.__swap_bonds__(self.__reverse_bond_position__(new_bond_position), self.__reverse_bond_position__(old_bond_position))

        return new_bond_position

    def distribute_bonds(self) -> None:
        bond_angle = 360 // sum(1 for bond in self.bonds.values() if bond is not None)
        bond_num = 0

        # Adjust bond directions
        for bond in dict(sorted(self.bonds.items())):
            if isinstance(self.bonds[bond], Atom):
                self.bonds[bond].direction = bond_num * bond_angle
            if self.bonds[bond] is not None:
                bond_num += 1


        # Adjust bond positions to match bond directions.
        # Deal with border case: If there are two bond where one is a parent bond.
        new_bonds = {}
        if len(self.bonds) == 2:
            # Re-used variables defined here for read-ability.
            pos1 = list(self.bonds.keys())[0]
            pos2 = list(self.bonds.keys())[1]
            at1 = list(self.bonds.values())[0]
            at2 = list(self.bonds.values())[1]

            # If the two bonds are not already directly opposite each other sort them out.
            if at1 != self.__reverse_bond_position__(at2):
                if isinstance(at1, method):
                    new_bonds[self.__reverse_bond_position__(pos1)] = at2
                    new_bonds[self.__reverse_bond_position__(pos1)].direction = 90 * (self.__reverse_bond_position__(pos1) - 1)
                    new_bonds[pos1] = at1
                else:
                    new_bonds[self.__reverse_bond_position__(pos2)] = at1
                    new_bonds[self.__reverse_bond_position__(pos2)].direction = 90 * (self.__reverse_bond_position__(pos2) - 1)
                    new_bonds[pos2] = at2
        # All other cases.
        else:
            # For each bond set its bond_position to match its direction.
            for bond in self.bonds:
                if isinstance(self.bonds[bond], Atom):
                    new_bond_position = self.__calc_bond_position__(self.bonds[bond].direction)
                    new_bonds[new_bond_position] = self.bonds[bond]
                elif self.bonds[bond] is None:
                    new_bonds[bond] = None
                elif isinstance(self.bonds[bond], method):
                    new_bonds[bond] = self.bonds[bond]

        # Push new bond positions to global.
        self.bonds = new_bonds

    def replace(self, bond_address: list, new_element: int) -> None:
        """
        Replace an existing atom with a new atom at the specified address.
        
        Arguments
        ---------
        bond_address: A list of integers representing the address of the atom to replace. Each integer represents a bond position (1: right, 2: bottom, 3: left, 4: top).
        new_element: The atomic number of the element of the new atom.
        
        Returns Nothing.
        """
        # Ensure that input is in a valid format (i.e. a list of integers).
        if type(bond_address) is not list:
            raise TypeError("Address must be a LIST of integers.")
        if all(isinstance(bond_locant, int) for bond_locant in bond_address) == False:
            raise TypeError("Address must be a list of INTEGERS.")
        if type(new_element) is not int:
            raise TypeError("New element must be an INTEGER.")

        # Identify the parent object.
        parent_bond_address = bond_address[:-1]
        if parent_bond_address == []:
            parent_object = self
        else:
            parent_object = self.__index__(parent_bond_address)
        
        # Attribute the parent object to the newly created Atom object.
        self.__index__(bond_address).parent_object = parent_object

        # Choose bond length based on new element. This will be used to calculate the position of the new atom.
        if new_element == 1:
            bond_length = Atom.SECONDARY_BOND_LENGTH
        else:
            bond_length = Atom.PRIMARY_BOND_LENGTH

        # Calculate new position.
        parent_position = parent_object.position
        direction = self.__index__(bond_address).direction
        x_offset = bond_length * cos(radians(direction))
        y_offset = bond_length * sin(radians(direction))
        new_position = (parent_position[0] + x_offset, parent_position[1] + y_offset)
        self.__index__(bond_address).position = new_position

        # Repalce existing atom with new atom.
        self.__index__(bond_address).element = new_element
        self.__index__(bond_address).element_symbol = Atom.PERIODIC_TABLE[new_element-1][0]
        if Atom.PERIODIC_TABLE[new_element - 1][2] > 1:
            self.__index__(bond_address).bonds = {self.__reverse_bond_position__(bond_address[-1]) % (Atom.PERIODIC_TABLE[self.element - 1][2] + 1): parent_object.__object__}
            self.__index__(bond_address).__populate_hydrogens__()
            self.__index__(bond_address).distribute_bonds()
        
        # Add multi_bonds dict if applicable.
        if Atom.PERIODIC_TABLE[self.__index__(bond_address).element - 1][2] > 1:
            self.__index__(bond_address).multi_bonds = {}
        else:
            self.__index__(bond_address).multi_bonds = None
             
        # !Verify bonds here

    def is_colliding(self, mouse_pos: Tuple[int, int], mode: int) -> list | None:
        """
        When run this function will check if a given mouse position is hovering over the atom or any of its bonding atoms.
        
        Arguments
        ---------
        mouse_pos: A tuple (x, y) representing the position of the mouse.
        mode: This communicates whether this method checks for bonds or atoms. If a 0 is given this method will detect if the point collides with an Atom. If a 1 is provided this method will check if the provided point collides with a bond.

        Returns
        -------
        bond_address: A list representing the address of the bond being hovered over.
        """
        # Fetch the dimensions of the atom based on its element.
        if mode == 0:
            if self.element == 1:
                match self.__calc_bond_position__(self.direction):
                    case 1:
                        atom_rect = pygame.Rect(self.position[0], self.position[1] - 7, Atom.SYMBOLS[self.element_symbol].get_width() + 15, Atom.SYMBOLS[self.element_symbol].get_height() + 15)
                    case 2:
                        atom_rect = pygame.Rect(self.position[0], self.position[1] - 7, Atom.SYMBOLS[self.element_symbol].get_width() + 15, Atom.SYMBOLS[self.element_symbol].get_height() + 15)
                    case 3:
                        atom_rect = pygame.Rect(self.position[0], self.position[1] - 7, Atom.SYMBOLS[self.element_symbol].get_width() + 15, Atom.SYMBOLS[self.element_symbol].get_height() + 15)
                    case 4:
                        atom_rect = pygame.Rect(self.position[0], self.position[1] - 7, Atom.SYMBOLS[self.element_symbol].get_width() + 15, Atom.SYMBOLS[self.element_symbol].get_height() + 15)
            
            else:
                atom_rect = pygame.Rect(self.position[0], self.position[1], Atom.SYMBOLS[self.element_symbol].get_width(), Atom.SYMBOLS[self.element_symbol].get_height())
        elif mode == 1:
            if self.IS_MAIN:
                atom_rect = pygame.Rect(self.position[0], self.position[1], Atom.SYMBOLS[self.element_symbol].get_width(), Atom.SYMBOLS[self.element_symbol].get_height())
            else:
                atom_rect = Atom.bond_rects[self]

        # Calculate if the mouse is hovering over the atom or any of its bonds.
        if collidepoint(atom_rect, mouse_pos):
            return []
        elif Atom.PERIODIC_TABLE[self.element - 1][2] > 1:
            for bond in self.bonds:
                if isinstance(self.bonds[bond], Atom):
                    if isinstance(self.bonds[bond].is_colliding(mouse_pos, mode), list):
                            return [bond] + self.bonds[bond].is_colliding(mouse_pos, mode)
        else:
            return None
 
    def edit_bond(self, bond_address: list, add: bool) -> None:
        """
        This function can be used to add or remove bonds between two atoms.

        Arguments
        ---------
        bond_address: A list of integers representing the address of the bond to modify. Each integer represents a bond position (1: right, 2: bottom, 3: left, 4: top).
        add: A boolean value indicating whether to add (True) or remove (False) a bond.

        Returns nothing.
        """
        # Ensure that a bond address was provided.
        if len(bond_address) == 0:
            raise ValueError('Bond Address cannot be empty.')
        
        # Identify the two atoms involved in the bond modification.
        elif len(bond_address) == 1:
            atom_at_loc = self
            next_atom = self.__index__(bond_address)
        else:
            atom_at_loc = self.__index__(bond_address[:-1])
            next_atom = self.__index__(bond_address)


        # Initialize multi-bond tracking if it does not already exist.
        if bond_address[-1] not in atom_at_loc.multi_bonds:
            atom_at_loc.multi_bonds[bond_address[-1]] = 1


        if add and atom_at_loc.multi_bonds[bond_address[-1]] < 3:
            # Find the hydrogens on each atom.
            atom_at_loc_Hs = []
            for bond in atom_at_loc.bonds.values():
                if isinstance(bond, Atom):
                    if bond.element == 1:
                        atom_at_loc_Hs.append(bond)

            next_atom_Hs = []
            for bond in next_atom.bonds.values():
                if isinstance(bond, Atom):
                    if bond.element == 1:
                        next_atom_Hs.append(bond)

            
            # Ensure that there are hydrogens to remove.
            if atom_at_loc_Hs == [] or next_atom_Hs == []:
                return None
            

            # Choose hydrogens to remove and execute their removal.
            next_value_index = list(next_atom.bonds.values()).index(next_atom_Hs[len(next_atom_Hs) // 2])
            next_remove_key = list(next_atom.bonds.keys())[next_value_index]
            next_atom.bonds[next_remove_key] = None

            aal_value_index = list(atom_at_loc.bonds.values()).index(atom_at_loc_Hs[len(atom_at_loc_Hs) // 2])
            aal_remove_key = list(atom_at_loc.bonds.keys())[aal_value_index]
            atom_at_loc.bonds[aal_remove_key] = None


            # Record the new multi-bond.
            atom_at_loc.multi_bonds[bond_address[-1]] += 1


        elif add is False and atom_at_loc.multi_bonds[bond_address[-1]] > 1:
            # Find the Nones on each atom.
            atom_at_loc_None = None
            for bond in atom_at_loc.bonds:
                if atom_at_loc.bonds[bond] is None:
                    atom_at_loc_None = bond

            next_atom_None = None
            for bond in next_atom.bonds:
                if next_atom.bonds[bond] is None:
                    next_atom_None = bond

            # Ensure that there are Nones to replace.
            if atom_at_loc_None is None or next_atom_None is None:
                return None
            

            # Replace the Nones with hydrogens.
            atom_at_loc_direction = (atom_at_loc_None - 1) * 90
            atom_at_loc.bonds[atom_at_loc_None] = Atom(1, parent_object=atom_at_loc.__object__(), direction = atom_at_loc_direction)

            next_atom_direction = (next_atom_None - 1) * 90
            next_atom.bonds[next_atom_None] = Atom(1, parent_object=next_atom.__object__(), direction = next_atom_direction)


            # Remove the multi-bond.
            atom_at_loc.multi_bonds[bond_address[-1]] -= 1

    def name_side_chains(self, main_chain: 'Alkane') -> tuple[dict[str, list[int]], dict[str, list[int]]]:
        """Analyze the main chain for side chains and functional groups.

        Args:
            main_chain: The main carbon chain as an Alkane object.

        Returns:
            tuple: (prefixes, suffixes) where prefixes/suffixes are dictionaries mapping
                   naming stems to lists of locant positions.
        """
        # Create an empty dictionary to hold side chain locants and stems. Format: {stem: [locant1, locant2, ...], ...}
        prefixes: dict[str, list[int]] = {}
        suffixes: dict[str, list[int]] = {}
        present_FGs = {'ester': [], 'carboxylic acid': [], 'aldehyde': [], 'ketone': [], 'alcohol': [], 'ether': [], 'halide': []}

        # Iterate through each bond of each atom in the main chain to identify side chains.
        for atom in main_chain:
            for bond in atom.bonds.values():
                locant = None
                prefix = None
                suffix = None

                # Skip bonds marked as multi-bonds.
                if bond is None:
                    continue
                # Convert parent bond methods to Atom objects.
                if type(bond) is method:
                    bond = bond()
                
                # Identify Alkyl groups.
                if bond not in main_chain.atom_chain and bond.element == 6:
                    side_chain = main_chain.explore(bond, use_parents = True, exclude=[atom])
                    prefix = Atom.ALKANE_STEMS[len(side_chain)] + 'yl'
                    locant = main_chain.atom_chain.index(atom)

                # Identify any oxygen containing functional group.
                elif bond not in main_chain.atom_chain and bond.element == 8:
                    # Identify the other atom bonding to the oxygen.
                    alt_bonds = list(bond.bonds.values())
                    for alt_bond in alt_bonds:
                        if alt_bond != bond:
                            break

                    main_bonds = atom.bonds.values()
                    carboxylic_acid = False
                    for main_bond in main_bonds:
                        if type(main_bond) is method:
                            main_bond = main_bond()

                        if main_bond in main_chain.atom_chain or main_bond is None:
                            continue
                        elif main_bond.element == 8 and main_bond != bond:
                            bond_pos_one = list(atom.bonds.keys())[list(atom.bonds.values()).index(main_bond)]
                            bond_pos_two = list(atom.bonds.keys())[list(atom.bonds.values()).index(bond)]

                            bond_one = False
                            if bond_pos_one in atom.multi_bonds:
                                if atom.multi_bonds[bond_pos_one] == 2:
                                    bond_one = True
                                                                
                            bond_two = False
                            if bond_pos_two in atom.multi_bonds:
                                if atom.multi_bonds[bond_pos_two] == 2:
                                    bond_two = True

                            if bond_one ^ bond_two:
                                    carboxylic_acid = True
                                    alt_main_bond = None

                                    if bond_one:
                                        for b in bond.bonds:
                                            b = bond.bonds[b]
                                            if type(b) is method:
                                                b = b()
                                            if b is not atom:
                                                alt_main_bond = b
                                    else:
                                        for b in main_bond.bonds:
                                            b = main_bond.bonds[b]
                                            if type(b) is method:
                                                b = b()
                                            if b is not atom:
                                                alt_main_bond = b
                                    
                                    chain_length = 0
                                    if alt_main_bond != None and alt_main_bond != atom:
                                        if alt_main_bond.element != 1:
                                            chain_length = len(main_chain.explore(alt_main_bond, use_parents = True, exclude=[atom, bond, main_bond]))

                                    if chain_length == 0:
                                        suffix = 'oic acid'
                                        locant = main_chain.atom_chain.index(atom)
                                        present_FGs['carboxylic acid'].append(locant)
                                    else:
                                        prefix = Atom.ALKANE_STEMS[chain_length] + 'yl '
                                        suffix = 'oate'
                                        locant = main_chain.atom_chain.index(atom)
                                        present_FGs['ester'].append(locant)
                                    break
                    
                    if carboxylic_acid is False:
                        # Identify Ketones, Aldehydes, and carboxylic acids.
                        if None in alt_bonds:
                            if main_chain.atom_chain.index(atom) == 0 or main_chain.atom_chain.index(atom) == len(main_chain.atom_chain) - 1:
                                # Name Aldehydes
                                locant = main_chain.atom_chain.index(atom)
                                prefix = 'formyl'
                                #suffix = 'al'
                                present_FGs['aldehyde'].append(locant)
                            else:
                                locant = main_chain.atom_chain.index(atom)
                                prefix = 'oxo'
                                #suffix = 'one'
                                present_FGs['ketone'].append(locant)

                        # Identify ethers.
                        elif alt_bond.element == 6:
                            locant = main_chain.atom_chain.index(atom)
                            prefix = len(main_chain.explore(alt_bond, use_parents = True, exclude = [self, atom, bond]))
                            prefix = Atom.ALKANE_STEMS[prefix] + 'oxy'
                            present_FGs['ether'].append(locant)
                        
                        # Identify Alcohols.
                        elif alt_bond.element == 1:
                            locant = main_chain.atom_chain.index(atom)
                            prefix = 'hydroxy'
                            present_FGs['alcohol'].append(locant)
                            #suffix = 'ol'  
                                                            
                # Identify alkyl halides.
                elif bond not in main_chain.atom_chain and bond.element in Atom.HALOGENTS.keys():
                    prefix = Atom.HALOGENTS[bond.element]
                    locant = main_chain.atom_chain.index(atom)
                    present_FGs['halide'].append(locant)

                # If a function group was identified, add it to the prefixes dictionary.
                if locant is not None and prefix is not None:
                    locant += 1
                    if prefix in prefixes:
                        prefixes[prefix].append(locant)
                    else:
                        prefixes[prefix] = [locant]

                # If a function group was identified, add it to the suffixes dictionary.
                if locant is not None and suffix is not None:
                    locant += 1
                    if suffix in suffixes:
                        suffixes[suffix].append(locant)
                    else:
                        suffixes[suffix] = [locant]

        # Return the side chains dictionary.
        return prefixes, suffixes, present_FGs

    def get_position(self, atom, carbonchain) -> list | None:
        """Get the position (locant) of an atom within a carbon chain.

        Args:
            atom: The atom to locate.
            carbonchain: A list of Atom objects representing the main carbon chain.

        Returns:
            list|None: The locant index (1-based) of the atom in the chain, or None.
        """
        if atom is None:
            return None
        if type(atom) is not Atom:
            raise TypeError("Input must be an ATOM object.")

        for carbon in carbonchain:
            for bond in carbon.bonds.values():
                if bond is atom:
                    return carbonchain.index(carbon) + 1

    def identify_functional_groups(self, carbon_chain) -> tuple[list, list]:
        """Identify functional groups in the provided carbon chain.

        Args:
            carbon_chain: A list of Atom objects representing the main carbon chain.

        Returns:
            tuple[list, list]: A pair of lists (prefixes, suffixes) describing functional groups.
        """
        functional_prefixes, functional_suffixes = [], []

        for carbon in carbon_chain:
            for bond in carbon.bonds.values():
                if type(bond) is Atom:
                    if bond.element == 8:
                        if 1 in [a.element for a in bond.bonds.values() if type(a) is Atom]:
                            if True in [True for suf in functional_suffixes if 'ol' in suf]:
                                suf = [s for s in functional_suffixes if 'ol' in s][0]
                                index = functional_suffixes.index(suf)

                                if '-ol' in suf:
                                    functional_suffixes[index] = '-' + suf.split('-')[1] + ',' + str(self.get_position(bond, carbon_chain)) + '-diol'
                                else:
                                    functional_suffixes[index] = '-' + suf.split('-')[1] + ',' + str(self.get_position(bond, carbon_chain)) + '-' + Atom.PRE_NUMBERS[list(Atom.PRE_NUMBERS.keys())[list(Atom.PRE_NUMBERS.values()).index(suf.split('-')[2][:-2])] + 1] + 'ol'

                            else:
                                functional_suffixes.append('-' + str(self.get_position(bond, carbon_chain)) + '-ol')

        return functional_prefixes, functional_suffixes

    def enumerate_locants(self, name: str) -> int:
        """Sum all locant numbers found in an IUPAC name string.

        This helper is used to compare naming options based on locant orders.

        Args:
            name: The name string to analyze (e.g. '2,3-dimethylbutane').

        Returns:
            int: The sum of all locant numbers found in the name.
        """
        nums: list[int] = []
        new_str = ''

        for char in name:
            if char.isalpha() == False and char != ' ':
                new_str += char

        new_str = new_str.replace(',', '-')
        nums = new_str.split('-')
        nums = list(filter(None, nums))
        nums = list(map(int, nums))
        
        return sum(nums)

    def name(self) -> str:
        """Generate the IUPAC name for the current molecule.

        Returns:
            str: The IUPAC name of the molecule.
        """
        # Aquire a list of all Atoms, in order, in the longest or main chain of the hydrocarbon.
        self.master_carbon.main_chain = Alkane(self)
        self.master_carbon.main_chain.find_main_chain()

        # name the molocule in both posible orientations.
        op_one = self.generate_name(self.master_carbon.main_chain)
        op_two = self.generate_name(self.master_carbon.main_chain.reverse(), direction = 1)

        # Determin which orientation produces the lowest sum of locants and return that name as the final name of the molocule.
        if self.enumerate_locants(op_one) < self.enumerate_locants(op_two):
            return op_one
        else:
            return op_two

    def generate_name(self, main_chain: 'Alkane', direction: bool = False) -> str:
        """Generate an IUPAC name for a given main carbon chain.

        Args:
            main_chain: An Alkane object representing the main carbon chain.
            direction: If True, name the chain in reverse direction (used for comparison).

        Returns:
            str: The generated IUPAC name.
        """
        mol_stem = Atom.ALKANE_STEMS[len(main_chain)]

        # Determin suffix
        double_bond_locs = []
        triple_bond_locs = []
        for atom in main_chain:
            atom_loc = main_chain.index(atom)
            for bond in main_chain[atom_loc].multi_bonds:
                if main_chain[atom_loc].bonds[bond] in main_chain:
                    if main_chain[atom_loc].multi_bonds[bond] == 2:
                        double_bond_locs.append(atom_loc + 1 - int(direction))
                    elif main_chain[atom_loc].multi_bonds[bond] == 3:
                        triple_bond_locs.append(atom_loc + 1 - int(direction))


        bond_suffix = None

        if double_bond_locs != []:
            bond_suffix = '-' + str(double_bond_locs)[1:-1].replace(' ', '') + '-' + Atom.PRE_NUMBERS[len(double_bond_locs)] + 'ene'

        if triple_bond_locs != [] and double_bond_locs != []:
            bond_suffix = bond_suffix[:-1] + '-' + str(triple_bond_locs)[1:-1].replace(' ', '') + '-' + Atom.PRE_NUMBERS[len(triple_bond_locs)] + 'yne'
        elif triple_bond_locs != [] and double_bond_locs == []:
            bond_suffix = '-' + str(triple_bond_locs)[1:-1].replace(' ', '') + '-' + Atom.PRE_NUMBERS[len(triple_bond_locs)] + 'yne'
        
        if bond_suffix == None:
            bond_suffix = 'ane'
        

        # Name any branching chains.
        prefixes, suffixes, present_FGs = self.name_side_chains(main_chain)
        prefixes = dict(sorted(prefixes.items()))

        # Determine if this direction is the correct one based on the priority list.
        median = float(len(main_chain)) / 2.
        for fg in Atom.FUNCTIONAL_GROUP_PRIORITY:
            locants = present_FGs[fg]
            if locants != []:
                for locant_pos in range(len(locants)):
                    locants[locant_pos] = locants[locant_pos] - median
                balance = sum(locants)
                if balance == 0:
                    continue
                elif balance > 0:
                    return '999999999999999'
                if balance != 0:
                    break


        prefix_names = ''
        for stem in prefixes:
            if prefix_names != '':
                prefix_names += '-'

            locants = str(prefixes[stem])[1::].replace(' ', '').replace(']', '')
            count = Atom.PRE_NUMBERS[len(prefixes[stem])]

            if stem[-1] == ' ':
                prefix_names = stem + prefix_names
            else:
                prefix_names += locants + '-' + count + stem

        suffix_names = ''
        for stem in suffixes:
            if suffix_names != '':
                suffix_names += '-'

            locants = str(suffixes[stem])[1::].replace(' ', '').replace(']', '')
            count = Atom.PRE_NUMBERS[len(suffixes[stem])]

            if stem == 'oic acid' or stem == 'oate':
                suffix_names += stem
            else:
                suffix_names += locants + '-' + count + stem
        
        return prefix_names + mol_stem + bond_suffix + suffix_names
    
class Alkane:
    """
    This class represents a chain of carbon atoms. It is a collection of Atom objects linked together in a list with their object references. This class brings Atoms together to allow a more seemless usage in code by providing a few helper functions.
    """

    def __init__(self, main_carbon: Atom, atom_chain: list['Atom'] = []) -> None:
        """
        Initialize an Alkane object.
        
        Arguments
        ---------
        atom_chain: A list of Atom objects representing the carbon chain of the alkane.
        
        Returns Nothing.
        """
        self.atom_chain = atom_chain
        self.main_carbon = main_carbon

    def explore(self, carbon: 'Atom | method', use_parents: bool = True, exclude: list['Atom'] = []) -> list['Atom']:
        """
        Recursively explores a carbon atom graph to find the longest continuous
        chain of bonded carbon atoms starting from a given atom.

        Parameters
        ----------
        carbon : Atom or callable
            A carbon atom object, or a callable that returns a carbon atom
            (used to resolve parent bonds when `use_parents` is True).

        use_parents : bool, optional
            If True, callable bond references are resolved by calling them.
            If False, callable references are ignored. Default is True.

        exclude : list of Atom, optional
            A list of atom objects that should not be revisited during traversal.
            This is typically used to prevent backtracking in a specific direction.

        Returns
        -------
        list[Atom]
            An ordered list of atom pointers representing the longest continuous
            carbon chain reachable from the starting atom. The starting carbon
            is included as the first element of the list.
        """
        # Resolve callable carbon reference if parent traversal is allowed
        if type(carbon) is method and use_parents:
            carbon = carbon()
        elif type(carbon) is method and use_parents == False:
            return []
        
        # Stop recursion if the atom is not carbon
        if carbon is None:
            return []
        if carbon.element != 6:
            return []
        
        # Track the longest chain found from this atom
        longest_chain = []

        # Iterate over all bond positions on the carbon atom
        for bond in carbon.bonds:
            bnd = carbon.bonds[bond]
            
            # Only consider valid atom objects that are not excluded
            if bnd not in exclude and isinstance(bnd, Atom):
                # Recursively explore the bonded atom and prepend the current carbon
                chain = [carbon] + self.explore(
                    bnd, 
                    use_parents = use_parents, 
                    exclude = exclude
                )
                # Keep the longest chain found
                if len(chain) > len(longest_chain):
                    longest_chain = chain

        # Return the longest carbon chain originating from this atom
        return longest_chain

    def find_primary_chain(self, carbon) -> None:
        """
        Utalizes the single provided datapoint, self.main_carbon to find the four branches of the main carbon.
        Takes no parameters, just uses, the already defined, self.main_carbon attribute.
        
        Returns
        -------
        primary_chains: The four branches from the main carbon.
        """
        primary_chains = {}

        # Iterate through the four chains bonded to the main carbon and identy the longest path each one can take.
        for bond in carbon.bonds:
            primary_chains[bond] = self.explore(carbon.bonds[bond])

        longest = []
        second_longest = []
        # Iterate through the primary chains and choose the longest and second longest chain.
        for bond in primary_chains:
            # Qualify this chain option for the longest of the primary chains
            if len(primary_chains[bond]) > len(longest):
                longest = primary_chains[bond]

            # Qualify this chain option for the second longest of the primary chains
            if len(primary_chains[bond]) > len(second_longest) and primary_chains[bond] != longest and len(primary_chains[bond]) <= len(longest):
                l = True
                for a in longest:
                    if a in primary_chains[bond]:
                        l = False
                if l == True:
                    second_longest = primary_chains[bond]
                

        # Reverse the second longest chain.
        second_longest.reverse()

        # return the full primary chain
        if carbon in longest:
            return second_longest + longest[longest.index(carbon)::]
        else:
            return second_longest + [carbon] + longest

    def find_main_chain(self) -> None:
        """Determine and store the longest carbon chain for this alkane.

        The longest chain is stored in `self.atom_chain`.
        """
        primary_chains = {self.main_carbon: self.find_primary_chain(self.main_carbon)}

        for atom in primary_chains[self.main_carbon]:
            primary_chains[atom] = self.find_primary_chain(atom)
        
        self.atom_chain = max(list(primary_chains.values()), key=len)

    def __len__(self) -> int:
        """
        Returns the length of the alkane's carbon chain.
        Takes no arguments.
        Returns an integer representing the number of carbon atoms in the alkane's carbon chain.
        """
        return len(self.atom_chain)
    
    def __iter__(self):
        """Return an iterator over the alkane's carbon chain."""
        return iter(self.atom_chain)

    def __getitem__(self, position: int) -> Atom:
        """
        Index an atom in the alkane's carbon chain by its position.
        
        Arguments
        ---------
        position: An integer representing the position of the atom in the carbon chain (1-indexed).
        
        Returns
        -------
        - Atom: the Atom object at the specified position.
        """
        return self.atom_chain[position]

    def reverse(self) -> 'Alkane':
        """Return a new Alkane with the carbon chain reversed."""
        rev = Alkane(self.main_carbon, self.atom_chain[::-1])
        return rev

    def index(self, atom: Atom) -> int:
        """
        Find the position of an atom in the alkane's carbon chain.
        
        Arguments
        ---------
        atom: An Atom object representing the atom to find.
        
        Returns
        -------
        - int: the position of the atom in the carbon chain (1-indexed).
        """
        return self.atom_chain.index(atom)

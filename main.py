# Author: Ilan Weinberger
# Date: September 06 2025
# Description: Main entrypoint for the IUPAC Alkane Namer application. Initializes pygame, constructs pages, and starts the main application window.


# Import used classes & libraries.
from Window_Classes import window, page
import pygame

# Import page information.
from Molecule_Display import Molecule_Display_definitions, Molecule_Display_page, Molecule_Display_event_handler
from Main_Page import Main_Page_definitions, Main_Page_page, Main_Page_event_handler
from Imports_Page import Imports_definitions, Imports_page, Imports_event_handler

# Initial Pygame.
pygame.init()
pygame.font.init()

# Compile each page
Main_Page = page(Main_Page_definitions, Main_Page_page, Main_Page_event_handler)
Molecule_Display_page = page(Molecule_Display_definitions, Molecule_Display_page, Molecule_Display_event_handler)
Imports_page = page(Imports_definitions, Imports_page, Imports_event_handler)

# Load icon.
icon = pygame.image.load('img/icon.png')
# Init main pong window.
pw = window(
    icon, 
    "IUPACane", 
    [Main_Page, Molecule_Display_page, Imports_page], 
    is_resizable=True
    )
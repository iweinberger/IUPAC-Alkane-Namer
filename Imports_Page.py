# Author: Ilan Weinberger
# Date: September 06 2025
# Description: Page for importing saved molecule files. This page lists available saved molecule files and lets the user load them.


# Import used classes & libraries.
import pygame
import colors as color_scheme
from Window_Classes import button
from Alkane_Classes import Atom
from os import listdir

def Imports_definitions(window):
    """Initialize the imports page and prepare the list of saved molecules.

    Args:
        window: The window instance to attach UI objects to.
    """
    # Define fonts.
    window.title1_font = pygame.font.Font('fonts/Orbitron_Bold.ttf', 50)
    window.title2_font = pygame.font.Font('fonts/Orbitron_Bold.ttf', 25)
    window.menu_button_font = pygame.font.Font('fonts/Orbitron.ttf', 16)
    window.menu_symbol_font = pygame.font.Font('fonts/FontAwesome.otf', 16)
    window.sign_button_font = pygame.font.Font('fonts/FontAwesome.otf', 17)
    window.sign_button_font_small = pygame.font.Font('fonts/FontAwesome.otf', 15)

    # Button definitions.
    window.home_button = button(
        window.screen,
        pygame.Rect((window.window_dimentions[0] - 50, window.title_bar_height * 2, 25, 25)),
        'home',
        window.sign_button_font_small,
        color_scheme.WHITE,
        color_scheme.WHITE
    )

    # Get file list.
    window.import_buttons = []
    top = window.title_bar_height + 50

    with open('./outside_saves.txt') as imports_list:
        imports_list_str = imports_list.read()
    imports_list = imports_list_str.split('\n')

    for file in listdir('./saves/') + imports_list:
        window.import_buttons.append(button(
            window.screen,
            pygame.Rect((window.window_dimentions[0] / 10, top, window.window_dimentions[0] * 8 / 10, 50)),
            file.split('\\')[-1],
            window.title2_font,
            color_scheme.GREEN,
            color_scheme.WHITE
        ))
        prefix = '' if 'C:\\' in file else './saves/'
        window.import_buttons[-1].path = f'{prefix}{file}'
        top += 60

def Imports_page(screen, window):
    """Render the imports page each frame.

    Args:
        screen: The pygame surface to draw on.
        window: The window instance containing UI objects.
    """
    # Reset screen background color.
    window.screen.fill(color_scheme.BG_BLUE)

    # Draw content.
    window.home_button.draw(border_width=2, border_width_hover=3)
    for button in window.import_buttons:
        button.draw(border_width=2, border_width_hover=3)

def Imports_event_handler(window, e, key):
    """Handle input events for the imports page.

    Args:
        window: The window instance for this page.
        e: The pygame event to handle.
        key: The current keyboard state.
    """
    if window.home_button.on_click(e):
        window.page = 0
    
    for button in window.import_buttons:
        if button.on_click(e):
            import_file = button.path
            window.master_carbon = Atom.import_molocule(import_file)
            window.page = 1
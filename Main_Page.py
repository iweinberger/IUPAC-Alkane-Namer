# Author: Ilan Weinberger
# Date: September 06 2025
# Description:Main menu page for the IUPAC Alkane Namer application. Defines the UI elements for the main page and handles layout.


# Import used classes & libraries.
import pygame
import colors as color_scheme
from Window_Classes import button
from Alkane_Classes import Atom
from typing import Any

def Main_Page_definitions(window: Any) -> None:
    """Initialize the main menu page UI elements.

    Args:
        window: The window instance to attach UI objects to.
    """
    # Define fonts.
    window.title1_font = pygame.font.Font('fonts/Orbitron_Bold.ttf', 50)
    window.title2_font = pygame.font.Font('fonts/Orbitron_Bold.ttf', 25)
    window.menu_button_font = pygame.font.Font('fonts/Orbitron.ttf', 16)
    window.menu_symbol_font = pygame.font.Font('fonts/FontAwesome.otf', 16)

    # Define text and buttons.
    window.title1 = window.title1_font.render("IUPAC", True, color_scheme.GREEN)
    window.title2 = window.title2_font.render(" Namer", True, color_scheme.WHITE)
    window.title2 = pygame.transform.rotate(window.title2, -10)

    window.build_button = button(
        window.screen, 
        pygame.Rect((window.window_dimentions[0] / 2 - 100, window.window_dimentions[1] * 3 / 8, 200, 40)), 
        'Molocule Builder', 
        window.menu_button_font,
        color_scheme.WHITE,
        color_scheme.WHITE
    )
    window.lessons_button = button(
        window.screen, 
        pygame.Rect((window.window_dimentions[0] / 2 - 100, window.window_dimentions[1] / 2, 200, 40)), 
        'Lessons', 
        window.menu_button_font,
        color_scheme.WHITE,
        color_scheme.WHITE
    )
    window.imports_button = button(
        window.screen, 
        pygame.Rect((window.window_dimentions[0] / 2 - 100, window.window_dimentions[1] * 5 / 8, 90, 40)), 
        'download', 
        window.menu_symbol_font,
        color_scheme.GREEN,
        color_scheme.GREEN
    )
    window.settings_button = button(
        window.screen, 
        pygame.Rect((window.window_dimentions[0] / 2 + 10, window.window_dimentions[1] * 5 / 8, 90, 40)), 
        'cog', 
        window.menu_symbol_font,
        color_scheme.GREEN,
        color_scheme.GREEN
    )

def Main_Page_page(screen: pygame.Surface, window: Any) -> None:
    """Render the main menu page each frame.

    Args:
        screen: The pygame surface to draw on.
        window: The window instance containing UI objects.
    """
    # Reset screen background color.
    window.screen.fill(color_scheme.BG_BLUE)

    # Draw the title on the screen.
    window.screen.blit(window.title1, 
                       (
                           (window.window_dimentions[0] / 2) - ((window.title1.get_width() + window.title2.get_width()) / 2), 
                           window.window_dimentions[1] * 3 / 16
                           )
                        )
    window.screen.blit(window.title2, 
                       (
                           (window.window_dimentions[0] / 2) - ((window.title1.get_width() + window.title2.get_width()) / 2) + window.title1.get_width(), 
                           (window.window_dimentions[1] * 3 / 16) + (window.title1.get_height() * 3 / 8)
                           )
                        )
    
    # Draw button on screen.
    window.build_button.draw(border_width=2, border_width_hover=3)
    window.lessons_button.draw(border_width=2, border_width_hover=3)
    window.imports_button.draw(border_width=2, border_width_hover=3)
    window.settings_button.draw(border_width=2, border_width_hover=3)

def Main_Page_event_handler(window: Any, e: pygame.event.Event, key: Any) -> None:
    """Handle input events for the main menu.

    Args:
        window: The window instance for this page.
        e: The pygame event to handle.
        key: The current keyboard state.
    """
    if window.build_button.on_click(e):
        window.master_carbon = None
        window.page = 1

    if window.imports_button.on_click(e):
        window.page = 2
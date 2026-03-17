# Authoer: Ilan Weinberger
# Date: June 06 2025
# Description: Modal window used to confirm whether the user wants to save before closing. This script is intended to be run as a separate process that communicates with the main application via the file `configs/save_window_communication.txt`.


from Window_Classes import page, window, button
import pygame
from pygame._sdl2 import Window
import colors as color_scheme

# Initiate Pygame
pygame.init()

def close_definitions(window):
    """Initialize the confirmation window.

    This function sets up the UI elements for the save confirmation dialog and
    writes the initial status into the communication file.

    Args:
        window: The window instance being initialized.
    """
    # Ensure that window begins in focus.
    Window.from_display_module().focus()

    # Open communication channel.
    with open('configs/save_window_communication.txt', 'w') as f:
        f.write('1')

    # Define fonts and text objects for later attachment to the screen.
    window.q_font = pygame.font.Font('fonts/Orbitron.ttf', 20)
    window.q_text1 = window.q_font.render('Are you sure you want to exit', True, color_scheme.WHITE)
    window.q_text2 = window.q_font.render('settings page without saving?', True, color_scheme.WHITE)

    # Define YES & NO button objects for later display on screen.
    window.yes_button = button(
        window.screen,
        pygame.Rect((window.window_dimentions[0] / 3 - 50, window.title_bar_height * 3 + window.q_text1.get_height() + window.q_text2.get_height(), 100, 40)),
        'YES',
        window.q_font,
        color_scheme.WHITE,
        color_scheme.RED
    )

    window.no_button = button(
        window.screen,
        pygame.Rect((window.window_dimentions[0] * 2 / 3 - 50, window.title_bar_height * 3 + window.q_text1.get_height() + window.q_text2.get_height(), 100, 40)),
        'NO',
        window.q_font,
        color_scheme.WHITE,
        color_scheme.BLUE
    )

def close_page(screen, window):
    """Render the save confirmation UI.

    This function draws the prompt text and the YES/NO buttons.

    Args:
        screen: The pygame surface to draw onto.
        window: The window instance containing UI elements.
    """
    # Display title text on screen.
    screen.blit(window.q_text1, [(window.window_dimentions[0] / 2) - (window.q_text1.get_width() / 2), window.title_bar_height * 2])
    screen.blit(window.q_text2, [(window.window_dimentions[0] / 2) - (window.q_text2.get_width() / 2), window.title_bar_height * 2 + window.q_text1.get_height()])

    # Display YES and NO buttons on screen.
    window.yes_button.draw()
    window.no_button.draw()

def close_event_handler(window, e, key):
    """Handle input events for the save confirmation dialog.

    Updates the shared communication file based on the user selection and closes the
    confirmation window as appropriate.

    Args:
        window: The window instance for this dialog.
        e: The pygame event being handled.
        key: The current pressed key state (unused).
    """
    # If the YES button is pressed communicate with parent window and close this window.
    if window.yes_button.on_click(e):
        # Update communication.
        with open('configs/save_window_communication.txt', 'w') as f:
            f.write('2')
        # Close window.
        window.in_game = False
    
    # Handle out of focus events. (Close the window if it leaves focus and update communication)
    if e.type == pygame.ACTIVEEVENT:
        if e.state == 2 and not e.gain:
            # Update communication.
            with open('configs/save_window_communication.txt', 'w') as f:
                f.write('0')
            # Close window.
            window.in_game = False
    
    # If the NO button is pressed close the window and update communication.
    if window.no_button.on_click(e):
        # Update communication.
        with open('configs/save_window_communication.txt', 'w') as f:
            f.write('0')
        # Close window.
        window.in_game = False

# Load window icon.
icon = pygame.image.load('img/icon.png')
# Organize page functions in a way which can be handed to the window.
close = page(close_definitions, close_page, close_event_handler)
# Initialize the window with.
close_window = window(
    icon, 
    "Save?", 
    [close], 
    is_resizable=False, 
    hide_maximize=True, 
    hide_minimize=True, 
    window_dimentions=[400, 200]
    )
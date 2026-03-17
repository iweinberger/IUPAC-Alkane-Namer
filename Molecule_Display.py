# Author: Ilan Weinberger
# Date: September 06 2025
# Description: Displays, edits, and exports molecular structures. This module implements the main molecule editing page including rendering, user input handling, and saving/loading interactions.

# Import used classes & libraries.
import pygame
import colors as color_scheme
from Window_Classes import button
from Alkane_Classes import Atom
import time
from subprocess import Popen
from time import sleep
from typing import Any

def Molecule_Display_definitions(window: Any) -> None:
    """Initialize the molecule display page state and UI controls.

    Args:
        window: The main window object to attach state and widgets to.
    """
    # Define global tracking variables.
    try:
        window.master_carbon
    except:
        window.master_carbon = None
    window.mode = 1
    window.activity = 0
    window.drag_address = None
    window.saved = True
    window.close_prompt_status_tracker = False

    window.halogens = ['X', 'F', 'Cl', 'Br', 'I', 'At']
    window.halogen_atomic_number = {
        'F': 9,
        'Cl': 17,
        'Br': 35,
        'I': 53,
        'At': 85
    }

    # Reset Tracking Files.
    window.loading = 0
    window.next_loading = 0
    with open('configs/save_window_communication.txt', 'w') as file:
        file.write('1')

    # Define page fonts.
    window.title_font = pygame.font.Font('fonts/Orbitron_Bold.ttf', 12)
    window.button_font = pygame.font.Font('fonts/Orbitron.ttf', 10)
    window.name_font = pygame.font.Font('fonts/Orbitron_Bold.ttf', 10)
    window.sign_button_font = pygame.font.Font('fonts/FontAwesome.otf', 17)
    window.sign_button_font_small = pygame.font.Font('fonts/FontAwesome.otf', 15)

    # Define editing menu title & border.
    window.editing_menu_title = window.title_font.render('Editing Menu', True, color_scheme.WHITE)

    # Define editing menu buttons.
    window.carbon_button = button(
        window.screen,
        pygame.Rect((window.title_bar_height * 0.5, window.title_bar_height * 2, 25, 25)),
        'C',
        window.button_font,
        color_scheme.WHITE,
        color_scheme.GREEN
    )
    window.bond_button = button(
        window.screen,
        pygame.Rect((window.title_bar_height * 0.5 + 30, window.title_bar_height * 2, 55, 25)),
        'Bonds',
        window.button_font,
        color_scheme.WHITE,
        color_scheme.GREEN
    )
    window.alcohol_button = button(
        window.screen,
        pygame.Rect((window.title_bar_height * 0.5 + 90, window.title_bar_height * 2, 30, 25)),
        'OH',
        window.button_font,
        color_scheme.WHITE,
        color_scheme.GREEN
    )
    window.halogen_button = button(
        window.screen,
        pygame.Rect((window.title_bar_height * 0.5 + 125, window.title_bar_height * 2, 25, 25)),
        'X',
        window.button_font,
        color_scheme.WHITE,
        color_scheme.GREEN
    )
    window.mode_button = button(
        window.screen,
        pygame.Rect((window.title_bar_height * 0.5 + 155, window.title_bar_height * 2, 25, 25)),
        '+',
        window.sign_button_font,
        color_scheme.WHITE,
        color_scheme.RED
    )
    window.name_button = button(
        window.screen,
        pygame.Rect((window.window_dimentions[0] - 110, window.title_bar_height * 2, 100, 25)),
        'Name',
        window.sign_button_font,
        color_scheme.WHITE,
        color_scheme.WHITE
    )
    window.export_button = button(
        window.screen,
        pygame.Rect((window.window_dimentions[0] - 140, window.title_bar_height * 2, 25, 25)),
        'upload',
        window.sign_button_font,
        color_scheme.WHITE,
        color_scheme.WHITE
    )
    window.home_button = button(
        window.screen,
        pygame.Rect((window.window_dimentions[0] - 170, window.title_bar_height * 2, 25, 25)),
        'home',
        window.sign_button_font_small,
        color_scheme.WHITE,
        color_scheme.WHITE
    )

    # Define name display variables.
    window.name_text = ''
    window.name_obj = window.name_font.render(window.name_text, True, color_scheme.WHITE)

def Molecule_Display_page(screen, window):
    """Render the molecule editor page each frame.

    Args:
        screen: The pygame surface to draw on.
        window: The main window object containing state and widgets.
    """
    # Reset screen background color.
    window.screen.fill(color_scheme.BG_BLUE)

    # Draw editing menu buttons, title, & border.
    window.screen.blit(window.editing_menu_title, (window.title_bar_height * 0.5, window.title_bar_height * 1.25))
    window.carbon_button.draw(border_width=2, border_width_hover=3)
    window.bond_button.draw(border_width=2, border_width_hover=3)
    window.alcohol_button.draw(border_width=2, border_width_hover=3)
    window.halogen_button.draw(border_width=2, border_width_hover=3)
    window.mode_button.draw(border_width=2, border_width_hover=3)
    window.name_button.draw(border_width=2, border_width_hover=3)
    window.export_button.draw(border_width=2, border_width_hover=3)
    window.home_button.draw(border_width=2, border_width_hover=3)

    # Draw molecule data.
    if window.master_carbon != None:
        window.master_carbon.render(screen)

    # Slowly ease into the progress percentage.
    if window.loading != window.next_loading:
        if window.loading < window.next_loading:
            window.loading += 1
        else:
            window.loading -= 1
        sleep(10)

    # Draw save window progress bar.
    if window.loading > 0:
        pygame.draw.rect(window.screen, color_scheme.GREEN, (window.window_dimentions[0] // 2 - 100, window.window_dimentions[1] // 2 - 10, window.loading, 20))

    # Draw name of the molecule.
    window.screen.blit(window.name_obj, (10, window.window_dimentions[1] - window.name_obj.get_height() - 10))

def Molecule_Display_event_handler(window, e, key):
    """Handle user input events on the molecule editor page.

    Args:
        window: The main window object containing state and widgets.
        e: The pygame event to handle.
        key: The current keyboard state.
    """
    # Returning to home page.
    if window.home_button.on_click(e):
        if window.saved:
            window.page = 0
        else:
            Popen(['close_window.exe'])
            window.close_prompt_status_tracker = True

    if window.close_prompt_status_tracker:
        with open('configs/save_window_communication.txt', 'r+') as tracking_file:
            code = tracking_file.read()
            if code == '0':
                window.close_prompt_status_tracker = False
            elif code == '2':
                window.page = 0
                tracking_file.write('0')

    # Onclick on mode button alternate through each mode.
    if window.mode_button.on_click(e):
        # Alternate through each mode.
        window.mode = (window.mode + 1) % 3
        
        # Update button symbol.
        if window.mode == 0:
            window.mode_button.change_text('-')
        elif window.mode == 1:
            window.mode_button.change_text('+')
        elif window.mode == 2:
            window.mode_button.change_text('↔')

    # Onclick on carbon button set activity to carbon placement.
    elif window.carbon_button.on_click(e):
        window.activity = 1
        window.carbon_button.overide_hover(True)
        window.bond_button.overide_hover(False)
        window.alcohol_button.overide_hover(False)
        window.halogen_button.overide_hover(False)   
    # Onclick on bond button set activity to carbon placement.
    elif window.bond_button.on_click(e):
        window.activity = 2
        window.carbon_button.overide_hover(False)
        window.bond_button.overide_hover(True)
        window.alcohol_button.overide_hover(False)
        window.halogen_button.overide_hover(False)   
    # Onclick on alcohol button set activity to carbon placement.
    elif window.alcohol_button.on_click(e):
        window.activity = 3
        window.carbon_button.overide_hover(False)
        window.bond_button.overide_hover(False)
        window.alcohol_button.overide_hover(True)
        window.halogen_button.overide_hover(False)   
    # Onclick on halogen button set activity to carbon placement.
    elif window.halogen_button.on_click(e):
        window.activity = 4

        window.carbon_button.overide_hover(False)
        window.bond_button.overide_hover(False)
        window.alcohol_button.overide_hover(False)
        window.halogen_button.overide_hover(True) 

        # Cycle through the halogen options.
        if window.halogen_button.text == 'At':
            next_halogen = window.halogens[1]
        else:
            next_halogen = window.halogens[window.halogens.index(window.halogen_button.text) + 1]
        window.halogen_button.change_text(next_halogen)
    
    # Ensure halogen button text is reset if activity is not halogen placement.
    if window.activity != 4 and window.halogen_button.text != 'X':
        window.halogen_button.change_text('X')

    # Handle mouse button down events.
    if e.type == pygame.MOUSEBUTTONDOWN:
        # Do not react to clicks within the editing menu area.
        if (e.pos[0] > window.mode_button.rect.right + 10 or e.pos[1] > window.title_bar_height * 3) and e.pos[1] > window.title_bar_height:
            # If activity is carbon placement place, remove, or drag a carbon atom.
            if window.activity == 1:
                # Any change means the molecule is not in a saved state.
                window.saved = False

                if window.mode == 1:
                    # Add/replace a carbon atom at the clicked location.
                    if window.master_carbon is None:
                        window.master_carbon = Atom(6, position=e.pos)
                    else:
                        is_colliding = window.master_carbon.is_colliding(e.pos, 0)
                        if is_colliding:
                            window.master_carbon.replace(is_colliding, 6)

                elif window.mode == 0:
                    # Delete a carbon atom / replace it with hydrogen.
                    if window.master_carbon is not None:
                        is_colliding = window.master_carbon.is_colliding(e.pos, 0)
                        if is_colliding == []:
                            window.master_carbon = None
                        elif is_colliding:
                            window.master_carbon.replace(is_colliding, 1)

                elif window.mode == 2:
                    # Drag mode: allow moving existing non-hydrogen atoms.
                    if window.drag_address is None:
                        window.drag_address = window.master_carbon.is_colliding(e.pos, 0)
                        if window.drag_address is not None:
                            window.drag_atom = window.master_carbon.__index__(window.drag_address)
                            if window.drag_atom.element != 1:
                                window.drag_offset = (window.drag_atom.position[0] - e.pos[0], window.drag_atom.position[1] - e.pos[1])
                            else:
                                window.drag_address = None
                    else:
                        # End dragging when mouse is pressed again.
                        window.drag_address = None

            # If activity is bond placement edit bonds.
            elif window.activity == 2:
                # If any alteration is made record that the latest molocule has not been saved.
                window.saved = False
                
                if window.mode == 1 and window.master_carbon == None:
                    window.master_carbon = Atom(6, position=e.pos)
                elif window.mode == 1 and window.master_carbon != None:
                    is_colliding = window.master_carbon.is_colliding(e.pos, 1)
                    if is_colliding != None and is_colliding != []:
                        window.master_carbon.edit_bond(is_colliding, True)
                elif window.mode == 0 and window.master_carbon != None:
                    is_colliding = window.master_carbon.is_colliding(e.pos, 1)
                    if is_colliding != None and is_colliding != []:
                        window.master_carbon.edit_bond(is_colliding, False)

            # If activity is hydroxide placement place hydroxide.
            elif window.activity == 3:
                # If any alteration is made record that the latest molocule has not been saved.
                window.saved = False
                
                if window.mode == 1 and window.master_carbon != None:
                    is_colliding = window.master_carbon.is_colliding(e.pos, 0)
                    if is_colliding != None and is_colliding != []:
                        window.master_carbon.replace(is_colliding, 8)
                elif window.mode == 0 and window.master_carbon != None:
                    is_colliding = window.master_carbon.is_colliding(e.pos, 0)
                    if is_colliding == []:
                        window.master_carbon = None
                    elif is_colliding != None:
                        window.master_carbon.replace(is_colliding, 1)

            # If activity is halogen placement place halogen.
            elif window.activity == 4:
                # If any alteration is made record that the latest molocule has not been saved.
                window.saved = False
            
                if window.mode == 1 and window.master_carbon != None:
                    is_colliding = window.master_carbon.is_colliding(e.pos, 0)
                    if is_colliding != None and is_colliding != []:
                        window.master_carbon.replace(is_colliding, window.halogen_atomic_number[window.halogen_button.text])
                elif window.mode == 0 and window.master_carbon != None:
                    is_colliding = window.master_carbon.is_colliding(e.pos, 0)
                    if is_colliding == []:
                        window.master_carbon = None
                    elif is_colliding != None:
                        window.master_carbon.replace(is_colliding, 1)

        if window.mode != 2:
            time.sleep(0.2)

    if window.drag_address != False and window.drag_address != None:
        try:
            window.drag_address[-1] = window.master_carbon.__index__(window.drag_address).reposition(e.pos[0] + window.drag_offset[0], e.pos[1] + window.drag_offset[1])
        except AttributeError:
            pass

    if window.name_button.on_click(e) and window.master_carbon is not None:
        window.name_text = window.master_carbon.name()
        window.name_obj = window.name_font.render(window.name_text, True, color_scheme.WHITE)
    
    # Deal with exportation.
    if window.export_button.on_click(e) and window.master_carbon == None:
        window.export_button.temp_color_change(color_scheme.RED)
    elif window.export_button.on_click(e):
        window.master_carbon.export_molocule('mol.data')
        window.saved = True

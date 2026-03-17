# Authoer: Ilan Weinberger
# Date: June 06 2025
# Description: Defines globally used key classes and functions such as the window class, the page class, the button class, and the collidepoint function.

import pygame
import ctypes
from typing import Any

class window():
    def __init__(
        self,
        icon: pygame.Surface,
        title: str,
        page_list: list[Any],
        is_resizable: bool = True,
        hide_maximize: bool = False,
        hide_minimize: bool = False,
        window_dimentions: list[int] = [900, 500],
    ) -> None:
        """Initialize the window with the given information.

        Parameters:
        -----------
        icon: The icon to be displayed on the window.
        title: The title of the window.
        page_list: A list of pages to be displayed in the window.
        fps: The frame rate of the window.

        Optional:
        ---------
        is_resizable: If False the window will not be resizable and the fullscreen button will not work.
        hide_maximize: If True the maximize button will not be visible or usable.
        hide_minimize: If True the minimize button will not be visible or usable.
        window_dimentions: The size of the window in x, y format. If not provided will default to 900, 500.
        """

        # Calculate and globally define monitor information and messurements.
        self.monitor_dimentions = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.window_dimentions = window_dimentions
        self.restore_window_dimentions = self.window_dimentions.copy()
        self.window_coordinates = [int(self.monitor_dimentions[0] / 2 - self.window_dimentions[0] / 2), int(self.monitor_dimentions[1] / 2 - self.window_dimentions[1] / 2)]
        self.display_info = pygame.display.Info()

        # Configure screen.
        self.screen = pygame.display.set_mode(self.window_dimentions, pygame.NOFRAME)
        self.icon = icon
        
        pygame.display.set_icon(icon)
        pygame.display.set_caption(title)

        #Define Pygame fonts.
        self.title_font = pygame.font.Font('fonts/Orbitron.ttf', 18)
        self.font = pygame.font.SysFont('Segoe UI Symbol', 15, bold=True)
        self.font_awesome = pygame.font.Font('./fonts/FontAwesome.otf', 15)

        # Globalize arguments.
        self.title = title

        # Define tracking variables.
        self.title_bar_height = self.title_font.get_height() + 5
        self.title_bar_button_width = 25
        self.toggle_fullscreen = False
        self.is_resizable = is_resizable
        self.hide_minimize = hide_minimize
        self.hide_maximize = hide_maximize

        self.in_game = True
        self.MBD = False
        self.frame_num = 0
        self.page = 0
        self.last_page = 0
        self.frame_num = 0

        # Define button & text objects.
        self.button_and_text_definitions()

        # Globalize pages and define important values.
        self.page_list = page_list
        for page in self.page_list:
            page.preloop_definitions(self)

        # Begin Main Loop.
        self.main_loop()

        # Quit Pygame.
        pygame.quit()
    
    ### BEGIN HELPER FUNCTION DEFINITIONS ###
    def button_and_text_definitions(self) -> None:
        """Initialize the buttons and text for the title bar."""
        # Text for screen title.
        self.title_text = self.title_font.render(self.title, True, (255, 255, 255))

        # Title bar icon scaling.
        self.icon_scale = self.title_bar_height / self.icon.get_height()
        self.icon = pygame.transform.scale(self.icon, ((self.icon.get_width() * self.icon_scale), (self.icon.get_height() * self.icon_scale)))

        # Definition of quit button (& associated objects).
        self.quit_button_rect = pygame.Rect((self.screen.get_width() - self.title_bar_button_width * 1.25, 0, self.title_bar_button_width * 1.25, self.title_bar_height))
        self.quit_button = button(self.screen, self.quit_button_rect, 'xmark', self.font_awesome, (200, 70, 70), (200, 0, 0), background_color=(13, 34, 43))

        # Definition of maximize button (& associated objects).
        self.max_button_rect = pygame.Rect((self.screen.get_width() - self.title_bar_button_width * 2.5, 0, self.title_bar_button_width * 1.25, self.title_bar_height))

        if self.is_resizable and not self.hide_maximize:
            self.max_button = button(self.screen, self.max_button_rect, 'expand', self.font_awesome, (255, 255, 255), (150, 150, 150), background_color=(13, 34, 43))
        elif not self.is_resizable and not self.hide_maximize:
            self.max_button = button(self.screen, self.max_button_rect, 'expand', self.font_awesome, (150, 150, 150), (150, 150, 150), background_color=(13, 34, 43), enabled=False)

        # Definition of minimize button (& associated objects).
        self.min_button_rect = pygame.Rect((self.screen.get_width() - self.title_bar_button_width * 3.75, 0, self.title_bar_button_width * 1.25, self.title_bar_height))
        
        if not self.hide_minimize:
            self.min_button = button(self.screen, self.min_button_rect, 'window-minimize', self.font_awesome, (255, 255, 255), (150, 150, 150), background_color=(13, 34, 43))

        # Definition of objects used in welcome animation.
        self.an_ball = pygame.Rect((50, 50, 50, 50))
        self.an_ball_pos = [0, 0, 0]

    def event_handler(self) -> None:
        """Track, respond to, and handle events in the window.

        This includes mouse and keyboard events, as well as window resizing and moving.
        Any additional events can be added using the page event handler.
        """
        
        # Track key & mouse movment.
        key = pygame.key.get_pressed()
        self.mouse_position = pygame.mouse.get_pos()

        for e in pygame.event.get():
            # When quit button or CTRL-W are pressed exit main loop and end the program.
            if e.type == pygame.QUIT or key[pygame.K_LCTRL] == True and key[pygame.K_w] == True or key[pygame.K_RCTRL] == True and key[pygame.K_w] == True:
                self.in_game = False

            # Track mouse button changes.
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.MBD = True
                self.relative_mouse_position = self.mouse_position
            elif e.type == pygame.MOUSEBUTTONUP:
                self.MBD = False

            # Events (hover & press) for X button.
            if self.quit_button.is_hover():
                # If pressed exit main loop.
                if e.type == pygame.MOUSEBUTTONUP:
                    self.in_game = False
            
            # Events (hover & press) for maximize button.
            if not self.hide_maximize:
                if self.max_button.is_hover() and self.is_resizable:
                    # If pressed while not in fullscreen mode enter fullscreen mode.
                    if e.type == pygame.MOUSEBUTTONUP and not self.toggle_fullscreen:
                        # Change window size & calculate the difference in dimentions.
                        screen_width_dif = self.screen.get_width()
                        self.window_dimentions = self.monitor_dimentions
                        self.screen = pygame.display.set_mode(self.window_dimentions, pygame.NOFRAME)
                        screen_width_dif = self.screen.get_width() - screen_width_dif

                        # Ajust window locations. (Taken from stackoverflow, link unavailable)
                        ctypes.windll.user32.MoveWindow(pygame.display.get_wm_info()["window"], 0, 0, self.window_dimentions[0], self.window_dimentions[1], True)

                        # Adjust location of title bar buttons.
                        self.quit_button.move_ip(screen_width_dif, 0)
                        self.max_button.move_ip(screen_width_dif, 0)
                        if not self.hide_minimize:
                            self.min_button.move_ip(screen_width_dif, 0)

                        # Change button icon.
                        self.max_button.change_text('compress')

                        self.toggle_fullscreen = True

                    # If pressed while in fullscreen mode exit fullscreen mode.
                    elif e.type == pygame.MOUSEBUTTONUP and self.toggle_fullscreen:
                        # Change window size & calculate difference in dimentions.
                        self.window_dimentions = self.restore_window_dimentions
                        self.screen = pygame.display.set_mode(self.window_dimentions, pygame.NOFRAME)
                        screen_width_dif = self.monitor_dimentions[0] - self.window_dimentions[0]

                        # Adjust window location.
                        ctypes.windll.user32.MoveWindow(pygame.display.get_wm_info()["window"], self.window_coordinates[0], self.window_coordinates[1], self.window_dimentions[0], self.window_dimentions[1], True)

                        # Adjust location of title bar buttons.
                        self.quit_button.move_ip(-screen_width_dif, 0)
                        self.max_button.move_ip(-screen_width_dif, 0)
                        if not self.hide_minimize:
                            self.min_button.move_ip(-screen_width_dif, 0)

                        # Change button icon.
                        self.max_button.change_text('expand')
                    
                        self.toggle_fullscreen = False

            # Events (hover & press) for minimize button if visibile.
            if not self.hide_minimize:
                if self.min_button.is_hover():
                    # If the button is pressed minimize the window.
                    if e.type == pygame.MOUSEBUTTONUP:
                        pygame.display.iconify()

            # Control the movment of the window by the user.
            if self.mouse_position[0] <= (self.screen.get_width() - self.title_bar_button_width * 3) and self.mouse_position[1] <= self.title_bar_height and not self.toggle_fullscreen:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    # When the title bar of the window is pressed move the window with the cursor.
                    if e.type == pygame.MOUSEMOTION and self.MBD:
                        self.updated_mouse_position = pygame.mouse.get_pos()
                        mouse_offset = (self.relative_mouse_position[0] - self.updated_mouse_position[0], self.relative_mouse_position[1] - self.updated_mouse_position[1])
                        self.window_coordinates = (int(self.window_coordinates[0] - mouse_offset[0] * 1.1), int(self.window_coordinates[1] - mouse_offset[1] * 1.1))
                        # Chaage the position of the window.
                        ctypes.windll.user32.MoveWindow(pygame.display.get_wm_info()["window"], self.window_coordinates[0], self.window_coordinates[1], self.window_dimentions[0], self.window_dimentions[1], True)
            # If no events take place revert the button to its normal state.
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # Adjust window size from the right when the user drags the right side.
            if self.mouse_position[0] >= (self.screen.get_width() - 7) and self.mouse_position[1] > self.title_bar_height and self.is_resizable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                # When the user presses on the right side of the window.
                if e.type == pygame.MOUSEMOTION and self.MBD:
                    # Calculate the difference in the mouses position (since the initiol click).
                    self.updated_mouse_position = pygame.mouse.get_pos()
                    difference = (self.updated_mouse_position[0] - self.relative_mouse_position[0])

                    # Ajust program variables & title bar buttons.
                    if self.window_dimentions[0] + difference >= 200:
                        self.window_dimentions[0] += difference
                        self.quit_button.move_ip(difference, 0)
                        if not self.hide_maximize:
                            self.max_button.move_ip(difference, 0)
                        if not self.hide_minimize:
                            self.min_button.move_ip(difference, 0)

                    # Change window size & reset variables.
                    self.relative_mouse_position = self.updated_mouse_position
                    self.screen = pygame.display.set_mode(self.window_dimentions, pygame.NOFRAME)
            
            # Adjust window size from the bottom when the user drags the bottom.
            if self.mouse_position[1] > (self.screen.get_height() - 5) and self.is_resizable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
                # When the user presses on the right side of the window.
                if e.type == pygame.MOUSEMOTION and self.MBD:
                    # Calculate the difference in the mouses position (since the initiol click).
                    self.updated_mouse_position = pygame.mouse.get_pos()
                    difference = (self.updated_mouse_position[1] - self.relative_mouse_position[1])

                    # Update window & reset variables.
                    if self.window_dimentions[1] + difference >= 200:
                        self.window_dimentions[1] += difference

                    self.relative_mouse_position = self.updated_mouse_position
                    self.screen = pygame.display.set_mode(self.window_dimentions, pygame.NOFRAME)
            
            # Handle any additional events accociated with the current page.
            self.page_list[self.page].event_handler(self, e, key)
        
        # Ensure that eventless keypresses (such as key holds) are still dealt with.
        try:
            self.page_list[self.page].event_handler(self, None, key)
        except Exception:
            pass
        
    def main_loop(self) -> None:
        while self.in_game:
            # If the page has changed run the new page's preloop definitions.
            if self.page != self.last_page:
                self.last_page = self.page
                self.page_list[self.page].preloop_definitions(self)

            # Reset Screen.
            self.screen.fill((0, 0, 0))

            # Handle events.
            self.event_handler()

            # Display current page.
            self.page_list[self.page].inloop_definitions(self.screen, self)

            # Control titlebar background size (based on fullscreen mode & changing window dimentions).
            if self.toggle_fullscreen:
                title_bar_bg = pygame.Rect((0, 0, self.monitor_dimentions[0], self.title_bar_height))
            else:
                title_bar_bg = pygame.Rect((0, 0, self.window_dimentions[0], self.title_bar_height))
            pygame.draw.rect(self.screen, (13, 34, 43), title_bar_bg)

            # Draw X, min, & max button in top right.
            self.quit_button.draw(border_width=0, border_width_hover=0)
            if not self.hide_maximize:
                self.max_button.draw(border_width=0, border_width_hover=0)
            if not self.hide_minimize:
                self.min_button.draw(border_width=0, border_width_hover=0)

            # Draw title & icon in top left.
            self.screen.blit(self.icon, (5, 0))
            self.screen.blit(self.title_text, (self.icon.get_width() + 15, 0))

            # Update Screen & track frame rate.
            pygame.display.update()
            self.frame_num += 1

class page:
    def __init__(self, preloop_definitions: Any, inloop_definitions: Any, event_handler: Any) -> None:
        """Initialize the page with preloop definitions, page function, and event handler.

        preloop_definitions: Function to be called before the main loop of the page.
        inloop_definitions: Function to be called during the main loop of the page.
        event_handler: Function to handle events for the page.

        This class is purley to simplfy passing a page to the window class.
        """
        self.preloop_definitions = preloop_definitions
        self.inloop_definitions = inloop_definitions
        self.event_handler = event_handler

class button:
    def __init__(self, screen, rect, text, font, color, hover_text_color, background_color=(0, 0, 0), enabled=True):
        """
        Initialize a button with its properties.

        Parameters:
        -----------
        screen: The pygame screen object which the button is to be accociated with.
        rect: The rectangle defining the button's position and size.
        text: The text to be displayed on the button.
        font: The font of the button's text.
        color: The default color of the button.
        hover_color: The color of the button when hovered over.
        background_color: The background color of the button (for use at all times).
        enables: if this is False the button will not be clickable and on hover will display a disabled mouse cursor.
        """
        # Globalized provided arguments.
        self.screen = screen

        self.rect = rect
        self.text = text
        self.font = font
        self.color = color
        self.hover_text_color = hover_text_color
        self.background_color = background_color

        self.enabled = enabled

        # Define tracking variables.
        self.is_hover_overide = False
        self.visible = True
        self.temp_color = None
    
    ### DEFINE CALLABLE METHODS ###
    def draw(self, intensity=255, border_width=4, border_width_hover=6):
        """
        Draw the button on the screen.
        """
        # If an intensity value is set change the intensity of the button's color.
        if intensity != 255:
            # Calculate the intensity as a percentage.
            intensity_percentage = intensity / 255

            # Set the colors (this is temporary).
            if self.temp_color != None:
                color = (self.temp_color[0] * intensity_percentage, self.temp_color[1] * intensity_percentage, self.temp_color[2] * intensity_percentage)
                hover_text_color = (self.temp_color[0] * intensity_percentage, self.temp_color[1] * intensity_percentage, self.temp_color[2] * intensity_percentage)

                self.color_timer -= 1
                if self.color_timer <= 0:
                    self.temp_color = None
            else:
                color = (self.color[0] * intensity_percentage, self.color[1] * intensity_percentage, self.color[2] * intensity_percentage)
                hover_text_color = (self.hover_text_color[0] * intensity_percentage, self.hover_text_color[1] * intensity_percentage, self.hover_text_color[2] * intensity_percentage)
        # If no intensity value is set set the temporary color variables to their full intensity.
        else:
            if self.temp_color != None:
                color = self.temp_color
                hover_text_color = self.temp_color

                self.color_timer -= 1
                if self.color_timer <= 0:
                    self.temp_color = None
            else:
                color = self.color
                hover_text_color = self.hover_text_color
        
        # Ensure that the button is only visible is the intensity is high enough.
        if intensity > 150:
            self.visible = True
        else:
            self.visible = False

        # Render the button text and border with a thicker border (if it is hovered over).
        if self.is_hover() or self.is_hover_overide:
            # Render button text.
            text_surface = self.font.render(self.text, True, hover_text_color)

            # Render as a solid rect (if no border radius was provided)
            if border_width_hover == 0:
                pygame.draw.rect(self.screen, self.background_color, self.rect, border_width_hover, 4)
            # Otherwise render as a hollow rect (if a border radius was provided)
            else:
                pygame.draw.rect(self.screen, hover_text_color, self.rect, border_width_hover, 4)
        # Render the button text and border with a thinner border (if it is not hovered over)
        else:
            # Render button text.
            text_surface = self.font.render(self.text, True, color)
            
            # Render as a solid rect (if no border radius was provided)
            if border_width == 0:
                pygame.draw.rect(self.screen, self.background_color, self.rect, border_width, 4)
            # Otherwise render as a hollow rect (if a border radius was provided)
            else:
                pygame.draw.rect(self.screen, hover_text_color, self.rect, border_width, 4)

        # Render the text and blit it to the screen.
        self.screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) / 2, self.rect.y + (self.rect.height - text_surface.get_height()) / 2))
    
    def on_click(self, e):
        """
        Check if the button is clicked.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        if self.is_hover() and e.type == pygame.MOUSEBUTTONDOWN:
            return True
        return False

    def move_ip(self, x, y):
        """
        Move the button's rectangle by the given x and y offsets.
        """
        self.rect.move_ip(x, y)

    def is_hover(self):
        """
        Check if the mouse is hovering over the button.

        Returns:
            bool: True if the mouse is hovering over the button, False otherwise.
        """
        # Get the current mouse position.
        mouse_pos = pygame.mouse.get_pos()

        # Check is the mouse is over the button rect.
        is_hover_track = collidepoint(self.rect, mouse_pos)

        # Change the mouse cursor to a hand when hovering over the button (or a disabled sign if hover while the button is disabled).
        # Handle mouse cursor on an enabled button.
        if self.visible:
            if self.enabled:
                if is_hover_track and pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif is_hover_track and pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            # Handle mouse cursor on a disabled button.
            else:
                if is_hover_track and pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_NO:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                elif is_hover_track and pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Return True the mouse is over the button otherwise False.
        return is_hover_track
    
    def temp_color_change(self, color, frames = 70):
        """
        Changes all aspects of the button to the provided color for a given number of frames.

        Arguments
        ---------
        color: The color to which the button should be changed.
        frames (optional): The number of frames the change should be present for. Defaults to 70 frames.

        Returns Nothing
        """
        self.temp_color = color
        self.color_timer = frames

    ### BEING SETTER METHOD DEFINITIONS ###
    def change_text(self, text):
        """
        Change the text of the button.

        text: The new text to be displayed on the button.
        """
        self.text = text

    def overide_hover(self, is_hover):
        """
        Override the hover state of the button.

        is_hover: Boolean value to set the hover state.
        """
        self.is_hover_overide = is_hover

    def set_button_text(self, text):
        """
        Change the text on the button.
        """
        self.text = text
    
    ### DEFINE GETTER METHOD DEFINITIONS ###
    def get_button_text(self):
        """
        Return the button's text.
        """
        return self.text

def collidepoint(rect, point):
    """
    Check if a point is inside a rectangle.

    rect: The rectangle to check.
    point: The point to check.

    Returns:
        bool: True if the point is inside the rectangle, False otherwise.
    """
    return rect.left <= point[0] <= rect.right and rect.top <= point[1] <= rect.bottom
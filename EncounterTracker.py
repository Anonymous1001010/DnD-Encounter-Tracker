import pygame
import random as r
import sys

# Initialize PyGame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("D&D Initiative Tracker")
font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()
WIDTH, HEIGHT = pygame.display.get_surface().get_size()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Data structures
participants = {}
initiative_order = []

# Input box for text commands
input_box = pygame.Rect(40, 550, WIDTH - 250, 30)
# input_box = pygame.Rect(40, 840, WIDTH - 20, 30)

input_text = ""
active_input = True
message = "Enter a command:"
active_conditions = {}

# Helper functions
def roll_initiative(new_only=None):
    """Roll initiative for all or newcomers."""
    global initiative_order
    if not participants:
        return

    # If new_only is None, roll for all participants
    if new_only is None:
        for person in participants:
            participants[person]["initiative"] = r.randint(1, 20)
    elif new_only:
        # Only roll initiative for newcomers (those without initiative)
        for person in participants:
            if "initiative" not in participants[person]:
                participants[person]["initiative"] = r.randint(1, 20)
    else:
        # Roll initiative for everyone
        for person in participants:
            participants[person]["initiative"] = r.randint(1, 20)

    # Sort participants by initiative, in descending order
    initiative_order = sorted(
        [(name, data["initiative"]) for name, data in participants.items() if "initiative" in data],
        key=lambda x: x[1],
        reverse=True,
    )

def apply_condition(condition, effect, duration, target):
    target=target.capitalize()
    if target not in active_conditions:
        active_conditions[target] = []
    active_conditions[target].append((condition, effect, duration))
    return f"Condition '{condition}' applied to {target.capitalize()} for {duration} turns."

def advance_conditions():
    to_remove = []

    for target, conditions in active_conditions.items():
        for condition, effect, duration in conditions:
            if duration > 1:
                conditions[conditions.index((condition, effect, duration))] = (condition, effect, duration - 1)
            else:
                to_remove.append((target, condition))
    # Remove expired conditions
    for target, condition in to_remove:
        active_conditions[target] = [c for c in active_conditions[target] if c[0] != condition]
    
    return "Conditions advanced by one turn."

def remove_condition(target, condition=None):
    """Remove a specific condition or all conditions from a participant."""
    if target in active_conditions:
        if condition:
            active_conditions[target] = [
                cond for cond in active_conditions[target] if cond[0] != condition
            ]
            return f"Condition '{condition}' removed from {target.capitalize()}."
        else:
            active_conditions[target] = []
            return f"All conditions removed from {target.capitalize()}."
    return f"Target '{target}' not found or has no conditions."

def add_character(name, health, ac):
    """Add a new character to the tracker."""
    if name in participants:
        return f"Character '{name}' already exists!"
    participants[name] = {"health": health, "ac": ac}
    return f"Character '{name}' added with {health} HP and {ac} AC."

def remove_character(name):
    """Remove a character from the tracker."""
    if name in participants:
        del participants[name]
        return f"Character '{name.capitalize()}' removed."
    return f"Character '{name.capitalize()}' not found."

def modify_health_ac(name, health=None, ac=None):
    """Modify a character's health or AC."""
    if name.capitalize() not in participants:
        return f"Character '{name.capitalize()}' not found."

    if health is not None:
        participants[name.capitalize()]["health"] = health
    if ac is not None:
        participants[name.capitalize()]["ac"] = ac
    
    return f"Character '{name.capitalize()}' updated with HP: {participants[name.capitalize()]['health']} and AC: {participants[name.capitalize()]['ac']}."

def draw_multiline_text(text, x, y, width, line_spacing=5):
    """Render multiline text within a specified width."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = current_line + [word]
        test_text = font.render(" ".join(test_line), True, BLACK)
        if test_text.get_width() <= width:
            current_line = test_line
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    for line in lines:
        rendered_text = font.render(line, True, BLACK)
        screen.blit(rendered_text, (x, y))
        y += rendered_text.get_height() + line_spacing

def draw_command_key(x, y):
    """Draw the command key in the bottom-right corner."""
    commands = [
        "Command Key:",
        "1. Add: Add, name, health, ac",
        "2. Remove: Remove, name",
        "3. Add condition: Condition, effect, duration, target",
        "4. Advance conditions: Advance",
        "5. Remove condition: Remove, target, [condition]",
        "6. Initiative: roll, [new_only]",
        "7. Modify Health/AC: Modify, name, [health], [ac]",
    ]
    padding = 10
    key_width = 600
    key_height = len(commands) * (font.get_height() + 5) + padding * 2

    # Draw background
    pygame.draw.rect(screen, GRAY, (x - key_width, y - key_height, key_width, key_height))
    pygame.draw.rect(screen, BLACK, (x - key_width, y - key_height, key_width, key_height), 2)

    # Draw commands
    text_y = y - key_height + padding
    for command in commands:
        command_surface = font.render(command, True, BLACK)
        screen.blit(command_surface, (x - key_width + padding, text_y))
        text_y += font.get_height() + 5

# Adjust the input box setup and handling:
def draw_ui():
    """Render the UI."""
    screen.fill(WHITE)
    WIDTH, HEIGHT = screen.get_size()

    # Title
    title = font.render("D&D Encounter Tracker", True, (0,0,0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

    # Participant list
    y_offset = 50
    for person, data in participants.items():
        person.capitalize
        text = f"{person} | HP: {data['health']} | AC: {data['ac']} | Initiative: {data.get('initiative', 'N/A')}"
        draw_multiline_text(text, 50, y_offset, WIDTH - 300)
        y_offset += 60
        
        # Check if the character has conditions
        # Display conditions with indentation and remaining duration
        if person in active_conditions and active_conditions[person]:
            for condition, effect, duration in active_conditions[person]:
                condition_text = f"  - {condition.capitalize()}: {effect.capitalize()}, {duration} Turns Remaining"
                draw_multiline_text(condition_text, 70, y_offset, WIDTH - 225)
                y_offset += 30


    # Initiative order
    y_offset += 20
    order_title = font.render("Initiative Order:", True, (0,0,0))
    screen.blit(order_title, (50, y_offset))
    y_offset += 30
    for person, initiative in initiative_order:
        order_text = font.render(f"{person}: {initiative}", True, (0,0,0))
        screen.blit(order_text, (50, y_offset))
        y_offset += 30

    # Input box and message
    pygame.draw.rect(screen, GRAY if active_input else WHITE, input_box)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))  # Text inside the box
    pygame.draw.rect(screen, BLACK, input_box, 2)  # Draw the border of the input box

    message_surface = font.render(message, True, BLACK)
    screen.blit(message_surface, (40, HEIGHT - 80))

    # Command key box position at the bottom-right, ensuring visibility
    draw_command_key(WIDTH, HEIGHT-60)
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:  # Detect resizings
            WIDTH, HEIGHT = pygame.display.get_surface().get_size()
            input_box = pygame.Rect(40, HEIGHT - 50, WIDTH - 140, 30)
        if event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    if "," in input_text or input_text=="roll" or input_text=="advance" or input_text[0].lower()=="mode":
                        parts = [x.strip() for x in input_text.split(",")]
                        if parts[0].lower() == "add":
                            if len(parts) == 4:
                                name, health, ac = parts[1:4]
                                try:
                                    health, ac = int(health), int(ac)
                                    message = add_character(name.capitalize(), health, ac)
                                except ValueError:
                                    message = "Invalid health/AC! Must be integers."
                            else:
                                message = "Format: Add name, health, ac"
                        elif parts[0].lower() == "remove" and parts[1].lower() != "condition":
                            name = parts[1]
                            message = remove_character(name.capitalize())
                        elif parts[0].lower() == "condition":
                            # Split the input string by commas and strip spaces
                            condition_parts = parts
                            # Ensure there are exactly 4 parts: condition, effect, duration, target
                            if len(condition_parts) == 5:
                                condition, effect, duration, target = condition_parts[1:]
                                try:
                                    duration = int(duration)  # Convert duration to an integer
                                    target.capitalize()
                                    message = apply_condition(condition, effect, duration, target)  # Apply the condition
                                except ValueError:
                                    message = "Duration must be an integer!"
                                except Exception as e:
                                    message = f"Error: {str(e)}"  # Catch other potential errors
                            else:
                                message = "Format: condition name, effect, duration, target"

                        elif parts[0].lower() == "advance":
                            message = advance_conditions()
                        elif parts[0].lower() == "roll":
                            if len(parts) == 2 and parts[1].lower() == "new":
                                roll_initiative(new_only=True)
                                message = "Rolling initiative for new characters only."
                            else:
                                roll_initiative(new_only=None)
                                message = "Rolling initiative for all characters."
                        elif parts[0].lower() == "modify" and len(parts) == 4:
                            modify_health_ac(parts[1],parts[2],parts[3])

                        elif parts[0].lower() == "remove" and parts[1].lower=="condition":
                            if len(parts) == 2:
                                target = parts[1]
                                message = remove_condition(target)
                            elif len(parts) == 3:
                                target, condition = parts[1], parts[2]
                                message = remove_condition(target, condition)
                        elif parts[0].lower() == "mode":
                            if parts[1].lower() == "light":
                                BLACK == (0,0,0)
                                WHITE == (255,255,255)
                            elif parts[1].lower()== "dark":
                                BLACK == (255,255,255)
                                WHITE ==(0,0,0)
                    else:
                        message = "Invalid command format!"
                    input_text = ""  # Clear input text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    draw_ui()
    clock.tick(60)  # Limit FPS to 60
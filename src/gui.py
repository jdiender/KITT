# GUI-do Quaroni
import sys, pygame

from gui_constants import \
    WINDOW_WIDTH, \
    WINDOW_HEIGHT, \
    FIELD_X_OFFSET, \
    FIELD_Y_OFFSET, \
    FIELD_WIDTH, \
    FIELD_HEIGHT, \
    Position;

from localize import localization
from model import car

def main() -> int:
    "GUI-do tool for KITT"
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    current_position = Position(-1, -1)

    while running:
        # Record transmitted beacon-signal.
        #recording =
        # Estimate location using said recording.
        #estimated_position =
        current_position.update(estimated_position[0], estimated_position[1])

        # Temporary location for testing GUI-do
        # current_position.update(2.4, 4.8)

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("#000010")

        # Render field
        pygame.draw.rect(screen, "#eedd82", (FIELD_X_OFFSET,
                                             FIELD_Y_OFFSET,
                                             FIELD_WIDTH,
                                             FIELD_HEIGHT))
        # Render location here
        pygame.draw.circle(screen, "red", current_position.get(), 20)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Finish!
    pygame.quit()

if __name__ == '__main__':
    sys.exit(main())

import pygame
import pygame_gui

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/background.mp3")  
pygame.mixer.music.set_volume(0.5)     
pygame.mixer.music.play(-1)  

click_sound = pygame.mixer.Sound("assets/click.wav")
click_sound.set_volume(0.6) 


screen_width = 1280
screen_height = 832
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CODING RACE")

tlo = pygame.image.load("assets/gotowe.png")
tlo = pygame.transform.scale(tlo, (screen_width, screen_height))

manager = pygame_gui.UIManager((screen_width, screen_height), "theme.json")

font = pygame.font.Font("C:/Users/kubaa/AppData/Local/Microsoft/Windows/Fonts/Michroma-Regular.ttf", 32)

MENU, SETTINGS = "menu", "settings"
current_screen = MENU
game_title = pygame_gui.elements.UILabel(
    
    relative_rect=pygame.Rect((0, -220), (470, 80)),
    text='Coding Race',
    manager=manager,
    object_id='#game_title',
    anchors={'center': 'center'}
)

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen_width//2-190, 300), (380, 80)),
    text='Start',
    manager=manager
)
settings_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen_width//2-190, 420),  (380, 80)),
    text='Settings',
    manager=manager
)
exit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen_width//2-190, 540),  (380, 80)),
    text='Exit',
    manager=manager
)

volume_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 350), (300, 50)),
    start_value=0.5,
    value_range=(0.0, 1.0),
    manager=manager
)
back_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen_width//2-190, 450), (380, 80)),
    text='Back',
    manager=manager
)

volume_slider.hide()
back_button.hide()

clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    screen.blit(tlo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            click_sound.play()

            if event.ui_element == start_button:
                print("rozpoczynamy gre")
            elif event.ui_element == exit_button:
                running = False
            elif event.ui_element == settings_button:
                current_screen = SETTINGS
                start_button.hide()
                settings_button.hide()
                exit_button.hide()
                volume_slider.show()
                back_button.show()
            elif event.ui_element == back_button:
                current_screen = MENU
                start_button.show()
                settings_button.show()
                exit_button.show()
                volume_slider.hide()
                back_button.hide()
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == volume_slider:
            volume = event.value
            pygame.mixer.music.set_volume(volume)
            click_sound.set_volume(volume)
        
        manager.process_events(event)
    
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()

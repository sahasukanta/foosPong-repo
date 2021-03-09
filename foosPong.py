import pygame

def main():

    pygame.init()

    # making the main window screen
    size = (1280,720)
    screen = pygame.display.set_mode(size)
    # window title
    title = "Pong"
    pygame.display.set_caption(title)
    # window icon
    icon = pygame.image.load("pong_ball.png")
    pygame.display.set_icon(icon)

    game = Game(screen)
    game.play()

class Line:

    def __init__(self, start, end, width, color, screen):
        self.start = start
        self.end = end
        self.width = width
        self.color = color
        self.screen = screen

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.start, self.end, self.width)

class Ellipse:

    def __init__(self, rect_left, rect_top, rect_width, rect_height, screen):
        self.rect_left = rect_left
        self.rect_top = rect_top
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.screen = screen

    def draw(self, width):
        rect = pygame.Rect(self.rect_left, self.rect_top, self.rect_width, self.rect_height)
        pygame.draw.ellipse(self.screen, pygame.Color("white"), rect, width)

class Paddle:
    # Attributes:
    # -- left
    # -- top
    # -- width
    # -- height
    # -- velocity
    # -- color
    # -- screen
    # Methods:
    # -- draw
    # -- bound_check
    def __init__(self, left, top, width, height, velocity, color, screen):
        # dimensions
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.bottom = self.top + self.height
        self.middle = self.left + self.width/2
        self.right = self.left + self.width
        # others
        self.velocity = velocity
        self.color = color
        self.screen = screen

    def draw(self):
        # draws the paddle rect onto the display
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.rect)

    def bound_check(self):
        # stops the pads from going out of the display through the y axis
        if self.top > self.screen.get_height()-self.height:
            self.top = self.screen.get_height()-self.height
        if self.top < 0:
            self.top = 0

class Ball:
    # Attributes:
    # -- radius
    # -- center
    # -- velocity
    # -- color
    # -- screen
    # Methods:
    # -- draw
    # -- move**
    def __init__(self, dot_radius, dot_center, dot_velocity, dot_color, screen):
        self.radius = dot_radius
        self.center = dot_center
        self.left = self.center[0] - self.radius
        self.right = self.center[0] + self.radius
        self.color = dot_color
        self.screen = screen
        self.velocity = dot_velocity

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)

    def move(self):
        # moves the ball across the display
        # keeps the ball within the display
        display_width, display_height  = self.screen.get_size()
        # boundary checking
        if self.center[0] > display_width:
            self.velocity[0] *= -1
        if self.center[0] < 0:
            self.velocity[0] *= -1
        if self.center[1] > display_height:
            self.velocity[1] *= -1
        if self.center[1] < 0:
            self.velocity[1] *= -1
        # updating position of center
        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]

class Game:
    # main game class
    def __init__(self, game_screen):
         # --- attributes general to all games
        self.x_min = 0
        self.y_min = 0
        self.x_max = 1280
        self.y_max = 720
        self.screen = game_screen
        self.background_color = pygame.Color("black")
        self.game_clock = pygame.time.Clock()
        self.fps = 120
        self.continue_game = True
        self.close_clicked = False

        # creating the paddle objects
        left_pad_left = self.x_min + 100
        left_pad_top = self.y_min + 280
        left_pad_width = 10
        left_pad_height = 120
        left_pad_velocity = 0
        left_pad_color = pygame.Color("orangered")
        self.left_pad = Paddle(left_pad_left, left_pad_top, left_pad_width, left_pad_height, left_pad_velocity, left_pad_color, self.screen)

        left_pad_2_left = self.x_min + 300
        left_pad_2_top = self.y_min + 280
        left_pad_2_width = 10
        left_pad_2_height = 120
        left_pad_2_velocity = 0
        left_pad_2_color = pygame.Color("orangered")
        self.left_pad_2 = Paddle(left_pad_2_left, left_pad_2_top, left_pad_2_width, left_pad_2_height, left_pad_2_velocity, left_pad_2_color, self.screen)

        right_pad_left = self.x_max - 120
        right_pad_top = 280
        right_pad_width = 10
        right_pad_height = 120
        right_pad_velocity = 0
        right_pad_color = pygame.Color("chartreuse")
        self.right_pad = Paddle(right_pad_left, right_pad_top, right_pad_width, right_pad_height, right_pad_velocity, right_pad_color, self.screen)

        right_pad_2_left = 960
        right_pad_2_top = 280
        right_pad_2_width = 10
        right_pad_2_height = 120
        right_pad_2_velocity = 0
        right_pad_2_color = pygame.Color("chartreuse")
        self.right_pad_2 = Paddle(right_pad_2_left, right_pad_2_top, right_pad_2_width, right_pad_2_height, right_pad_2_velocity, right_pad_2_color, self.screen)

        # creating the ball object
        dot_radius = 5
        dot_center = [450,300]
        dot_color = pygame.Color("aquamarine")
        dot_velocity = [4,4]
        self.ball = Ball(dot_radius, dot_center, dot_velocity, dot_color, self.screen)

        # creating line objects
        midline_start = (640,0)
        midline_end = (640,720)
        midline_width = 3
        midline_color = pygame.Color("white")
        self.midline = Line(midline_start, midline_end, midline_width, midline_color, self.screen)

        # right goal lines
        right_goalline_start = (1258,280)
        right_goalline_end = (1258,400)
        right_goalline_width = 3
        right_goalline_color = pygame.Color("white")
        self.right_goalline = Line(right_goalline_start, right_goalline_end, right_goalline_width, right_goalline_color, self.screen)

        right_goalline_A_start = (1258,280)
        right_goalline_A_end = (1280,250)
        right_goalline_A_width = 3
        right_goalline_A_color = pygame.Color("white")
        self.right_goalline_A = Line(right_goalline_A_start, right_goalline_A_end, right_goalline_A_width, right_goalline_A_color, self.screen)

        right_goalline_B_start = (1258,400)
        right_goalline_B_end = (1280,430)
        right_goalline_B_width = 3
        right_goalline_B_color = pygame.Color("white")
        self.right_goalline_B = Line(right_goalline_B_start, right_goalline_B_end, right_goalline_B_width, right_goalline_B_color, self.screen)


        # left goal lines
        left_goalline_start = (20,280)
        left_goalline_end = (20,400)
        left_goalline_width = 3
        left_goalline_color = pygame.Color("white")
        self.left_goalline = Line(left_goalline_start, left_goalline_end, left_goalline_width, left_goalline_color, self.screen)

        left_goalline_A_start = (20,280)
        left_goalline_A_end = (0,250)
        left_goalline_A_width = 3
        left_goalline_A_color = pygame.Color("white")
        self.left_goalline_A = Line(left_goalline_A_start, left_goalline_A_end, left_goalline_A_width, left_goalline_A_color, self.screen)

        left_goalline_B_start = (20,400)
        left_goalline_B_end = (0,430)
        left_goalline_B_width = 3
        left_goalline_B_color = pygame.Color("white")
        self.left_goalline_B = Line(left_goalline_B_start, left_goalline_B_end, left_goalline_B_width, left_goalline_B_color, self.screen)

        rect_left = 590
        rect_top = 295
        rect_width = 100
        rect_height = 100
        self.center_ellipse = Ellipse(rect_left, rect_top, rect_width, rect_height, self.screen)

        # setting initial score
        self.left_pad_score = 0
        self.right_pad_score = 0

    def handle_events(self):
        # cross click event
        # key down and up events
        # implementing the bound check method of paddles

        for event in pygame.event.get():
            # close game event
            if event.type == pygame.QUIT:
                self.close_clicked = True
            # left pad events
            if event.type == pygame.KEYDOWN:
                # left pad 1 key down events
                if event.key == pygame.K_a:
                    self.left_pad.velocity = 4
                if event.key == pygame.K_q:
                    self.left_pad.velocity = -4
                # left pad 2 key down events
                if event.key == pygame.K_d:
                    self.left_pad_2.velocity = 4
                if event.key == pygame.K_e:
                    self.left_pad_2.velocity = -4
            if event.type == pygame.KEYUP:
                # left pad key down events
                if event.key == pygame.K_a:
                    self.left_pad.velocity = 0
                if event.key == pygame.K_q:
                    self.left_pad.velocity = 0
                # left pad 2 key down events
                if event.key == pygame.K_d:
                    self.left_pad_2.velocity = 0
                if event.key == pygame.K_e:
                    self.left_pad_2.velocity = 0
            # righ pad events
            if event.type == pygame.KEYDOWN:
                 # right pad key down events
                if event.key == pygame.K_l:
                    self.right_pad.velocity = 4
                if event.key == pygame.K_p:
                    self.right_pad.velocity = -4
                if event.key == pygame.K_j:
                    self.right_pad_2.velocity = 4
                if event.key == pygame.K_i:
                    self.right_pad_2.velocity = -4
            if event.type == pygame.KEYUP:
                # right pad key down events
                if event.key == pygame.K_l:
                    self.right_pad.velocity = 0
                if event.key == pygame.K_p:
                    self.right_pad.velocity = 0
                # right pad 2 key down events
                if event.key == pygame.K_j:
                    self.right_pad_2.velocity = 0
                if event.key == pygame.K_i:
                    self.right_pad_2.velocity = 0
            # both right and left pads keydown at the same time:


        # updating pad y (top) point
        self.left_pad.top += self.left_pad.velocity
        self.left_pad_2.top += self.left_pad_2.velocity
        self.right_pad.top += self.right_pad.velocity
        self.right_pad_2.top += self.right_pad_2.velocity
        self.left_pad.bound_check()
        self.right_pad.bound_check()

    def draw(self):
        # draws the pads and ball
        # fill the screen with black
        self.screen.fill(self.background_color)
        # draws all game objects to screen
        self.left_pad.draw()
        self.left_pad_2.draw()
        self.right_pad.draw()
        self.right_pad_2.draw()
        self.ball.draw()
        self.midline.draw()
        self.right_goalline.draw()
        self.right_goalline_A.draw()
        self.right_goalline_B.draw()
        self.left_goalline.draw()
        self.left_goalline_A.draw()
        self.left_goalline_B.draw()
        self.center_ellipse.draw(3)

        # pygame.display.flip()

    def collide(self):
        # detects collision with pads and ball
        # if self.ball.center[0] < self.left_pad.right and self.ball.velocity[0] > 0: collision = False               # these two lines set collision to false when ball is behind the pad.
        # elif self.ball.center[0] > self.right_pad.left and self.ball.velocity[0] < 0: collision = False
        # else: collision = True
        collision = True
        if collision == True:
            if self.left_pad.rect.collidepoint(self.ball.center) or self.left_pad_2.rect.collidepoint(self.ball.center):
                self.ball.velocity[0] *= -1
        if collision == True:
            if self.right_pad.rect.collidepoint(self.ball.center) or self.right_pad_2.rect.collidepoint(self.ball.center):
                self.ball.velocity[0] *= -1

    def score(self):
        # updates the score
        display_width = self.screen.get_width()
        if self.ball.center[0] > display_width:
            self.left_pad_score += 1
            if self.left_goalline_A.end[1] <= self.ball.center[1] <= self.left_goalline_B.end[1]:
                self.left_pad_score += 1

        if self.ball.center[0] < 0:
            self.right_pad_score += 1
            if self.right_goalline_A.end[1] <= self.ball.center[1] <= self.right_goalline_B.end[1]:
                self.right_pad_score += 1
        # if self.left_goalline_A.end[1] <= self.ball.center[1] <= self.left_goalline_B.end[1]:
        #     self.left_pad_score += 1


    def display_score(self):
        # displays the updates scores
        right_text = str(self.right_pad_score)
        left_text = str(self.left_pad_score)
        right_text_pos = (1210,25)
        left_text_pos = (30,25)

        text_color = pygame.Color("white")
        text_font = pygame.font.SysFont('freesansbold.ttf', 64)
        right_text_image = text_font.render(right_text, True, text_color)
        left_text_image = text_font.render(left_text, True, text_color)

        self.screen.blit(right_text_image, right_text_pos)
        self.screen.blit(left_text_image, left_text_pos)
        pygame.display.flip()

    def check_continue(self):
        # checks for max points limit (11) and if game should continue
        if self.left_pad_score > 11 or self.right_pad_score > 11:
            self.continue_game = False

    def update(self):
        # updates ball movement and score
        self.ball.move()
        self.score()

    def play(self):
        # main gameplay method
        while not self.close_clicked:
            self.handle_events()
            self.draw()
            self.display_score()
            self.check_continue()
            if self.continue_game:
                self.collide()
                self.update()
            self.game_clock.tick(self.fps)


main()

from manim import *
import math

# The video for this formula has a lot of different types of scenes. Therefore it needs to be editited in a 
# video-editor. Instructions for the flow are commented in the docstrings of each class.

class SD1(MovingCameraScene):
    def construct(self):
        """"
        First scene as introduction to the standard deviation. We're gonna move along a numberline in the range -10 till
        160 (later on 190 but its not visible in the video). The start is at -2 till round 6 so the camera is gonna move
        till point 150. For this the 'MovingCameraScene' is used.
        """

        # Beginning of the scene is set up with this numberline 
        line = NumberLine(x_range=(-10, 160, 1), length=170, color=GREEN_E, include_numbers=True, label_direction=DOWN, 
                          font_size=40).set_opacity(1)
        self.add(line)

        # Setting the camera in the right position
        self.camera.frame.move_to(line.n2p(2)).set_width(10)  # Set the beginning point of the video
        self.wait(1) 

        # This actually moves the camera along the line to point 150
        self.play(self.camera.frame.animate.move_to(line.n2p(150)).set_width(10),
            run_time=5, rate_func=smooth)
        self.wait(2)

        # Later on in the video all the numbers will be shown with an interval of 10. Therefore a new numberline is created with these intervals
        line2 = NumberLine(x_range=(-10, 160, 10), length=170, color=GREEN_E, include_numbers=True, label_direction=DOWN, 
                           font_size=40).set_opacity(2)
        line2.move_to(line)

        # For smooth transition the first line is faded out and the second line is faded in
        self.play(FadeOut(line, run_time=1), FadeIn(line2, run_time=2))
        self.wait(1)

 
class SD2(ZoomedScene):
    def construct(self):
        """"
        This class has the "ZoomedScene" as parent class. This means that the scene can be zoomed in or out. In this scene it is used
        to zoom out such that we can see the whole numberline, well the parts which are relevant for our data, which we created before.
        It is recreated in this scene. It is necessary to create a different class due to the differing parent classes of the parts.
        After the zooming out the dots of our data points as drawn on the numberline. The whole numberline is then rotated with their labels
        such that it is now a vertical line. The dots are first faded out but then correctly restored to their positions, also rotated.
        The dots + numberline are moved to the left and a dashed line is drawn from 150, which is the average, to the right. The deviations
        from the dots are drawn as lines to the average.
        Then the whole scene is zoomed out and the deviations are kind of plucked out to square them. After they are added together to create
        a big square which represents the sum of total surface.
        """
        # Original line from where we left off in the previous scene
        height_line = NumberLine(x_range=(90, 200, 10), length=110, color=GREEN_E, include_numbers=True, label_direction=DOWN, 
                                 font_size=40).set_opacity(1)
        self.add(height_line)
        
        self.camera.frame.move_to(height_line.number_to_point(150)).set_width(10)  

        # Zooming out to see the whole numberline
        for width, font in [(37, 110), (64, 180), (90, 250)]:
            updated_line = NumberLine(x_range=(90, 200, 10), length=110, color=GREEN_E, include_numbers=True, label_direction=DOWN,
                font_size=font, stroke_width=20).move_to(height_line)
            
            self.play(self.camera.frame.animate.set_width(width), 
                      ReplacementTransform(height_line, updated_line), run_time=1, rate_func=smooth)
            
            height_line = updated_line

        self.wait(2)

        # Create a new line with a smaller lenght 
        dot_line = NumberLine(x_range=(110, 190, 10), length=8, color=GREEN_E, include_numbers=True, label_direction=DOWN,
            font_size=30, stroke_width=2)
        dot_line.move_to([height_line.number_to_point(150)[0], height_line.get_center()[1], 0])

        # Replace the lines. Now we also zoom out. This is for working with the numberline and the dots
        self.play(ReplacementTransform(height_line, dot_line), self.camera.frame.animate.set_width(9.5), run_time=1, rate_func=smooth)
        self.wait(2)

        # Our data as dots
        points = [(120, 1), (130, 1), (140, 1), (150, 1), (160, 1), (170, 1), (180, 1)]
        doubles = [140, 160]
        dots = VGroup()

        # The correct positioning of the dots in space
        for x, y in points:
            dot = Dot(dot_line.number_to_point(x), color=RED, radius=0.05).shift(0.5*UP)
            dots.add(dot)
            
            if x in doubles:
                dot = Dot(dot_line.number_to_point(x), color=RED, radius=0.05).shift(UP*1)
                dots.add(dot)
        self.play(Create(dots), run_time=2)

        # We're gonna rotate the line to a vertical line
        vertical_line = NumberLine(x_range=(110, 190, 10), length=8, color=GREEN_E, include_numbers=False,
                font_size=30, stroke_width=2).rotate(PI / 2)
        vertical_line.move_to(dot_line.number_to_point(150))
        
        # To ensure the labels are also vertically we have to manually rotate them
        labels = VGroup()
        for x in range(110, 191, 10):  
            label = Text(str(x), font_size=30)
            label.move_to(vertical_line.number_to_point(x) + LEFT * 0.5)
            labels.add(label)

        # Here the dots are copied and rotated. For smooth transition purposes they are first faded out and then faded in, otherwise
        # the rotation wasn't accurate
        mirrored_dots = dots.copy().rotate(-PI/2, about_point=dot_line.number_to_point(150))
        self.play(FadeOut(dots))

        # Smooth transformation from horizontal to vertical while also adjusting the frame width and adding dots+labels
        self.play(Transform(dot_line, vertical_line), self.camera.frame.animate.set_width(15), 
                  FadeIn(mirrored_dots), FadeIn(labels), run_time=2)
        
        self.wait(1)

        # Remove the dot_line other wise it will remain in the scene at its original place
        self.remove(dot_line)

        # Shifting all objects to the left
        shift_left = VGroup(vertical_line, labels, mirrored_dots)
        self.play(ApplyMethod(shift_left.shift, 6*LEFT), run_time=2)
        self.wait(1)

        # Get the matching coordinates of the vertical line to draw a dashed line as the average
        start_dashed = vertical_line.get_center()[0]
        y_axis_dashed = vertical_line.number_to_point(150)[1]
        
        # Compile the dashed line
        dashed = DashedLine(start=[start_dashed, y_axis_dashed, 0], end=[10, y_axis_dashed, 0], dashed_ratio=0.3)

        self.play(Create(dashed))
        self.wait(1)

        # Dots are going to move in space to the right.
        new_x = mirrored_dots[8].get_center()[0] + 1  
        for dot in reversed(mirrored_dots):
            self.play(dot.animate.move_to([new_x, dot.get_center()[1], 0]), run_time=0.5)
            new_x += 1  # Increment the x position for the next dot

        # Now we're gonna create lines which represent the deviation of the data points from the average
        deviation_lines = VGroup()

        for dot in reversed(mirrored_dots):
            line = Line(start=dot.get_center(), end=[dot.get_center()[0], y_axis_dashed, 0], color=BLUE)
            deviation_lines.add(line)
            self.play(Create(line), run_time=0.5)
            self.play(FadeOut(dot), run_time=0.1) # Removing the dot looks nicer
            
        self.wait(1)

        #  Scene is zoomed out and moved to DR 
        self.play(self.camera.frame.animate.scale(4).shift(DOWN*12 + RIGHT*22))
        self.wait(1)

        # The bgeinning of squaring every deviation from a line to a square
        movement=0
        squares = VGroup()
        sum_surface = 0

        # In this loop it is actually squared and positioned at a handy place
        for l in deviation_lines:
            if movement < 40:
                x_shift = movement
                y_shift = -18  
            elif movement ==40:
                self.play(FadeOut(l), run_time=0.1)
                movement +=10
                continue
            else:
                x_shift = movement-55
                y_shift = -6

            current_start = l.get_start()
            current_end = l.get_end()
            start = [current_start[0] + x_shift, y_shift, 0] 
            end = [current_end[0] + x_shift, y_shift - l.get_length(), 0]

            self.play(l.animate.put_start_and_end_on(start, end).scale(3))
            movement +=10

            side_length = l.get_length()

            square_surface = side_length**2
            sum_surface += square_surface

            square = Square(side_length=side_length, color=BLUE, fill_color=BLUE).set_opacity(0.8)
            line_start = l.get_start()
            square.move_to(line_start +3*RIGHT+3*DOWN) 
            squares.add(square)  
            self.play(ReplacementTransform(l, square))
        
        self.wait(1)

        # The sum of all the surfaces has been tracked and now we're gonna calculate the square root of it to set as the side lenght of the new squares
        side_length = math.sqrt(sum_surface)

        # Square with side length of the square root of the sum 
        squared_square = Square(side_length=side_length, color=BLUE, fill_color=BLUE).set_opacity(1)
        squared_square.move_to([26, -10, 0]) 

        self.play(FadeOut(dashed, vertical_line, labels))
        self.play(Transform(squares, squared_square), run_time=2)
        self.wait(1)       


class SD3(Scene):
    def construct(self):
        """
        This scene shows the standard deviation by first calculating the variance of the previously determined sum of total
        and then taking the square root of it.
        """

        # Add the original square to the screen
        squared_square = Square(side_length=4, color=BLUE, fill_color=BLUE).set_opacity(1)
        self.add(squared_square)

        # SD formula the one we are gonna work to in this scene. Put in the top right corner and stays there for the whole scene
        standard_deviation_formula = MathTex(r"s_y = \sqrt{s^2_y}").scale(0.7).move_to(3.5*UP + 5*RIGHT)
        self.play(Create(standard_deviation_formula))
        self.wait(1)

        # Step to get there is to first resolve the variance. Moved to underneath the SD formula
        variance_formula = MathTex(r"s^2_y = \frac{\sum_{i=1}^{n} (Y_i - \overline{Y})^2}{n - 1}").scale(0.7).next_to(standard_deviation_formula, DOWN)
        variance_formula.shift(LEFT*0.2)
        self.play(Create(variance_formula))
        self.wait(1)
        
        # Formula of the surface of the big square put underneath the square
        surface = MathTex(r"\sum_{i=1}^{i=n}(Y_i - \overline{Y}) = 3000").scale(0.7).next_to(squared_square, DOWN)
        self.play(Create(surface))
        self.wait(1)

        # The numbers we already have are gonna be filled in the formula. Created underneath the empty formula
        filled_variance = MathTex(r"s^2_y = \frac{3000^2}{8}").scale(0.7).next_to(variance_formula, DOWN)
        self.play(Create(filled_variance))

        # To split the square in 8 smalller squares we first need to create a vgroup where the mobjects can be stored
        squares = VGroup()

        # Loop to create 8 squares and positioning them such that all are visible. To then add them to the vgroup
        for s in range(8):
            square = Square(side_length=1, color=BLUE, fill_color=BLUE).set_opacity(1)
            square.shift(LEFT * 4 + RIGHT * (s * 1.2))
            squares.add(square)

        # The transformation to 8 smaller squares while simulaniously fading out the big square
        self.play(ReplacementTransform(squared_square, squares), FadeOut(surface))
        self.wait(1)

        # All the squares except for the first mobject in the group are faded out. We only need one the rest is redundant
        self.play(*[FadeOut(square) for square in squares[1:]])
        self.wait(1)
        
        # For visibility the first square is moved to the right which is more the middle of the screen
        self.play(squares[0].animate.shift(3*RIGHT))
        self.wait(1)

        # Where filling in the variance underneath the other formulas on the right side of the screen
        variance = MathTex(r"s^2_y = 375").scale(0.7).next_to(filled_variance, DOWN)
        self.play(Create(variance))
        self.wait(1)

        # Now we're moving the variance underneath the square that is representing it as its surface
        self.play(variance.animate.next_to(squares[0], DOWN), FadeOut(filled_variance), FadeOut(variance_formula))
        self.wait(1)

        # Indicating of th original formula of the standard deviation to remind of what we're working towards
        self.play(Indicate(standard_deviation_formula, scale_factor=1.5, color=PURE_GREEN), run_time=2)

        # Copying the scare and moving it to the right.
        copy_square = squares[0].copy()
        self.play(TransformFromCopy(squares[0], copy_square))
        self.play(copy_square.animate.shift(RIGHT * 2))
        self.wait(1)

        # Then we'll create a line with the lenght of a side of the variance
        standard_deviation_line = Line(start=copy_square.get_bottom(), end=copy_square.get_bottom() + UP * copy_square.get_height(), color=BLUE)

        # Transform copy variance into the line where the line thus represents the standard deviation
        self.play(ReplacementTransform(copy_square, standard_deviation_line))
        self.wait(1)

        # Filling in the SD formula with the now gathered information
        filled_standard_deviation = MathTex(r"s_y = \sqrt{375}").scale(0.7).next_to(standard_deviation_formula, DOWN)
        self.play(Create(filled_standard_deviation))
        self.wait(1)

        # The final result of the standard deviation
        standard_deviation = MathTex(r"s_y = 19.36").scale(0.7).next_to(filled_standard_deviation, DOWN)
        self.play(Create(standard_deviation))
        self.play(standard_deviation.animate.next_to(standard_deviation_line, DOWN), FadeOut(filled_standard_deviation))
        self.wait(1)


# ToDo 
# - andere formules eerder erin zetten vanaf SD2



            



        


    
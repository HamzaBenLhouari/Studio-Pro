from manim import *

# manim -pql explain_circle_area.py ExplainCircleArea

class ExplainCircleArea(Scene):
    def construct(self):
        # Introduction
        intro_text = Text("Let's learn how to find the area of a circle!", font_size=48)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))
        
        # Drawing a circle
        circle = Circle(radius=2, color=BLUE)
        radius_line = Line(circle.get_center(), circle.get_right(), color=RED)
        radius_label = MathTex("r", color=RED).next_to(radius_line, UP)
        self.play(Create(circle))
        self.play(Create(radius_line), Write(radius_label))
        self.wait(1)

        # Introducing the formula
        formula_text = Text("The formula for the area of a circle is", font_size=36)
        formula = MathTex("A = \\pi r^2", font_size=48)
        formula_group = VGroup(formula_text, formula).arrange(DOWN)
        self.play(Write(formula_text))
        self.wait(1)
        self.play(Write(formula))
        self.wait(2)
        self.play(FadeOut(formula_text), formula.animate.to_edge(UP))

        # Explain each part of the formula
        pi_text = Text("Pi (π) is a special number", font_size=36).to_edge(LEFT)
        pi_value = MathTex("\\pi \\approx 3.14", font_size=48).next_to(pi_text, DOWN)
        self.play(Write(pi_text))
        self.play(Write(pi_value))
        self.wait(2)
        self.play(FadeOut(pi_text), FadeOut(pi_value))

        r_text = Text("r is the radius of the circle", font_size=36).to_edge(LEFT)
        r_explain = Text("The distance from the center to the edge", font_size=36).next_to(r_text, DOWN)
        self.play(Write(r_text))
        self.play(Write(r_explain))
        self.wait(2)
        self.play(FadeOut(r_text), FadeOut(r_explain))

        # Example calculation
        example = Text("Let's calculate the area for r = 3", font_size=36)
        r_value = MathTex("r = 3", font_size=48)
        example_group = VGroup(example, r_value).arrange(DOWN)
        self.play(Write(example))
        self.wait(1)
        self.play(Write(r_value))
        self.wait(2)
        self.play(FadeOut(example), FadeOut(r_value))

        calculation = MathTex("A = \\pi (3)^2", font_size=48)
        result = MathTex("A = 9\\pi \\approx 28.26", font_size=48).next_to(calculation, DOWN)
        self.play(Write(calculation))
        self.wait(1)
        self.play(Write(result))
        self.wait(2)

        # Conclusion
        conclusion = Text("So, the area of the circle is about 28.26 square units.", font_size=36)
        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(calculation), FadeOut(result), FadeOut(circle), FadeOut(radius_line), FadeOut(radius_label))

        # Ending text
        end_text = Text("And that's how you find the area of a circle!", font_size=48)
        self.play(Write(end_text))
        self.wait(2)
        self.play(FadeOut(end_text))

# To render the video, run the following in your terminal:
# manim -pql explain_circle_area.py ExplainCircleArea

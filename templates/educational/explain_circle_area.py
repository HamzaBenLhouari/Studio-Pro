from manim import *
from moviepy.editor import AudioFileClip
from elevenlabs import set_api_key,generate, play, save, voices, Voice, VoiceSettings

class ExplainSharpeRatio(Scene):
    def get_duration(self,file):
        return AudioFileClip(file).duration

    def generate_tts_audio(self, text, filename):
        # Replace this with actual API call logic to get the audio file
        api_key = "3cd04161eb64b39de66b5d198babc762"
        set_api_key(api_key)
        audio = generate(
                        text=text,
                        voice="Lily",
                        model="eleven_multilingual_v2"
                    )
        
        save(audio,filename)

    def construct(self):
        # Prepare and play background music (optional)
        # self.prepare_background_music("background.mp3", "bg_music_faded.mp3")
        # self.add_sound("bg_music_faded.mp3")

        # Explanation step 1: Introduction to the circle area
        intro_text = Text("Let's understand the area of a circle.", font_size=48).to_edge(UP)
        self.generate_tts_audio("Let's understand the area of a circle.", "intro.mp3")
        self.play(Write(intro_text))
        self.add_sound("intro.mp3")
        self.wait(self.get_duration("intro.mp3"))
        self.play(FadeOut(intro_text))

        # Step 2: Display the formula for the area
        formula_text = Text("The formula is:", font_size=36).to_edge(UP)
        formula = MathTex("A = \\pi r^2", font_size=48).next_to(formula_text, DOWN)
        self.generate_tts_audio("The formula is A equals pi r squared.", "formula.mp3")
        self.play(Write(formula_text), Write(formula))
        self.add_sound("formula.mp3")
        self.wait(self.get_duration("formula.mp3"))
        self.play(FadeOut(formula_text), FadeOut(formula))

        # Step 3: Explain the components of the formula
        explanation_text = Text("Where:", font_size=36).to_edge(UP)
        pi_text = Text("\\pi: A mathematical constant, approximately 3.14159.", font_size=24).next_to(explanation_text, DOWN)
        r_text = Text("r: The radius of the circle.", font_size=24).next_to(pi_text, DOWN)
        self.generate_tts_audio("Where pi is a mathematical constant approximately three point one four one five nine, and r is the radius of the circle.", "explanation.mp3")
        self.play(Write(explanation_text), Write(pi_text), Write(r_text))
        self.add_sound("explanation.mp3")
        self.wait(self.get_duration("explanation.mp3"))
        self.play(FadeOut(explanation_text), FadeOut(pi_text), FadeOut(r_text))

        # Step 4: Visualize a circle with its radius
        circle = Circle(radius=2, color=BLUE)
        radius_line = Line(circle.get_center(), circle.point_at_angle(PI / 4), color=RED)
        radius_label = MathTex("r", font_size=36).next_to(radius_line, RIGHT)
        self.generate_tts_audio("Here is a circle with its radius labeled as r.", "circle.mp3")
        self.play(Create(circle), Create(radius_line), Write(radius_label))
        self.add_sound("circle.mp3")
        self.wait(self.get_duration("circle.mp3"))

        # Step 5: Show the area filled
        area_label = Text("Area = \\pi r^2", font_size=36).to_edge(DOWN)
        self.generate_tts_audio("The shaded area represents pi r squared.", "area.mp3")
        self.play(Write(area_label))
        self.add_sound("area.mp3")
        self.wait(self.get_duration("area.mp3"))
        self.play(FadeOut(area_label), FadeOut(circle), FadeOut(radius_line), FadeOut(radius_label))

        # Step 6: Conclusion
        conclusion_text = Text("The area of a circle grows as the square of the radius.", font_size=36).to_edge(UP)
        self.generate_tts_audio("The area of a circle grows as the square of the radius.", "conclusion.mp3")
        self.play(Write(conclusion_text))
        self.add_sound("conclusion.mp3")
        self.wait(self.get_duration("conclusion.mp3"))
        self.play(FadeOut(conclusion_text))

        # Ending text
        end_text = Text("Now you understand the area of a circle!", font_size=48).to_edge(DOWN)
        self.generate_tts_audio("Now you understand the area of a circle!", "end.mp3")
        self.play(Write(end_text))
        self.add_sound("end.mp3")
        self.wait(self.get_duration("end.mp3"))
        self.play(FadeOut(end_text))

# To render the video, run the following in your terminal:
# manim -pql explain_circle_area.py ExplainCircleArea

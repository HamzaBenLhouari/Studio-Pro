from manim import *
from moviepy.editor import AudioFileClip, concatenate_audioclips
from elevenlabs import set_api_key, generate, save
from pydub import AudioSegment
import os

class ExplainSharpeRatio(Scene):

    def concate_audios(self, audios):
        clips = [AudioFileClip(c) for c in audios]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile("final_audio.mp3")

    def get_duration(self, file):
        return AudioFileClip(file).duration

    def generate_tts_audio(self, text, filename):
        api_key = "3cd04161eb64b39de66b5d198babc762"
        set_api_key(api_key)
        audio = generate(text=text, voice="Lily", model="eleven_multilingual_v2")
        save(audio, filename)

    def add_transition_audio(self, duration_ms):
        """Add a transition time (in milliseconds) between two audio clips"""
        silence = AudioSegment.silent(duration=duration_ms)
        silence.export("transition.mp3", format="mp3")
        return "transition.mp3"
    
    def remove_generated_files(self, file_list):
        """
        Remove the specified files from the file system.
        """
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed {file}")
            else:
                print(f"{file} not found, skipping.")

    def construct(self):
        audios = []
        transition_time_ms = 2200  # 2.2 second transition time between scenes
        
        # Scene 1: Introduction text
        intro_text = Text("Let's understand the area of a circle.", font_size=48).to_edge(UP)
        self.generate_tts_audio("Let's understand the area of a circle.", "intro.mp3")
        audios.append("intro.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Write(intro_text))
        self.wait(self.get_duration("intro.mp3"))
        self.play(FadeOut(intro_text))

        # Scene 2: Formula explanation
        formula_text = Text("The formula is:", font_size=36).to_edge(UP)
        formula = MathTex("A = \\pi r^2", font_size=48).next_to(formula_text, DOWN)
        self.generate_tts_audio("The formula is A equals pi r squared.", "formula.mp3")
        audios.append("formula.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Write(formula_text), Write(formula))
        self.wait(self.get_duration("formula.mp3"))
        self.play(FadeOut(formula_text), FadeOut(formula))

        # Scene 3: Explanation of the components
        explanation_text = Text("Where:", font_size=36).to_edge(UP)
        pi_text = Text("\\pi: A mathematical constant, approximately 3.14159.", font_size=24).next_to(explanation_text, DOWN)
        r_text = Text("r: The radius of the circle.", font_size=24).next_to(pi_text, DOWN)
        self.generate_tts_audio("Where pi is a mathematical constant approximately three point one four one five nine, and r is the radius of the circle.", "explanation.mp3")
        audios.append("explanation.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Write(explanation_text), Write(pi_text), Write(r_text))
        self.wait(self.get_duration("explanation.mp3"))
        self.play(FadeOut(explanation_text), FadeOut(pi_text), FadeOut(r_text))

        # Scene 4: Visualizing the circle
        circle = Circle(radius=2, color=BLUE)
        radius_line = Line(circle.get_center(), circle.point_at_angle(PI / 4), color=RED)
        radius_label = MathTex("r", font_size=36).next_to(radius_line, RIGHT)
        self.generate_tts_audio("Here is a circle with its radius labeled as r.", "circle.mp3")
        audios.append("circle.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Create(circle), Create(radius_line), Write(radius_label))
        self.wait(self.get_duration("circle.mp3"))

        # Scene 5: Showing the area
        area_label = Text("Area = \\pi r^2", font_size=36).to_edge(DOWN)
        self.generate_tts_audio("The shaded area represents pi r squared.", "area.mp3")
        audios.append("area.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Write(area_label))
        self.wait(self.get_duration("area.mp3"))
        self.play(FadeOut(area_label), FadeOut(circle), FadeOut(radius_line), FadeOut(radius_label))

        # Scene 6: Conclusion
        conclusion_text = Text("The area of a circle grows as the square of the radius.", font_size=36).to_edge(UP)
        self.generate_tts_audio("The area of a circle grows as the square of the radius.", "conclusion.mp3")
        audios.append("conclusion.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Write(conclusion_text))
        self.wait(self.get_duration("conclusion.mp3"))
        self.play(FadeOut(conclusion_text))

        # Final Scene: Ending text
        end_text = Text("Now you understand the area of a circle!", font_size=48).to_edge(DOWN)
        self.generate_tts_audio("Now you understand the area of a circle!", "end.mp3")
        audios.append("end.mp3")
        audios.append(self.add_transition_audio(transition_time_ms))  # Add transition time
        self.play(Write(end_text))
        self.wait(self.get_duration("end.mp3"))
        self.play(FadeOut(end_text))

        # Concatenate all audio clips
        self.concate_audios(audios)

        # Remove generated audio files after rendering
        self.remove_generated_files(audios)
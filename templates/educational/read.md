# Head over to an AI like ChatGPT or Copilot , ...

past this prompt and don't forget to change the TOPIC by another one interrests you

# Global Prompt

Create a Manim script that explains the topic: [TOPIC]. The script should follow these steps:

1. Introduction: Briefly introduce the topic.
2. Key Concepts: Explain the key concepts involved in the topic.
3. Example: Provide an example to illustrate the topic.
4. Conclusion: Summarize the explanation.

Ensure the script uses engaging animations and visual elements suitable for a child. Use the following placeholders:

- [INTRO_TEXT]: Introduction text for the topic.
- [CONCEPT_TEXT]: Text explaining the key concepts.
- [EXAMPLE_TEXT]: Text describing the example.
- [CONCLUSION_TEXT]: Conclusion text summarizing the topic.

# Example Prompt

Create a Manim script that explains the topic: "The Area of a Rectangle". The script should follow these steps:

1. Introduction: Briefly introduce the topic.
2. Key Concepts: Explain the key concepts involved in the topic.
3. Example: Provide an example to illustrate the topic.
4. Conclusion: Summarize the explanation.

Ensure the script uses engaging animations and visual elements suitable for a child. Use the following placeholders:

- [INTRO_TEXT]: "Let's learn how to find the area of a rectangle!"
- [CONCEPT_TEXT]: "The area of a rectangle is found by multiplying the length by the width."
- [EXAMPLE_TEXT]: "Let's calculate the area of a rectangle with a length of 5 units and a width of 3 units."
- [CONCLUSION_TEXT]: "So, the area of the rectangle is 15 square units.

#

Get-AppxPackage _Clipchamp_ | Remove-AppxPackage
Get-AppXPackage _Microsoft.ScreenSketch_ -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register “$($\_.InstallLocation)\AppXManifest.xml”}

# To render the video, run the following in your terminal:

- this will generate a low version (l:low,m:medium,h:high)
  manim -pql explain_circle_area.py ExplainCircleArea
  manim -pqm explain_circle_area.py ExplainCircleArea
  manim -pqh explain_circle_area.py ExplainCircleArea

# Perfect Prompt for Similar Scripts :

- You can use the explain_cercle_area scripts as a template to create another one based on it.

"Create a Python script using the Manim library that visually explains [concept, e.g., the area of a circle]. The script should include text animations synchronized with TTS-generated audio using an API. Each text should be displayed clearly, without overlapping with others, and the audio should play in sync with the displayed text. Ensure that each audio clip is played fully before moving on to the next part of the animation. Add a function that removes all generated audio files after the video is rendered, keeping only the final video output."

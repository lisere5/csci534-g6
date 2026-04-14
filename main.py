import os
import threading

from capture_audio import record_wav
from capture_video import record_video_features
from features_audio import transcribe, audio_confusion_features
from confusion import confusion_score, is_confused

try:
    from tts import speak
except ImportError:
    def speak(text: str):
        print(f"\nTutor: {text}")


LESSON = [
    """On the 6th of November of 1985 the Supreme Court of Colombia, otherwise known as the Palace of Justice, was overrun by a faction of rebels at approximately 11:35 in the morning. The rebels belonged to a guerilla group more formally known as M-19, short for the 19th of April Movement. At the time, Colombia’s president was Belisario Betancur, a proud member of Colombia’s Conservative Party.""",

    """The event was sparked due to the creation of the National Front, a treatise sparked between the respective Liberal and Conservative parties of Colombia to band together and alternate presidency amongst their parties. The joint front was promoted as a means of establishing peace after La Violencia, a ten year civil war in Colombia that claimed over 200,000 lives from 1948 to 1958.""",

    """While the National Front formally began in 1958, it was the Colombian presidential election of 1970 that ignited M-19’s rebellion. At this point in Colombian history, the National Front had gained a lot of ire from Colombians as they felt stripped of their political autonomy with little political improvements to show for it. Many Colombians thus felt that a shift from the National Front was necessary, choosing to vote for this hope in the form of leftist ex-president Gustavo Rojas Pinilla, a candidate from the new party known as la Alianza Nacional Popular.""",

    """Pinilla thus went head to head with the National Front’s conservative candidate, Misael Pastrana Borrero. The vote was incredibly close, but the government concluded that Borrero won the campaign by a mere 2,000 votes. While the government was firm in their results, not all parties were in agreement. Several radio stations and newspapers ran reports stating that Pinilla was the rightful winner the day after the election, leading to mass outcry from Colombian citizens who felt the election was stolen.""",

    """The M-19 thus formed in response to the government’s mishandling of the election by a majority of college-age citizens vowing to take the president to trial for his involvement. They thus stormed the Palace of Justice and took a plethora of hostages, some of which were officials incredibly high up in the government. One of the most notable, Alfonso Reyes Echandia, was the Chief Justice of the Supreme Court. Echandia attempted to initiate communications with President Betancur to negotiate a ceasefire, but the President entirely refused to answer his calls and chose to instead lead a brutal assault on the Palace of Justice.""",

    """Tanks and special military units were sent in to take the Palace of Justice back from M-19, yet they were entirely unprepared for the crisis. Helicopters came in with soldiers ready to storm the premises yet were not even given the rope necessary to safely rappel to the building, forcing them to instead jump which led to several injuries. The tanks that came to quell the situation were instead one of the very reasons the Palace of Justice was burnt to ash, leaving over 98 victims dead.""",

    """Although the event was one that demanded international importance, it was heavily covered up by the media. While several reporters were live on the scene relaying updates, the head of the Ministry of Communications, Noemi Sanin, chose to put news transmissions on pause to instead prioritize the airing of a local soccer game. Many citizens viewed this as an act of censorship as no news stations were thus allowed to air updates, sparking further outcry.""",

    """The event now lives in infamy as one of the darkest moments in Colombian history, only further cemented in its position due to the government’s power."""
]

CHECK_QUESTIONS = [
    "Who overran the Palace of Justice, and when did it happen?",
    "What was the National Front, and why was it created?",
    "Why did many Colombians become frustrated with the National Front?",
    "Why was the 1970 election considered controversial?",
    "Who was Alfonso Reyes Echandia, and what happened when he tried to negotiate?",
    "How did the military response contribute to the destruction and deaths?",
    "Why did many people view the media response as censorship?",
    "Why is this event remembered as such a dark moment in Colombian history?",
]


def adapt_text(original: str, user_response: str = "") -> str:
    first_sentence = original.split(".")[0].strip() + "."
    response_part = f'You said: "{user_response}". ' if user_response else ""

    return (
        "No worries, let me explain that more simply. "
        f"{response_part}"
        f"The main idea is: {first_sentence} "
        "Focus on the cause of the event, what happened, and why it mattered."
    )


def capture_multimodal_response(audio_path: str, seconds: float = 10.0):
    results = {
        "audio_path": None,
        "eye_features": None,
        "audio_error": None,
        "video_error": None,
    }

    def audio_worker():
        try:
            results["audio_path"] = record_wav(audio_path, seconds=seconds)
        except Exception as e:
            results["audio_error"] = str(e)

    def video_worker():
        try:
            results["eye_features"] = record_video_features(seconds=seconds)
        except Exception as e:
            results["video_error"] = str(e)

    t_audio = threading.Thread(target=audio_worker)
    t_video = threading.Thread(target=video_worker)

    t_audio.start()
    t_video.start()

    t_audio.join()
    t_video.join()

    return results


def run():
    os.makedirs("data/sessions", exist_ok=True)

    speak("Welcome. You will learn about the Palace of Justice siege in Colombia.")
    speak("After each paragraph, please say whether it makes sense and explain what you understood.")

    for i, paragraph in enumerate(LESSON, start=1):
        print("\n" + "=" * 80)
        print(f"PARAGRAPH {i}/{len(LESSON)}")
        print(paragraph)

        speak(f"Paragraph {i}.")
        speak(paragraph)

        understood = False
        attempts = 0
        max_attempts = 2

        while not understood and attempts < max_attempts:
            prompt_text = (
                "Does that make sense? Please answer yes or no, then explain what you understood in your own words."
            )
            print("\nTutor:", prompt_text)
            speak(prompt_text)
            print("Recording audio and eye tracking for 10 seconds...")

            audio_path = f"data/sessions/resp_{i}_{attempts}.wav"
            capture_results = capture_multimodal_response(audio_path, seconds=10.0)

            if capture_results["audio_error"]:
                print("Audio capture error:", capture_results["audio_error"])
                break

            if capture_results["video_error"]:
                print("Video capture error:", capture_results["video_error"])
                break

            eye = capture_results["eye_features"]
            wav_path = capture_results["audio_path"]

            wres = transcribe(wav_path)
            aud = audio_confusion_features(wres)
            score = confusion_score(aud, eye)

            print("\n--- RESULTS ---")
            print("Transcript:", aud["transcript"])
            print("Audio features:", aud)
            print("Eye features:", eye)
            print("Confusion score:", round(score, 3))

            if is_confused(score):
                attempts += 1
                speak("I think that may have been confusing.")
                simplified = adapt_text(paragraph, aud["transcript"])
                print("\n[ADAPT]", simplified)
                speak(simplified)

                if attempts < max_attempts:
                    speak("Let’s try that again.")
                else:
                    speak("We will move on for now and come back to the big idea in the next section.")
            else:
                understood = True
                question = CHECK_QUESTIONS[i - 1]
                print("\n[OK] Understanding seems sufficient.")
                print("Check question:", question)
                speak("Great. Here is a quick check question.")
                speak(question)

        print("\nEnd of paragraph", i)

    speak("Lesson complete. Thank you for participating.")


if __name__ == "__main__":
    run()

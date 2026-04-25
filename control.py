import os
import threading

try:
    from chatbot.tts import speak
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

def run():

    print("Welcome. You will learn about the Palace of Justice siege in Colombia.")
    speak("Welcome. You will learn about the Palace of Justice siege in Colombia.")

    for i, paragraph in enumerate(LESSON, start=1):
        print("\n" + "=" * 80)
        print(f"PARAGRAPH {i}/{len(LESSON)}")
        print(paragraph)

        speak(f"Paragraph {i}. {paragraph}")

        print("\nEnd of paragraph", i)

    speak("Lesson complete. Thank you for participating.")


run()
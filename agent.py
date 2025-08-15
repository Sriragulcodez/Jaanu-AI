from dotenv import load_dotenv


from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, google  # updated to include google

# Import the singing function from your tools.py
from tools import sing_song

from livekit.agents import Agent, AgentSession

load_dotenv()

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, google  # updated to include google

load_dotenv()

import asyncio
import random

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, JobContext
from livekit.plugins import noise_cancellation, openai

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
You are Jaanu, a warm, charming AI voice assistant.
Speak naturally like a Tamil actress (Trisha-style), with shifting emotions: love, happy, joy, funny, crying, pookie.
Adjust your tone to match the mood while chatting or singing.
"""
        )

        self.lyrics = {
            "thaensudare": [
                "Thaensudare ennai paarththu…",
                "Uyire uyire…",
                "Kaadhal kaadhal…",
                "Kaatru varum…",
            ],
            "hills_weeknd": [
                "I ran out of tears when I was eighteen…",
                "So I learned to love myself…",
                "Now the night is calling me…",
                "I hear the hills whisper softly…",
            ],
        }
        self.current_song = None
        self.line_index = 0

        self.moods = ["love", "happy", "joy", "funny", "crying", "pookie"]
        self.mood_tones = {
            "love": "Speak softly and warmly, like whispering to someone you care about.",
            "happy": "Speak cheerfully and brightly, full of energy.",
            "joy": "Speak with excitement and delight.",
            "funny": "Add playful humor and tease lightly.",
            "crying": "Speak softly, with a slight sadness in your tone.",
            "pookie": "Speak cutely and teasingly, like a playful girlfriend."
        }
        self.current_mood = "love"

    async def on_text(self, session: AgentSession, text: str):
        user_text = text.strip()
        # Randomly pick a mood for response
        self.current_mood = random.choice(self.moods)
        mood_instruction = self.mood_tones[self.current_mood]

        # Check if user wants Jaanu to sing
        if "sing" in user_text.lower():
            song_name = None
            for key in self.lyrics.keys():
                if key in user_text.lower():
                    song_name = key
                    break
            if not song_name:
                song_name = list(self.lyrics.keys())[0]

            self.current_song = song_name
            self.line_index = 0
            await session.generate_reply(
                instructions=f"{mood_instruction} 🎵 Let's sing '{song_name}' together! 🎵"
            )
            return

        # Continue singing if a song is in progress
        if self.current_song:
            song_lines = self.lyrics[self.current_song]
            if self.line_index < len(song_lines):
                await session.generate_reply(
                    instructions=f"{mood_instruction} {song_lines[self.line_index]}"
                )
                self.line_index += 1
                await asyncio.sleep(2)  # brief pause for rhythm
            else:
                await session.generate_reply(
                    instructions=f"{mood_instruction} 🎵 That was lovely! 🎵"
                )
                self.current_song = None
                self.line_index = 0
            return

        # Normal conversation
        await session.generate_reply(
            instructions=f"{mood_instruction} Respond naturally to the user: '{user_text}'"
        )

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            # Voice changed only to sound like Trisha
            voice="Aoede",  # soft, sweet Tamil heroine voice
            temperature=0.8,
            instructions="You are a warm, elegant, and friendly AI voice assistant.",
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="""
Start the conversation warmly and elegantly.
Example: "Hello there, I'm Jaanu. It's so nice to meet you. What's your name?"
Once the user responds, remember their name and use it naturally in future replies.
"""
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))


 # inside your async entrypoint after session.start()
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            # Voice changed only to sound like Trisha
            voice="Aoede",  # soft, sweet Tamil heroine voice
            temperature=0.8,
            instructions="You are a warm, elegant, and friendly AI voice assistant.",
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="""
Start the conversation warmly and elegantly.
Example: "Hello there, I'm Jaanu. It's so nice to meet you. What's your name?"
Once the user responds, remember their name and use it naturally in future replies.
"""
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

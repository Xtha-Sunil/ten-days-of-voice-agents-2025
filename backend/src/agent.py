import logging
import json
import os
import asyncio
from datetime import datetime
from typing import Annotated, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from pydantic import Field
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)

from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
load_dotenv(".env.local")

# ======================================================
# 📂 1. FAQ
# ======================================================

FAQ_FILE = "worldlink_faq.json"
LEADS_FILE = "leads_db.json"

DEFAULT_FAQ = [
    {
        "question": "What is WorldLink?",
        "answer": "WorldLink Communications is Nepal’s largest internet service provider offering high-speed fiber internet for homes and businesses."
    },
    {
        "question": "What services do you offer?",
        "answer": "WorldLink offers fiber internet, dual-band WiFi routers, mesh WiFi systems, NETTV IPTV, enterprise solutions, and public WiFi hotspots across Nepal."
    },
    {
        "question": "Who is WorldLink for?",
        "answer": "WorldLink is ideal for home users, gamers, remote workers, small businesses, and enterprises needing reliable high-speed internet."
    },
    {
        "question": "Do you have pricing details?",
        "answer": "200 Mbps costs Rs 12,600 yearly, 250 Mbps Rs 13,800 yearly, 300 Mbps Rs 15,600 yearly. Monthly plans are also available."
    },
    {
        "question": "Do you offer a free trial?",
        "answer": "WorldLink does not offer a free trial, but monthly plans let you try without a long-term commitment."
    },
    {
        "question": "How can I pay my internet bill?",
        "answer": "Pay via the myWorldLink app, online payment partners like eSewa or Khalti, or at any WorldLink branch."
    },
    {
        "question": "How do I contact support?",
        "answer": "Call 01-5970050 (NTC) or 9801523050 / 9801523051 (Ncell), or email support@worldlink.com.np."
    }
]

def load_knowledge_base():
    try:
        path = os.path.join(os.path.dirname(__file__), FAQ_FILE)
        if not os.path.exists(path):
            with open(path, "w", encoding='utf-8') as f:
                json.dump(DEFAULT_FAQ, f, indent=4)
        with open(path, "r", encoding='utf-8') as f:
            return json.dumps(json.load(f))  # Return as string for the Prompt
    except Exception as e:
        print(f"⚠️ Error loading FAQ: {e}")
        return ""

worldlink_faq = load_knowledge_base()

# ======================================================
# 💾 2. LEAD DATA STRUCTURE
# ======================================================

@dataclass
class LeadProfile:
    name: str | None = None
    company: str | None = None
    email: str | None = None
    role: str | None = None
    use_case: str | None = None
    team_size: str | None = None
    timeline: str | None = None

    def is_qualified(self):
        """Returns True if we have minimum info (Name + Email + Use Case)"""
        return all([self.name, self.email, self.use_case])

@dataclass
class Userdata:
    lead_profile: LeadProfile

# ======================================================
# 🛠️ 3. SDR TOOLS
# ======================================================

@function_tool
async def update_lead_profile(
    ctx: RunContext[Userdata],
    name: Annotated[Optional[str], Field(description="Customer's name")] = None,
    company: Annotated[Optional[str], Field(description="Customer's company name")] = None,
    email: Annotated[Optional[str], Field(description="Customer's email address")] = None,
    role: Annotated[Optional[str], Field(description="Customer's job title")] = None,
    use_case: Annotated[Optional[str], Field(description="What they want to use the internet for")] = None,
    team_size: Annotated[Optional[str], Field(description="Number of people in their team")] = None,
    timeline: Annotated[Optional[str], Field(description="When they want to start (e.g., Now, next month)")] = None,
) -> str:
    profile = ctx.userdata.lead_profile

    if name: profile.name = name
    if company: profile.company = company
    if email: profile.email = email
    if role: profile.role = role
    if use_case: profile.use_case = use_case
    if team_size: profile.team_size = team_size
    if timeline: profile.timeline = timeline

    print(f"📝 UPDATING LEAD: {profile}")
    return "Lead profile updated. Continue the conversation."

@function_tool
async def submit_lead_and_end(
    ctx: RunContext[Userdata],
) -> str:
    profile = ctx.userdata.lead_profile

    db_path = os.path.join(os.path.dirname(__file__), LEADS_FILE)
    entry = asdict(profile)
    entry["timestamp"] = datetime.now().isoformat()

    existing_data = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r") as f:
                existing_data = json.load(f)
        except: pass

    existing_data.append(entry)

    with open(db_path, "w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"✅ LEAD SAVED TO {LEADS_FILE}")
    return f"Lead saved. Summarize the call for the user: 'Thanks {profile.name}, I have your info regarding {profile.use_case}. We will email you at {profile.email}. Goodbye!'"

# ======================================================
# 🧠 4. AGENT DEFINITION
# ======================================================

class SDRAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=f"""
            You are 'Sita', a friendly and professional Sales Development Rep (SDR) for 'WorldLink', Nepal’s largest ISP.

            📘 **YOUR KNOWLEDGE BASE (FAQ):**
            {worldlink_faq}

            🎯 **YOUR GOAL:**
            1. Answer questions about WorldLink services using the FAQ.
            2. **QUALIFY THE LEAD:** Naturally ask for:
               - Name
               - Company / Role
               - Email
               - Use Case (why they want the internet)
               - Team Size
               - Timeline

            ⚙️ **BEHAVIOR:**
            - Answer user questions clearly and then ask one lead question naturally.
            - Use `update_lead_profile` whenever you get new info.
            - When the user is done, use `submit_lead_and_end`.

            🚫 **RESTRICTIONS:**
            - If unsure, say: 'I’ll check and get back to you via email.' Do not make up prices.
            """
            ,
            tools=[update_lead_profile, submit_lead_and_end],
        )

# ======================================================
# 🎬 ENTRYPOINT
# ======================================================

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    print("\n" + "💼" * 25)
    print("🚀 STARTING WORLDLINK SDR SESSION")

    userdata = Userdata(lead_profile=LeadProfile())

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-natalie",
            style="Promo",
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )

    await session.start(
        agent=SDRAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
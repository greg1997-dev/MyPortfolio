__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
import re
from google import genai
import os
import requests


STAPLE_LIST = [
    "Accesscode Talker", "Anti-Spell Fragrance", "Artifact Lancea",
    "Ash Blossom & Joyous Spring", "Beyond the Pendulum", "Book of Moon",
    "Bystial Druiswurm", "Bystial Magnamhut", "Called by the Grave",
    "Change of Heart", "Chaos Angel", "Cosmic Cyclone",
    "Crossout Designator", "D.D. Crow", "Dark Hole",
    "Dark Ruler No More", "Destructive Daruma Karma Cannon",
    "Dimension Shifter", "Dimensional Fissure", "Dinowrestler Pankratops",
    "Divine Arsenal AA-ZEUS - Sky Thunder", "Dogmatika Punishment",
    "Dominus Impulse", "Droll & Lock Bird", "Effect Veiler",
    "Elder Entity N'tss", "Emergency Teleport", "Enemy Controller",
    "Evenly Matched", "Exceed the Pendulum", "Fantastical Dragon Phantazmay",
    "Foolish Burial", "Foolish Burial Goods", "Forbidden Chalice",
    "Forbidden Droplet", "Garura, Wings of Resonant Life",
    "Ghost Belle & Haunted Mansion", "Ghost Mourner & Moonlit Chill",
    "Ghost Ogre & Snow Rabbit", "Gozen Match", "Gold Sarcophagus",
    "Harpie's Feather Duster", "I:P Masquerena", "Infinite Impermanence",
    "Instant Fusion", "Kashtira Fenrir", "Knightmare Phoenix",
    "Knightmare Unicorn", "Kurikara Divincarnate", "Lava Golem",
    "Lightning Storm", "Lost Wind", "Macro Cosmos", "Monster Reborn",
    "Mudragon of the Swamp", "Mulcharmy Fuwalos", "Mulcharmy Purulia",
    "Necrovalley", "One for One", "Pot of Avarice", "Pot of Desires",
    "Pot of Duality", "Raigeki", "Reinforcement of the Army",
    "Rivalry of Warlords", "S:P Little Knight", "Salamangreat Almiraj",
    "Set Rotation", "Skill Drain", "Super Starslayer TY-PHON - Sky Crisis",
    "There Can Be Only One", "Titanocider", "Torrential Tribute",
    "Trap Trick", "Underworld Goddess of the Closed World",
    "Upstart Goblin", "Zombie World"
]

base_path = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(base_path, "yugioh_db")

def get_card_id(card_name):
    """Fetch card ID from YGOPRODeck API"""
    try:
        url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card_name}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['data'][0]['id']
    except:
        return 89631139
    return None

@st.cache_resource
def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

client_db = get_chroma_client()

collection = client_db.get_collection(name="yugioh_master_collection") 

# UI & LLM LOGIC
st.title("Deck Doctor RAG")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai_client = genai.Client(api_key=api_key)
    archetype = st.text_input("Enter Archetype", "Snake-Eye")
    engine_context = st.text_input("Enter any engine you would like to add.", "Codebreaker")
    
    if st.button("Generate Deck"):
        with st.spinner("Searching database and consulting AI..."):
            # 1. RAG SEARCH
            search_query = f"Competitive {archetype} deck lists using {engine_context} for 2026 meta."
            results = collection.query(
                query_texts=[search_query],
                n_results=56
            )

            # 2. DATA PREP
            retrieved_knowledge = "\n".join(results['documents'][0])
            
            # 3. PROMPT GENERATION
            prompt = f"""
                You are an expert Yu-Gi-Oh! Deck Building Assistant.
                Build a competitive {archetype} deck list.

                KNOWLEDGE BASE: {retrieved_knowledge}
                CORE ENGINE: {engine_context}
                STAPLE OPTIONS: {STAPLE_LIST}

                INSTRUCTIONS:
                1. Use the KNOWLEDGE BASE to identify the most modern/powerful cards for {archetype}.
                2. MANDATORY: The Main Deck must contain at least 15-20 MONSTER cards.
                3. Ensure the deck follows the 2026 legality (no banned cards) and take into consideration the limited and semi-limited cards.
                4. Identify the core 25-30 cards.
                5. Fill the remaining slots with STAPLE OPTIONS.
                6. List potential weaknesses and propose a 15 card side deck with cards that can compliment the deck or be substitutes for cards in case they're facing a certain archetype.
                7. MANDATORY: Format the decklist as 'Quantityx Card Name' (e.g., 3x Ash Blossom & Joyous Spring).
            """
            
            response = genai_client.models.generate_content(model="gemini-3.1-flash-lite-preview", contents=prompt)
            
            # 4. DISPLAY
            st.markdown(response.text)
            
            # 5. SIDEBAR IMAGES
            st.sidebar.header("Visual Decklist")
            extracted = re.findall(r'\d+x\s+(.+?)(?=\n|$)', response.text)
            card_names = list(set([name.strip() for name in extracted]))
            st.write(f"Found cards: {card_names}")
            for card_name in card_names:
                card_id = get_card_id(card_name.strip())
                if card_id:
                    st.sidebar.image(f"https://images.ygoprodeck.com/images/cards/{card_id}.jpg",caption=card_name)
                    #st.sidebar.image(f"https://images.ygoprodeck.com/images/cards/{card_id}.jpg", caption=f"ID: {card_id}")
else:
    st.info("Please enter your Gemini API key in the sidebar to begin.")

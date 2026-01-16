# --- STEP 1: FIX SQLITE FOR STREAMLIT CLOUD ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
import re
from google import genai


STAPLE_LIST = [
    "Accesscode Talker [ID: 86066372]", "Anti-Spell Fragrance [ID: 58921041]", 
    "Artifact Lancea [ID: 34267776]", "Ash Blossom & Joyous Spring [ID: 14558127]", 
    "Beyond the Pendulum [ID: 71203602]", "Book of Moon [ID: 14087893]", 
    "Bystial Druiswurm [ID: 61019661]", "Bystial Magnamhut [ID: 14138100]", 
    "Called by the Grave [ID: 24224830]", "Change of Heart [ID: 04031928]", 
    "Chaos Angel [ID: 61405143]", "Cosmic Cyclone [ID: 82671409]", 
    "Crossout Designator [ID: 65681983]", "D.D. Crow [ID: 24508238]", 
    "Dark Hole [ID: 53129443]", "Dark Ruler No More [ID: 90307480]", 
    "Destructive Daruma Karma Cannon [ID: 46153721]", "Dimension Shifter [ID: 91800273]", 
    "Dimensional Fissure [ID: 81674782]", "Dinowrestler Pankratops [ID: 05501009]", 
    "Divine Arsenal AA-ZEUS - Sky Thunder [ID: 90448239]", "Dogmatika Punishment [ID: 35735125]", 
    "Dominus Impulse [ID: 82570001]", "Droll & Lock Bird [ID: 09414502]", 
    "Effect Veiler [ID: 97268402]", "Elder Entity N'tss [ID: 10389147]", 
    "Emergency Teleport [ID: 67723438]", "Enemy Controller [ID: 98139714]", 
    "Evenly Matched [ID: 15693423]", "Exceed the Pendulum [ID: 38851775]", 
    "Fantastical Dragon Phantazmay [ID: 98630720]", "Foolish Burial [ID: 81439173]", 
    "Foolish Burial Goods [ID: 28546905]", "Forbidden Chalice [ID: 25773167]", 
    "Forbidden Droplet [ID: 24299458]", "Garura, Wings of Resonant Life [ID: 11759235]", 
    "Ghost Belle & Haunted Mansion [ID: 73642296]", "Ghost Mourner & Moonlit Chill [ID: 52038441]", 
    "Ghost Ogre & Snow Rabbit [ID: 59438930]", "Gozen Match [ID: 53334471]", 
    "Gold Sarcophagus [ID: 75347539]", "Harpie's Feather Duster [ID: 18144506]", 
    "I:P Masquerena [ID: 65741786]", "Infinite Impermanence [ID: 10045474]", 
    "Instant Fusion [ID: 18452019]", "Kashtira Fenrir [ID: 32909498]", 
    "Knightmare Phoenix [ID: 02857333]", "Knightmare Unicorn [ID: 38342335]", 
    "Kurikara Divincarnate [ID: 45730592]", "Lava Golem [ID: 00102380]", 
    "Lightning Storm [ID: 14532163]", "Lost Wind [ID: 73488214]", 
    "Macro Cosmos [ID: 30243636]", "Monster Reborn [ID: 83764718]", 
    "Mudragon of the Swamp [ID: 40838625]", "Mulcharmy Fuwalos [ID: 26057213]", 
    "Mulcharmy Purulia [ID: 46845311]", "Necrovalley [ID: 47355498]", 
    "One for One [ID: 69931927]", "Pot of Avarice [ID: 55144522]", 
    "Pot of Desires [ID: 35261759]", "Pot of Duality [ID: 98645731]", 
    "Raigeki [ID: 12580477]", "Reinforcement of the Army [ID: 32807846]", 
    "Rivalry of Warlords [ID: 90840767]", "S:P Little Knight [ID: 29301450]", 
    "Salamangreat Almiraj [ID: 60303248]", "Set Rotation [ID: 58891075]", 
    "Skill Drain [ID: 82732705]", "Super Starslayer TY-PHON - Sky Crisis [ID: 36563630]", 
    "There Can Be Only One [ID: 61740673]", "Titanocider [ID: 15305141]", 
    "Torrential Tribute [ID: 53582587]", "Trap Trick [ID: 75434466]", 
    "Underworld Goddess of the Closed World [ID: 98127546]", "Upstart Goblin [ID: 70368879]", 
    "Zombie World [ID: 40642515]"
]

### DB Connectin
CHROMA_PATH = "./yugioh_db"

@st.cache_resource
def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

client_db = get_chroma_client()
# Make sure "ygo_cards" matches the name you gave your collection when you created it
collection = client_db.get_collection(name="ygo_cards") 

# --- STEP 3: UI & LLM LOGIC ---
st.title("Deck Doctor RAG")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai_client = genai.Client(api_key=api_key)
    archetype = st.text_input("Enter Archetype", "Snake-Eye")
    engine_context = st.text_input("Enter any engine you would like to add.", "Codebreaker")
    
    if st.button("Generate Deck"):
        with st.spinner("Searching database and consulting AI..."):
            # 1. RAG SEARCH
            search_query = f"Competitive {archetype} deck lists using {engine_context} for 2026 meta"
            results = collection.query(
                query_texts=[search_query],
                n_results=15 
            )

            # 2. DATA PREP (Now safely inside the button block)
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
                7. For every card, include its [ID: ########].
            """
            
            response = genai_client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            
            # 4. DISPLAY
            st.markdown(response.text)
            
            # 5. SIDEBAR IMAGES
            st.sidebar.header("Visual Decklist")
            ids = list(set(re.findall(r"\[ID: (\d+)\]", response.text)))
            for card_id in ids:
                st.sidebar.image(f"https://images.ygoprodeck.com/images/cards/{card_id}.jpg", caption=f"ID: {card_id}")
else:
    st.info("Please enter your Gemini API key in the sidebar to begin.")
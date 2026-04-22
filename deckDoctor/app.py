__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
import re
from google import genai
import os
import requests
import json
import glob

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
DATA_PATH = os.path.join(base_path, "yugioh_db")  # Folder where your JSON files are


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


def load_deck_data():
    """Load all JSON files from the data directory"""
    all_data = []
    json_files = glob.glob(os.path.join(DATA_PATH, "*.json"))

    if not json_files:
        st.error(f"No JSON files found in {DATA_PATH}")
        return []

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
        except Exception as e:
            st.warning(f"Error loading {json_file}: {e}")

    return all_data


@st.cache_resource
def initialize_database():
    """Initialize or rebuild the ChromaDB database from JSON files"""
    import shutil

    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)

        # Try to get existing collection
        try:
            collection = client.get_collection(name="yugioh_master_collection")

            # If collection exists but is empty or corrupted, rebuild
            if collection.count() == 0:
                raise Exception("Collection is empty, rebuilding...")

            return collection

        except Exception as e:
            # Collection doesn't exist or is corrupted - rebuild
            st.info(f"Building database from source files... ({str(e)})")

            # Delete corrupted database
            try:
                client.delete_collection(name="yugioh_master_collection")
            except:
                pass

            # Create fresh collection
            collection = client.create_collection(
                name="yugioh_master_collection",
                metadata={"hnsw:space": "cosine"}
            )

            # Load data from JSON files
            deck_data = load_deck_data()

            if not deck_data:
                st.error("No deck data found! Please check your JSON files.")
                st.stop()

            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []

            for idx, item in enumerate(deck_data):
                # Adjust these keys based on your JSON structure
                # Common formats: 'text', 'content', 'deck_list', etc.
                if isinstance(item, dict):
                    # Try common key names
                    text = item.get('text') or item.get('content') or item.get('deck_list') or str(item)
                    metadata = item.get('metadata', {})
                    item_id = item.get('id', f"deck_{idx}")
                else:
                    text = str(item)
                    metadata = {}
                    item_id = f"deck_{idx}"

                documents.append(text)
                metadatas.append(metadata)
                ids.append(str(item_id))

            # Add to collection in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                collection.add(
                    documents=documents[i:i + batch_size],
                    metadatas=metadatas[i:i + batch_size],
                    ids=ids[i:i + batch_size]
                )

            st.success(f"✅ Database built successfully with {len(documents)} deck entries!")
            return collection

    except Exception as e:
        st.error(f"Fatal database error: {e}")
        st.info("Try deleting the yugioh_db folder manually and restarting the app.")
        st.stop()


# Initialize database
collection = initialize_database()

# UI & LLM LOGIC
st.title("Deck Doctor RAG")

# Show database stats
st.sidebar.metric("Deck Entries in Database", collection.count())

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai_client = genai.Client(api_key=api_key)
    archetype = st.text_input("Enter Archetype", "Snake-Eye")
    engine_context = st.text_input("Enter any engine you would like to add.", "Codebreaker")

    if st.button("Generate Deck"):
        with st.spinner("Searching database and consulting AI..."):
            try:
                # 1. RAG SEARCH
                search_query = f"Competitive {archetype} deck lists using {engine_context} for 2026 meta."
                results = collection.query(
                    query_texts=[search_query],
                    n_results=min(56, collection.count())
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
                    7. MANDATORY: Format the decklist as 'Quantityx Card Name' (e.g., * 3x Ash Blossom & Joyous Spring). Do not add anything else on that line when listing the card. 
                """

                response = genai_client.models.generate_content(model="gemini-3.1-flash-lite-preview", contents=prompt)

                # 4. DISPLAY
                st.markdown(response.text)

                # 5. SIDEBAR IMAGES
                st.sidebar.header("Visual Decklist")
                extracted = re.findall(r'\d+x\s+(.+?)(?=\n|$)', response.text)
                card_names = list(set([name.strip() for name in extracted]))

                for card_name in card_names:
                    card_id = get_card_id(card_name.strip())
                    if card_id:
                        st.sidebar.image(
                            f"https://images.ygoprodeck.com/images/cards/{card_id}.jpg",
                            caption=card_name,
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"Error generating deck: {e}")

else:
    st.info("Please enter your Gemini API key in the sidebar to begin.")
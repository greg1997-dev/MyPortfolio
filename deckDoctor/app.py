__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
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
DATA_DIR = os.path.join(base_path, "yugioh_db")
COLLECTION_NAME = 'yugioh_master_collection'


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
def initialize_database():
    """Initialize or rebuild the ChromaDB database from JSON card data"""
    import shutil

    try:

        client = chromadb.PersistentClient(path=CHROMA_PATH)

        # Use the default embedding function (all-MiniLM-L6-v2)
        embedding_func = embedding_functions.DefaultEmbeddingFunction()

        # Try to get existing collection
        try:
            collection = client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=embedding_func
            )

            # If collection exists and has data, use it
            if collection.count() > 0:
                st.sidebar.success(f"✅ Database loaded: {collection.count()} cards")
                return collection
            else:
                # Collection exists but is empty - rebuild
                raise Exception("Collection is empty, rebuilding...")

        except Exception as e:
            # Collection doesn't exist or is corrupted - rebuild
            st.info(f"🔨 Building database from card data... ({str(e)})")

            # Delete old collection if it exists
            try:
                client.delete_collection(name=COLLECTION_NAME)
            except:
                pass

            # Create fresh collection
            collection = client.create_collection(
                name=COLLECTION_NAME,
                embedding_function=embedding_func,
                metadata={"hnsw:space": "cosine"}
            )

            # Get all JSON files
            json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))

            total_cards = 0
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Process each file
            for file_idx, file_path in enumerate(json_files):
                filename = os.path.basename(file_path)
                status_text.text(f"Indexing {filename}...")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cards = json.load(f)

                    # Handle both dict and list formats
                    if isinstance(cards, dict):
                        # If it's a dict with a 'data' key (YGOPRODeck API format)
                        cards = cards.get('data', [cards])
                    elif not isinstance(cards, list):
                        cards = [cards]

                    # Batch processing (ChromaDB limit is around 5k per add)
                    batch_size = 500
                    for i in range(0, len(cards), batch_size):
                        batch = cards[i: i + batch_size]

                        # Prepare data for this batch
                        ids = [str(c.get('id', f"{filename}_{i + j}")) for j, c in enumerate(batch)]

                        # Embed the card name + description for better search
                        documents = [
                            f"Name: {c.get('name', 'Unknown')}\nEffect: {c.get('desc', 'No description')}"
                            for c in batch
                        ]

                        # Metadata for filtering
                        metadatas = [{
                            "name": c.get("name", "Unknown"),
                            "type": c.get("type", "Unknown"),
                            "archetype": str(c.get("archetype", "None")),
                            "id": str(c.get("id", "")),
                            "file_source": filename
                        } for c in batch]

                        collection.add(
                            ids=ids,
                            documents=documents,
                            metadatas=metadatas
                        )

                        total_cards += len(batch)

                except Exception as e:
                    st.warning(f"⚠️ Error processing {filename}: {e}")

                # Update progress
                progress = (file_idx + 1) / len(json_files)
                progress_bar.progress(progress)

            progress_bar.empty()
            status_text.empty()
            st.success(f"✅ Database built successfully with {total_cards} cards!")

            return collection

    except Exception as e:
        st.error(f"❌ Fatal database error: {e}")
        st.info("Try deleting the yugioh_db folder manually and restarting the app.")
        st.stop()


# Initialize database
collection = initialize_database()

# UI & LLM LOGIC
st.title("🎴 Deck Doctor RAG")
st.caption("Yu-Gi-Oh! AI Deck Builder powered by RAG")

# Show database stats in sidebar
st.sidebar.header("📊 Database Info")
st.sidebar.metric("Total Cards", collection.count())

api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")

if api_key:
    genai_client = genai.Client(api_key=api_key)

    col1, col2 = st.columns(2)
    with col1:
        archetype = st.text_input("🎯 Enter Archetype", "Snake-Eye")
    with col2:
        engine_context = st.text_input("⚙️ Engine/Tech Cards", "Codebreaker")

    if st.button("🚀 Generate Deck", type="primary"):
        with st.spinner("🔍 Searching database and consulting AI..."):
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

                response = genai_client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview",
                    contents=prompt
                )

                # 4. DISPLAY
                st.markdown("### 📋 Generated Decklist")
                st.markdown(response.text)

                # 5. SIDEBAR IMAGES
                st.sidebar.header("🎴 Visual Decklist")
                extracted = re.findall(r'\d+x\s+(.+?)(?=\n|$)', response.text)
                card_names = list(set([name.strip() for name in extracted]))

                if card_names:
                    for card_name in card_names:
                        card_id = get_card_id(card_name.strip())
                        if card_id:
                            st.sidebar.image(
                                f"https://images.ygoprodeck.com/images/cards/{card_id}.jpg",
                                caption=card_name,
                                use_container_width=True
                            )
                else:
                    st.sidebar.warning("No cards extracted. Try a different archetype.")

            except Exception as e:
                st.error(f"❌ Error generating deck: {e}")
                st.info("Check your API key or try again.")

else:
    st.info("👈 Please enter your Gemini API key in the sidebar to begin.")
    st.markdown("""
    ### How to use:
    1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Enter the key in the sidebar
    3. Choose your archetype and any tech cards
    4. Click Generate Deck!
    5. Keys are not stored anywhere, so when you close the page it will not save it.
    """)

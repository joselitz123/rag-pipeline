import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:9000"

def test_ingest():
    print("Testing Ingestion...")
    # Create a dummy file
    with open("test_doc.md", "w") as f:
        f.write("""
        The boy was not sure what he was doing in the forest. He had been hiking for hours and thought he was at the edge of his endurance. The summer heat and humidity were oppressive and had left him feeling weak. He was seeking peace and quiet, a place to meditate and escape the distractions of his busy life. Maybe he was looking for treasure, but he did not know it. He was annoyed that his cell phone had no signal, but he was even more upset that his GPS had malfunctioned, and he had lost his way.
He thought he should be back at his vehicle by now. Unfortunately, he was not sure where he was, and he was becoming increasingly frustrated. He started to worry that he was lost. He was not worried about being eaten by wild animals. There were none in this part of the forest. He was, however, concerned that the sun would soon set and that he would become disoriented and lost at night.
He was feeling a bit less confident than he usually did when he was on a mountain hike. He had felt more at home in the rugged, beautiful surroundings of the Alps, but he was not sure that he had the endurance to blast his way out of this particular situation. He was happy to traverse the rugged trails of the mountains, but he was not convinced that he could battle his way out of this. He was grateful that he was a healthy man, but he was not sure that he had the strength to hike his way out of the jungle.
He wished he had been carrying more water, but he did not know how to ration the water he had. He thought he should try to find a stream or a pond, but he was not sure that any existed. He was a bit disheartened. He was also a bit tired and discouraged, and he was not sure how long he could continue to hike. He was not sure what he was going to do. He was not sure how he was going to get back home. He was not sure that he could hold out until morning. He was not sure he would survive. He was not sure.
He stopped walking and sighed. He realized that he was not sure about anything. He was not sure that he was going to make it out of the forest. He was not sure where he was. He was not sure that he was going to make it back to his vehicle. He was not sure how he was going to get water, or food, or shelter. He was not sure how he was going to survive. He was not even sure that he was going to live. He wished he had something to drink. He wished he had something to eat. He wished he had something to eat. He was not sure he was going to make it. He was not sure.
He was not sure. He did not know what to do. He did not know where to go. He did not know how to find his way out of the forest, but he was not sure that he could continue walking anyway. He did not want to die, but he was not sure that he could survive. He was not sure that he could find his way back home, but he was not sure that he could find his way out of the forest. He did not know what his options were. He did not know what to do. He did not know how to survive. He did not know how to get out of the forest. He did not know how to get home. He did not know what to do. He did not know anything. He was not sure.
He sat down on a fallen tree and looked up into the trees. He was feeling weak.""")
    
    files = {'file': open('test_doc.md', 'rb')}
    response = requests.post(f"{BASE_URL}/ingest", files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    os.remove("test_doc.md")

def test_chat():
    print("\nTesting Chat...")
    payload = {"query": "What is this document about?"}
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_ingest()
    test_chat()

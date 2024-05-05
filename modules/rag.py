import os
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone import ServerlessSpec
import time 
from openai import OpenAI

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def pinecone_client(PINECONE_API_KEY): 
    pc = Pinecone(api_key=PINECONE_API_KEY)
    spec = ServerlessSpec(
        cloud="aws", region="us-west-2"
    )
    

    pinecone_index_name = 'til'
    existing_pinecone_indexes = [
        pinecone_index_info["name"] for pinecone_index_info in pc.list_indexes()
    ]

    # check if pinecone_index already exists (it shouldn't if this is first time)
    if pinecone_index_name not in existing_pinecone_indexes:
        # if does not exist, create pinecone_index
        pc.create_index(
            pinecone_index_name,
            dimension=1536,  # dimensionality of voyage-2 embeddings
            metric='dotproduct',
            spec=spec
        )
        # wait for pinecone_index to be initialized
        while not pc.describe_index(pinecone_index_name).status['ready']:
            time.sleep(1)

    # connect to pinecone_index
    pinecone_index = pc.Index(pinecone_index_name)
    time.sleep(1)
    # view pinecone_index stats
    pinecone_index.describe_index_stats()    
    return pinecone_index 

pinecone_index = pinecone_client(PINECONE_API_KEY)

def get_embedding(message, openai_client, model):
   message = message.replace("\n", " ")   
   raw_response = openai_client.embeddings.create(input = [message], model=model)
#    print('raw_response',raw_response)
   embedding = raw_response.data[0].embedding
   return embedding


message_id = '1'
message = """
Feb 20 (Reuters) - The first human patient implanted with a brain-chip from Neuralink appears to have fully recovered and is able to control a computer mouse using their thoughts, the startup's founder Elon Musk said late on Monday.

"Progress is good, and the patient seems to have made a full recovery, with no ill effects that we are aware of. Patient is able to move a mouse around the screen by just thinking," Musk said in a Spaces event on social media platform X
"""
message_id2 ='2'
message2="""
Cultural homogenization is an aspect of cultural globalization and refers to the reduction in cultural diversity through the popularization and diffusion of a wide array of cultural symbols—not only physical objects but customs, ideas and values. David E. O'Connor defines it as "the process by which local cultures are transformed or absorbed by a dominant outside culture". Cultural homogenization has been called "perhaps the most widely discussed hallmark of global culture". In theory, homogenization could work in the breakdown of cultural barriers and the global adoption of a single culture.

thanks wikipedia. i imagine this can happen in multiple levels, including one starting from our little social friend groups
"""
message_id3='3'
message3="""
Man is the creature who does not know what to desire, and he turns to others in order to make up his mind. We desire what others desire because we imitate their desires."

The mimetic theory of desire, an explanation of human behavior and culture, originated with the French historian, literary critic, and philosopher of social science René Girard (1923–2015). The name of the theory derives from the philosophical concept mimesis, which carries a wide range of meanings. In mimetic theory, mimesis refers to human desire, which Girard thought was not linear but the product of a mimetic process in which people imitate models who endow objects with value

"""

def insert(message_id, message): 
    embed = get_embedding(message, openai_client, model="text-embedding-ada-002")
    print('created embedding')
    metadata = {'original':message}

    pinecone_index.upsert(vectors=[(message_id, embed, metadata)])
    print('pinecone_index upsert done')


def search(message_id, message):
    embed = get_embedding(message, openai_client, model="text-embedding-ada-002")
    print('created embedding')
    results = pinecone_index.query(
            vector=embed, top_k=2, include_metadata=True
        )
    recommendations = [match for match in results['matches'] if match['id'] != message_id]
    
    print('recommendation', recommendations)
    return recommendations


# insert(message_id3, message3, pinecone_index)
# search(message_id, message)


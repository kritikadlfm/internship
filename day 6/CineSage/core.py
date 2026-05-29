from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-2506")

response = model.invoke('''visually breathtaking and emotionally profound masterpiece, 
Interstellar blends hard science fiction with deeply human storytelling. 
Directed by Christopher Nolan, the film explores space travel, time dilation, 
, and survival with extraordinary ambition. The stunning cinematography, 
powerful soundtrack by Hans Zimmer, and heartfelt performances—especially by
Matthew McConaughey—make the experience unforgettable. While its scientific concepts 
may feel complex at times, the emotional core of a father trying to save both humanity 
and his daughter gives the movie remarkable depth and impact. Also Can you nplease extarct the summary and information of the movie''')

print(response.content)

'''Interstellar Review:'
A visually breathtaking and emotionally profound masterpiece, 
Interstellar blends hard science fiction with deeply human storytelling. 
Directed by Christopher Nolan, the film explores space travel, time dilation, 
, and survival with extraordinary ambition. The stunning cinematography, 
powerful soundtrack by Hans Zimmer, and heartfelt performances—especially by
Matthew McConaughey—make the experience unforgettable. While its scientific concepts 
may feel complex at times, the emotional core of a father trying to save both humanity 
and his daughter gives the movie remarkable depth and impact.'''

'''3 Idiots Review:
3 Idiots is an inspiring and entertaining film that brilliantly questions the 
pressure-driven education system. Directed by Rajkumar Hirani, the movie balances comedy, 
emotion, friendship, and social commentary with exceptional skill. Aamir Khan delivers a 
memorable performance as Rancho, a free-thinking student who challenges traditional learning 
methods and encourages curiosity over rote memorization. The film’s humor, emotional moments, 
and powerful life lessons resonate strongly with students and professionals alike, making it 
one of the most impactful Indian films ever made.
'''
'''The Shawshank Redemption Review:
The Shawshank Redemption is a timeless cinematic gem that beautifully portrays hope, resilience,
and friendship. Directed by Frank Darabont and based on a story by Stephen King, the film follows 
Andy Dufresne’s journey through injustice and survival inside a prison. The performances by
Tim Robbins and Morgan Freeman are deeply moving and authentic. Rather than relying on action or 
spectacle, the movie captivates viewers through emotional storytelling, meaningful dialogue, and a 
powerful message that hope can endure even in the darkest situations.
'''
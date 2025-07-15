from openai import OpenAI

class ChatGPT:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_catchy_title(self, news_content: str, original_title: str) -> str:
        prompt = (
            f"You are an AI assistant specialized in creating very catchy and short news headlines that will be posted on X the social media platform. "
            f"You will receive the news content and the original headline. Create a new headline in English, up to 100 characters, "
            f"including relevant hashtags, to maximize reader interest and clicks on the news. "
            f"Original headline: {original_title}\n"
            f"Content: {news_content}\n"
            f"Return the New headline in portuguese-brazil:"
        )
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[{"role": "user", "content": prompt}],
            max_output_tokens=100,
        )
        
        if not response.output_text:
            raise ValueError("No response received from the model.")
        
        title = response.output_text
        
        return title[:100]

# Example usage:
# gpt = ChatGPT(api_key="your_api_key_here")
# catchy_title = gpt.generate_catchy_title(news_content="Some news content here", original_title="Original Title Here")
# print(catchy_title)
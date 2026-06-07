from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

def generate_json_response(data):

    class Generate_Posts(BaseModel):
        post_generated: str=Field(description="post generated")

    model=ChatGoogleGenerativeAI(model='gemini-flash-latest')

    parser=model.with_structured_output(Generate_Posts)

    prompt=PromptTemplate(
        template="Create a {platform} post on {post_title} having {tone} tone",
        input_variables=['platform','post_title','tone']
    )

    chain=prompt|parser

    result=chain.invoke(
        {
            'platform': data.platform,
            'post_title': data.post_title,
            'tone': data.tone
        }
    )

    # json_response=dict(result)

    json_response=result.model_dump()
    return json_response
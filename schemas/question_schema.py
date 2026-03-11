from pydantic import BaseModel

class QuestionBase(BaseModel):
    question : str
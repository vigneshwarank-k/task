from fastapi import HTTPException, APIRouter
from graph.workflow import graph
from schemas.question_schema import QuestionBase

router = APIRouter()


@router.post("/chat")
def chat_agent(data: QuestionBase):
    try:
        question = data.question
        response = graph.invoke({"user_query": question})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

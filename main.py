from datetime import datetime
from typing import List
from typing import Optional
from typing import Set

import pandas as pd
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import Query
from pydantic import BaseModel

data = pd.read_csv("./questions.csv", delimiter=";")

users_db = {
    "aurelia": "augustina",
    "cassius": "cato",
    "admin": "admin",
}


class HealthStatusResponse(BaseModel):
    message: str


class Question(BaseModel):
    question: str
    subject: Set[str]
    use: Set[str]
    correct: Optional[Set[str]] = None
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str]
    remark: Optional[str] = None


class ResponseQuestionCreate(BaseModel):
    question: Question
    id: str
    created_at: str


class QuestionRequest(BaseModel):
    question: str
    subject: Set[str]
    use: Set[str]
    correct: Optional[Set[str]] = None
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str]
    remark: Optional[str] = None


class QuestionResponse(BaseModel):
    question: QuestionRequest
    id: str
    created_at: str


class QuestionResponseItem(BaseModel):
    question: str
    subject: Set[str]
    use: Set[str]
    correct: Optional[Set[str]] = None
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None
    remark: Optional[str] = None


class GetQuestionsResponse(BaseModel):
    questions: List[QuestionResponseItem]


app = FastAPI(
    title="API for creating questionnaires",
    description="API allows users to get MCQ, and admins to create new questions",
    version="0.0.1",
)


def verify_basic_auth(authorization: str = Header(...)):
    try:
        auth_type, auth_info = authorization.split()
        if auth_type.lower() != "basic":
            raise HTTPException(status_code=401, detail="Invalid authentication method")
        username, password = auth_info.split(":")
        if users_db.get(username) is None or users_db.get(username) != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/", name="Check the health status of the API.")
async def get_status():
    return HealthStatusResponse(message="healthy")


@app.get(
    "/questions",
    name="Get a random set of multiple-choice questions.",
    response_model=GetQuestionsResponse,
)
async def get_questions(
    current_user: str = Depends(verify_basic_auth),
    test_type: str = Query(
        ..., description="Choose a test type", enum=data.use.unique().tolist()
    ),
    categories: List[str] = Query(
        ...,
        description="Choose one or more categories",
        enum=data.subject.unique().tolist(),
        min_items=1,
    ),
    num_items: int = Query(
        ..., description="How many questions to get", enum=[5, 10, 20]
    ),
):

    if not categories or "" in categories:
        raise HTTPException(status_code=400, detail="Invalid categories")

    try:
        filtered_data = data[
            (data["subject"].isin(categories)) | (data["use"] == test_type)
        ]
        # pick randomly among the questions of type and belonging to categories
        filtered_data = filtered_data.sample(frac=1).reset_index(drop=True)
        num_samples_to_take = min(num_items, len(filtered_data))
        sampled_data = filtered_data.head(num_samples_to_take)
        sampled_data = sampled_data.fillna("")

        # Convert the DataFrame into a list of QuestionResponseItem instances
        questions_list = []
        for _, row in sampled_data.iterrows():
            question_item = QuestionResponseItem(
                question=row["question"],
                subject=set(row["subject"].split(",")),
                use=set(row["use"].split(",")),
                correct=set(row["correct"].split(",")) if row["correct"] else None,
                responseA=row["responseA"],
                responseB=row["responseB"],
                responseC=row["responseC"],
                responseD=row["responseD"] if "responseD" in row else None,
                remark=row["remark"] if "remark" in row else None,
            )
            questions_list.append(question_item)

        return GetQuestionsResponse(questions=questions_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


@app.post("/question", name="Create a new question", response_model=QuestionResponse)
async def create_question(
    current_user: str = Depends(verify_basic_auth), question: Question = None
):

    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    new_entry = question.dict()

    if new_entry.get("question") in data["question"].values:
        raise HTTPException(status_code=409, detail="Question already existing")

    # add new question to dataframe
    data.loc[len(data.index)] = new_entry
    a_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")

    return ResponseQuestionCreate(
        question=question, id=str(data.index[-1]), created_at=a_date
    )

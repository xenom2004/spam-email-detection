from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import json

pipe = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student", top_k=None)


class Input_Text(BaseModel):
    input_text: str

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def receive_text(item: Input_Text):
    inference_text = item.input_text
    data = pipe(inference_text)

    output = []
    max_score_entry = {'label':'', 'score':0}
    base_data = data[0].copy()
    for i in range(0, len(data[0])):
        for score in base_data:
            if max_score_entry['score']<score['score']:
                max_score_entry = score
                base_data.remove(score)
        output.append(max_score_entry)
        max_score_entry = {'label':'', 'score':0}

    output_dict = {}
    for i in range(0, len(output)):
        output_dict[i] = output[i]
        
    payload = json.dumps(output_dict)

    return payload

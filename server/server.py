import uvicorn
from typing import Optional, List, Annotated
from http import HTTPStatus
from fastapi import FastAPI, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from beyond_dnd import BeyondDnDClient

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

beyond = BeyondDnDClient()


@app.get('/characters')
def get_all_character_data(request: Request, char_ids: Optional[List[str]] = Query(None, nullable=True), force_update: bool = False):
    # Note: This would be simpler if the DnDBeyond API allowed for a get on campaign w/o auth. One ID, all characters.
    try:
        char_data = beyond.get_all_characters_data(char_ids=char_ids, force_update=force_update)
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return JSONResponse(content=char_data)


@app.get("/characters/{char_id}")
def get_character_data(request: Request, char_id: str, force_update: bool = False):
    try:
        char_data = beyond.get_one_characters_data(char_id=char_id, force_update=force_update)
        return JSONResponse(content=char_data)
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8998)

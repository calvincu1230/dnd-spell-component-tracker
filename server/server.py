import uvicorn
from typing import Optional, List, Annotated
from http import HTTPStatus
from fastapi import FastAPI, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from beyond_dnd import BeyondDnDClient, BeyondDnDAPIError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

beyond = BeyondDnDClient()


@app.exception_handler(RequestValidationError)
def testing_stuff(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for error in exc.errors():
        formatted_errors.append({
            "field": ".".join(map(str, error["loc"])),
            "message": error["msg"],
        })
    return JSONResponse(
        status_code=422,
        content={"errors": formatted_errors},
    )


@app.get('/characters')
def get_all_character_data(
        request: Request, char_ids: Optional[List[str]] = Query(None, nullable=True), force_update: bool = False
):
    # Note: This would be simpler if the DnDBeyond API allowed for a get on campaign w/o auth. One ID, all characters.
    try:
        char_data = beyond.get_all_characters_data(char_ids=char_ids, force_update=force_update)
    except BeyondDnDAPIError as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=e.status_code
        )
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
    except BeyondDnDAPIError as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.delete("/characters")
def delete_cached_data():
    try:
        beyond.delete_all_cached_character_data()
        return Response(status_code=HTTPStatus.ACCEPTED)
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.delete("/characters/{char_id}")
def delete_character_by_id(char_id: str):
    try:
        updated_data = beyond.delete_character_by_id(char_id)
        return JSONResponse(status_code=HTTPStatus.ACCEPTED, content=updated_data)
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


# Note: This must be committed as commented out, otherwise the executable file will run the server again after
#  stopping the bundled server
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8998)

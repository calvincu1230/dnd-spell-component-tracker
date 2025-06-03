import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from beyond_dnd import BeyondDnD

app = FastAPI()

beyond = BeyondDnD()


@app.get("/characters")
def get_all_character_data(request: Request, force_update: bool = False):
    char_ids = request.get('char_ids')
    char_data = beyond.get_bdnd_all_character_data(char_ids=char_ids, force_update=force_update)
    return JSONResponse(content=char_data)


@app.get("/characters/{char_id}")
def get_character_data(request: Request, char_id: str, force_update: bool = False):
    char_data = beyond.get_bdnd_all_character_data(char_ids=[char_id], update_one=True, force_update=force_update)
    return JSONResponse(content=char_data)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8998)

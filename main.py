from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.print import printReceipt

# run `uvicorn main:app --reload` to start the server

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# if there is a records.tsv file, read the last line and get the last i
# if not, set i to 0
try:
    with open("records.tsv", "r") as f:
        lines = f.readlines()
        i = int(lines[-1].split("\t")[0]) + 1
except:
    i = 0

print("i is", i)


@app.get("/", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/listen")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        print(websocket)
        while True:
            global i
            data = await websocket.receive_text()
            print(data, i)
            printReceipt(data, i)
            i += 1

    except Exception as e:
        raise Exception(f"Could not process data: {e}")
    finally:
        await websocket.close()

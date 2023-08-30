import mongo_actions
from cl_currency import ClCurrency
from fastapi import FastAPI, Request, Form, Depends
from statuses import Status
from transaction_details import TransactionDetails
from fastapi.templating import Jinja2Templates
from auth import get_curr_user, get_access_token, register_user, get_access_token_register
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from middleware import TimingMiddleware
import requests

app = FastAPI()
templates = Jinja2Templates(directory="html_pages")
app.add_middleware(TimingMiddleware)



@app.get("/")
async def home_index(request: Request):

    return templates.TemplateResponse("home_index.html", {"request": request})


@app.get("/get")
async def get_trans(t_id: str, current_user=Depends(get_curr_user)):
    return mongo_actions.get_transaction(t_id, current_user.u_name)


@app.delete("/delete")
async def delete_trans(t_id: str, current_user=Depends(get_curr_user)):
    return mongo_actions.delete_transaction(t_id, current_user.u_name)
@app.delete("/delet")
async def delete_trans( current_user=Depends(get_curr_user)):
    print('aaa')
    t_id='tid2001'
    return mongo_actions.delete_transaction(t_id, current_user.u_name)

@app.post("/post/transaction")
async def add_trans(
        transaction_id="tid2000", transaction_status="Successful", amount=0, recipient_u_name="uid2000",
        currency="USD", current_user=Depends(get_curr_user)
):
    u_name = current_user.u_name
    return mongo_actions.add_transaction(
        u_name=u_name,
        details=TransactionDetails(
            transaction_id=transaction_id,
            transaction_status=Status[transaction_status],
            amount=amount,
            recipient_u_name=recipient_u_name,
            currency=ClCurrency[currency],
        ),
    )


@app.put("/put/transaction")
async def update_trans(
        transaction_id="tid2000", transaction_status="Successful", amount=0, recipient_u_name="uid2000", currency="USD",
        current_user=Depends(get_curr_user)
):
    return mongo_actions.update_transaction(
        TransactionDetails(
            transaction_id=transaction_id,
            transaction_status=Status[transaction_status],
            amount=amount,
            recipient_u_name=recipient_u_name,
            currency=ClCurrency[currency],
        ),u_name=current_user.u_name
    )


@app.post('/register/')
async def register_account(u_name: str = Form(...),
                           email: str = Form(...),
                           f_name: str = Form(...),
                           pwd: str = Form(...)):
    u = register_user(u_name=u_name, f_name=f_name, email=email, pwd=pwd)
    token = get_access_token_register(u)

    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }
    return RedirectResponse(url='/ui', headers=headers)
@app.post('/ui')
async def ui_index(request: Request, current_user=Depends(get_curr_user)):
    print(current_user.u_name)
    return templates.TemplateResponse("ui_index.html", {"request": request})
@app.get('/register/')
async def register_index(request: Request):
    return templates.TemplateResponse("register_index.html", {"request": request})





@app.post('/token')
async def login(from_data: OAuth2PasswordRequestForm = Depends()):
    return get_access_token(from_data=from_data)


@app.get('/token')
async def login_index(request: Request):
    return templates.TemplateResponse("login_index.html", {"request": request})


# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)



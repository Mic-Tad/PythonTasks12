import pymongo
from camel_to_snake_converter import change_case
from cl_currency import ClCurrency
from statuses import Status
from transaction_details import TransactionDetails
from user_transactions import UsersTransactions
from user import User
from constants import EXCEP_400_WRONG_USER, EXCEP_400_TR_ALREADY_EXISTS, EXCEP_404_USER_NOT_FOUND

client = pymongo.MongoClient("localhost:27017")
db = client.Market
coll1 = db.Transactions
coll2 = db.UsersTransactions
coll3 = db.Users


def add_user(user: User, coll3=coll3):
    coll3.insert_one({"UName": user.u_name, "Email": user.email, 'FName': user.f_name, 'HashPass': user.hash_pass})


def add_users_trans(users_trans: UsersTransactions, coll2=coll2):
    coll2.insert_one({"UName": users_trans.u_name, 'Transactions': users_trans.transactions})


def update_user(user: User, coll3=coll3):
    if coll3.count_documents({"UName": user.u_name}) < 1:
        add_user(user=user)
    else:
        filt = {"UName": user.u_name}
        new_values = {"$set": {"Email": user.email, 'FName': user.f_name, 'HashPass': user.hash_pass}}
        coll3.update_one(filt, new_values)


def update_users_trans(users_trans: UsersTransactions, coll2=coll2):
    if coll2.count_documents({"UName": users_trans.u_name}) < 1:
        add_users_trans(users_trans=users_trans)
    else:
        filt = {"UName": users_trans.u_name}
        new_values = {"$set": {"Transactions": users_trans.transactions}}
        coll2.update_one(filt, new_values)


def get_user(u_name: str, coll3=coll3):
    if coll3.count_documents({"UName": u_name}) < 1:
        print('We cannot get nonexistent use')
    else:
        u = User()
        for i in coll3.find({"UName": u_name}):
            for k, v in i.items():
                u.__setattr__(k, v)
        return u


def if_user_exists(u_name: str, coll3=coll3):
    return coll3.count_documents({"UName": u_name}) > 0


def add_transaction(u_name: str, details: TransactionDetails, coll1=coll1, coll2=coll2, coll3=coll3):
    s = ""
    if coll1.count_documents({"TransactionId": details.transaction_id}) > 0:
        raise EXCEP_400_TR_ALREADY_EXISTS
    if coll3.count_documents({"UName": details.recipient_u_name}) < 1:
        raise EXCEP_404_USER_NOT_FOUND
    if coll2.count_documents({"UName": u_name}) < 1:
        add_users_trans(UsersTransactions(u_name=u_name, transactions=[details.transaction_id]))
        s += f"New UsersTransactions {u_name} added successfully. "
    else:
        l = list(coll2.find_one({"UName": u_name})["Transactions"])
        h = [i for i in l]
        h.append(details.transaction_id)
        update_users_trans(UsersTransactions(u_name=u_name, transactions=h))

    coll1.insert_one(
        {
            "TransactionId": details.transaction_id,
            "Amount": details.amount,
            "Currency": details.currency.name,
            "TransactionStatus": details.transaction_status.name,
            "RecipientUName": details.recipient_u_name,
        }
    )
    return s + f"Transaction {details.transaction_id} added successfully"


def get_transaction(transaction_id: str, u_name: str, coll1=coll1, coll2=coll2):
    if coll2.count_documents({"UName": u_name}) < 1:
        raise EXCEP_400_WRONG_USER
    elif not (transaction_id in coll2.find_one({"UName": u_name})["Transactions"]):
        raise EXCEP_400_WRONG_USER
    if coll1.count_documents({"TransactionId": transaction_id}) < 1:
        return "We cannot get nonexistent transaction"
    t = TransactionDetails()
    for i in coll1.find({"TransactionId": transaction_id}):
        for k, v in i.items():
            t.__setattr__(k, v)
    return t


def update_transaction(details: TransactionDetails, u_name: str, coll1=coll1, coll2=coll2):
    if coll2.count_documents({"UName": u_name}) < 1:
        raise EXCEP_400_WRONG_USER
    elif not (details.transaction_id in coll2.find_one({"UName": u_name})["Transactions"]):
        raise EXCEP_400_WRONG_USER
    flag = False
    if coll1.count_documents({"TransactionId": details.transaction_id}) < 1:
        return "We cannot update nonexistent transaction"
    for new_data in coll1.find({"TransactionId": details.transaction_id}):
        for k, v in new_data.items():
            k = change_case(k)
            if k != "_id" and details.__dict__[k] != v:
                flag = True
                break
    if flag:
        filt = {"TransactionId": details.transaction_id}
        new_values = {
            "$set": {
                "TransactionId": details.transaction_id,
                "Amount": details.amount,
                "Currency": details.currency.name,
                "TransactionStatus": details.transaction_status.name,
                "RecipientUName": details.recipient_u_name,
            }
        }
        coll1.update_one(filt, new_values)
        return f"Transaction {details.transaction_id} updated successfully"
    else:
        return "No updates needed"


def create_index(field, unique=False, coll1=coll1):
    coll1.create_index(field, unique=unique)


def delete_transaction(transaction_id: str, u_name: str, coll1=coll1, coll2=coll2):
    if coll2.count_documents({"UName": u_name}) < 1:
        raise EXCEP_400_WRONG_USER
    elif not (transaction_id in coll2.find_one({"UName": u_name})["Transactions"]):
        raise EXCEP_400_WRONG_USER
    if coll1.count_documents({"TransactionId": transaction_id}) < 1:
        return "No transactions to delete"
    coll1.delete_one({"TransactionId": transaction_id})
    filt = {"UName": u_name}
    l = list(coll2.find_one({"UName": u_name})["Transactions"])
    if len(l) < 2:
        coll2.delete_one({"UName": u_name})
    else:

        l.remove(transaction_id)

        for i in l:
            print(i, type(i))
        new_values = {
            "$set": {
                "UName": u_name,
                "Transactions": l
            }
        }
        coll2.update_one(filt, new_values)
    return f"Transaction {transaction_id} deleted successfully"


def clear_db(coll=coll1):
    coll.delete_many({})


def create_transactions(user: User, n: int, coll1=coll1, coll2=coll2):
    for i in range(n):
        add_transaction(
            u_name=user.u_name,
            details=TransactionDetails(
                transaction_id=f"tid200{i}",
                transaction_status=Status.Successful,
                amount=i * i + 200 % (i + 1),
                recipient_u_name=f"uid234{i * 2}",
                currency=ClCurrency.EUR,
            ),
            coll2=coll2,
            coll1=coll1,
        )

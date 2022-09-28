from ast import Delete
from email import message
from fastapi import FastAPI
from db import conn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn




app = FastAPI()

@app.get("/")
def show_all_data():
    val=conn.execute("select * from customer_table ").mappings().all()
    return JSONResponse({"message":"hello","key":jsonable_encoder(val)})

@app.post("/create")
def customer(customer_name:str,customer_address:str,customer_email:str):
    val=conn.execute(f"select * from customer_table where customer_email='{customer_email}'").mappings().all()
    if len(val)==0:
        val=conn.execute(f"INSERT INTO customer_table (customer_name,customer_address,customer_email) VALUES('{customer_name}','{customer_address}','{customer_email}')")
        return JSONResponse({"message":"user created"})
    else:
        return  JSONResponse({"message":"user exist"})
@app.post("/customer")
def customer_add(product_name:str,product_price:int):
    val=conn.execute(f"select * from product_table where product_name='{product_name}'").mappings().all()
    if len(val)==0:
        val=conn.execute(f"INSERT INTO product_table (product_name,product_price) VALUES('{product_name}','{product_price}')")
        return JSONResponse({"message":"user created"})
    else:
        return  JSONResponse({"message":"user exist"})

@app.post("/order")
def order_add(customer_email:str,product_name:str,quantity:int=1):
    if customer_email:
        customer_data=conn.execute(f"select * from customer_table where customer_email='{customer_email}'").mappings().all()        
        if len(customer_data)==0:
            return({"message":"customer_email not found"})
        else:
           customer_id = customer_data[0]["customer_id"]
           customer_name = customer_data[0]["customer_name"]
      
           
    if product_name:
        product_data=conn.execute(f"select * from product_table where product_name='{product_name}'").mappings().all()
        if len(product_data)==0:
            return({"message":"product_name not found"})
        else:
            product_id = product_data[0]["product_id"]
            product_price = product_data[0]["product_price"]
    
    Total_price = product_price * quantity
  

    conn.execute(f"INSERT INTO order_table (customer_id,product_id,order_price) VALUES('{customer_id}','{product_id}',{Total_price})")
    data =({"message":"order_plased",
            "customer_name":customer_name,
            "product_name":product_name,
            "quantity":quantity,
            "product_price":product_price,
            "Total_price":Total_price }) 
    return data

@app.post("/order_details")
def order_details(customer_id:int):
    order = conn.execute(f"select * from order_table  where customer_id='{customer_id}'").mappings().all()
    
    name_list =[]
    if order:
        for i in order:
            data=conn.execute(f"select * from product_table where product_id = {i['product_id']}").mappings().all()
            name = {"order_id":i["order_id"],
                    "product_name":data[0]["product_name"],
                    "total_price":i["order_price"]}
                    
            name_list.append(name)         
    
        return  JSONResponse({"message":"hello","key":jsonable_encoder(name_list)})
    else:
        return ({"message":"customer_id invlaid"})
@app.delete("/cancle_tha_order")
def c_order(order_id:int):
    create=conn.execute(f"select * from order_table where order_id='{order_id}'").mappings().all()
    if len(create)!=0:
        conn.execute(f"DELETE FROM order_table WHERE order_id='{order_id}'")
        return ({"message":"datacleare"})
    else:
        return ({"message":"invalid"})
    
@app.post("/order_id")
def order(order_id:int):
    data = conn.execute(f"""SELECT order_table.order_id,order_table.customer_id, customer_table.customer_name,product_table.product_price
                        FROM order_table
                        INNER JOIN customer_table ON order_table.customer_id = customer_table.customer_id
                        INNER JOIN product_table ON order_table.product_id = product_table.product_id
                        WHERE order_table.order_id={order_id}""").mappings().all()
    if len(data)==0:
        return ({"message":"invalid"})
    else:
        return JSONResponse({"message":jsonable_encoder(data)})
@app.post("/customer_id_z")
def uswe(customer_id:int):
    cd = conn.execute(f"""SELECT customer_table.customer_id, customer_table.customer_name,product_table.product_name,order_table.order_id,order_table.order_price,order_table.product_id
                    FROM order_table
                    INNER JOIN customer_table ON order_table.customer_id = customer_table.customer_id
                    INNER JOIN product_table ON order_table.product_id = product_table.product_id
                    WHERE customer_table.customer_id='{customer_id}'""").mappings().all()
    if len(cd)==0:
        return ({"message":"invalid"})
    else:
         return JSONResponse({"message":jsonable_encoder(cd)})





if __name__=="__main__":
    uvicorn.run("index:app",port=8000,reload=True)
import uvicorn 
import app.app as app
import database.database 
if __name__ =="__main__":
  uvicorn.run(app.app,host='127.0.0.1',port=3001)
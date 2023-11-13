import uvicorn 
import database.database as db 
if __name__ =="__main__":
  db.create_db()
  uvicorn.run("app.App:app",host='127.0.0.1',port=3001,reload=True)
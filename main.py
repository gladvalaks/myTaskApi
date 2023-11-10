import uvicorn 
import app.app as app

if __name__ =="__main__":
  uvicorn.run(app.app,host='localhost',port=3001)
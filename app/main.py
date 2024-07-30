from semrush import parser
from fastapi import FastAPI,Request,HTTPException
import uvicorn
from json import JSONDecodeError
from task import manager
from semrush import parser

app = FastAPI()

        

@app.post("/process/add")
async def process_add(request: Request):
     try:
          data = await request.json()
          task_id = manager.create_task(data)
          manager.task_process(task_id,{
              "task":data['task'],
              "urls":len(data['urls']),
              "completed":0,
              "errors":0,
              "status":"run"
          })
          
          return {'status':'succeful', 'id': task_id}
     except JSONDecodeError:
          raise HTTPException(status_code=400, detail='Invalid JSON data')

@app.get("/process/check/{task_id}")
async def check_task(task_id: int):
    if(task_id):
      return manager.get_task_process(task_id)
    
@app.get("/process/result/{task_id}")
async def check_task(task_id: int):
    if(task_id):
      return manager.get_task_result(task_id)    
 
           
@app.get("/task/list")
async def list_task():   
    return manager.get_task_list()      
 
@app.get("/task/start")
async def start_task():   
    return manager.do_task(parser)            


if __name__ == "__main__":

  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  
  

 



 

  
#print(domainOverview())    
#print(organicSummary())
#Api = parser.SemRush(userId=21956293,apiKey = "1c2ee429d802db9da677257125e73f94",searchItem = "roms-download.com")

#print(Api.backlinksSummary())
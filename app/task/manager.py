import redis
import time
import pickle
import random
import time
database = redis.Redis(host='redis', port=6379)

def create_task(task):
    time_id = int(time.time()+random.randint(50,300))
    database.set(f"task:{time_id}", pickle.dumps(task))

    task_list = database.get('task:list')
    if(task_list):
        task_list = pickle.loads(task_list)
        task_list[time_id]=time_id
    else:
        task_list = dict()
        task_list[time_id]=time_id
            
    database.set('task:list', pickle.dumps(task_list))

    return time_id



def update_task(task_id,url,data):
    task_list = database.get(f"task:result:{task_id}")
    if(task_list):
        task_list = pickle.loads(task_list)
        task_list[url]=data
    else:
        task_list = dict()
        task_list[url]=data
            
    database.set(f"task:result:{task_id}", pickle.dumps(task_list))



def task_process(task_id,process):
    database.set(f"task:process:{task_id}", pickle.dumps(process))

def get_task(task_id):
    task = database.get(f"task:{task_id}")
    task_data = pickle.loads(task)
    return task_data

def get_task_list():
    task = database.get('task:list')
    if(task):
       task_data = pickle.loads(task)
    else:
       task_data = dict()   
    return task_data

def get_task_process(task_id):
    task = database.get(f"task:process:{task_id}")
    if(task):
       task_data = pickle.loads(task)
    else:
       task_data = dict()    
    
    return task_data

def delete_task(task_id):
    task = database.get('task:list')
    if(task):
      task_data = pickle.loads(task)
    else:
      return dict()   
    if task_id in task_data:
     del task_data[task_id]
     database.set('task:list', pickle.dumps(task_data))
    return task_data

def get_task_result(task_id):  
    task = database.get(f"task:result:{task_id}")
    if(task):
        task_data = pickle.loads(task)
    else:
        task_data = dict()
         
    return task_data  
   
def do_task(parser):
    while True:
      time.sleep(1)
      tasks = get_task_list()

      for task in tasks:
          task_data = get_task(task)

          #парсим
          for count, url in enumerate(task_data['urls']):
            Api = parser.SemRush(userId=task_data['user_id'],apiKey = task_data['api_key'],searchItem = url)
            if(task_data['task']=="domainOverview"):
                result = Api.domainOverview()
            elif(task_data['task']=="organicSummary"):
                result = Api.organicSummary()
            elif(task_data['task']=="backlinksSummary"):
                result = Api.backlinksSummary()    
                
            task_count_url = get_task_process(task)

            if 'error' in result:
                update_task(task,url,{
                'error':result
                })
                errors = task_count_url['errors']+1
                completed = task_count_url['completed']
            else:
                errors = task_count_url['errors']
                completed = task_count_url['completed']+1


                
            update_task(task,url,{
                'result':result
            })

            
            task_list = get_task_result(task) 
            if(len(task_list) == task_count_url['urls']):
                delete_task(task)
                if(errors):
                    status = "failed"
                else:
                    status = "finish"    

            else:
                status = "in_process"      
            #"completed":len(task_list),  
            task_process(task,{
                "task":task_data['task'],
                "urls":len(task_data['urls']),
                "completed":completed,
                "errors":errors, 
                "status":status
            })
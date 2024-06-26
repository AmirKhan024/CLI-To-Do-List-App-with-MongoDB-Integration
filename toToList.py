import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["todolist"]
collection=db["userToDo"]


tasks=[]
saveList=[]
count=1
def addTask():
    newTask=input("Add the task : ")
    tasks.append(newTask)
    print(f"'{newTask}' added successfully")
def listTasks():
    if not tasks:
        print("There are currently no tasks")
    else:
        print("Unsaved tasks : ")
        for index,task in enumerate(tasks, start=1):
            print(f"Task #{index}. {task}")
def deleteTask():
    listTasks()
    if tasks:
        taskDelete=int(input("Enter number to delete an unsaved Task : "))
        if(taskDelete>=1 and taskDelete<=len(tasks)):
            tasks.pop(taskDelete-1)
            print(f"Task #{taskDelete} deleted successfully")
        else:
            print("Invalid input")
def saveTasks():    
    global count
       
    for task in tasks:        
        saveList.append({f"Task{count}":task}) 
        count+=1
    doc=collection.insert_many(saveList)
    saveList.clear()
    tasks.clear()
    print("Tasks saved successfully")


def previousTasks():
    if(collection.count_documents({})==0):
        print("There are no tasks stored")
    else:
        tasks=[]
        for i,doc in enumerate(collection.find({},{"_id":0}),start=1):
            for key,value in doc.items():
                tasks.append({f"Task{i}":value})
        print("Saved task are : ")
        for x in tasks:
            print(x)

def deleteSavedTask():
    previousTasks()  
    if(collection.count_documents({})!=0): 
        dst=int(input("Enter number you want to delete : "))   

        query={"Task{}".format(dst):{"$exists":True}}
        deletedvalue=collection.delete_one(query)
        if(deletedvalue.deleted_count!=0):
            print("Task {} deleted successfully".format(dst))
        else:
            print("Task {} does not exist".format(dst))  
    
print("***Welcome to To Do List Application :) ***")
print("------------------------------------")
while(True):
    print("Please select any one operation:-")
    print("1. Add task")
    print("2. Delete unsaved task")
    print("3. List the unsaved tasks")
    print("4. Save")
    print("5. List all the saved tasks ")
    print("6. Delete saved task")
    print("7. Quit")
    print()
    ip=input("Enter your choice : ")
    if(ip=="1"):
        addTask()
    elif(ip=="2"):
        deleteTask()
    elif(ip=="3"):
        listTasks()
    elif(ip=="4"):
        if(len(tasks)==0):
            print("No task to save! Please add some tasks first")
        else:
            saveTasks()
    elif(ip=="5"):
        previousTasks()
    elif(ip=="6"):
        deleteSavedTask()
    elif(ip=="7"):
        print("Goodbye 👋👋")
        break
    else:
        print("Invalid Input")
    

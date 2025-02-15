from fastapi import FastAPI, HTTPException
import os
import subprocess
import requests

app = FastAPI()

AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")

@app.post("/run")
async def run_task(task: str):
    try:
        # Parse the task using an LLM (GPT-4o-Mini)
        response = requests.post(
            "https://api.aiproxy.io/v1/complete",
            headers={"Authorization": f"Bearer {AIPROXY_TOKEN}"},
            json={"prompt": f"Parse this task and return the steps to execute: {task}"}
        )
        steps = response.json()["choices"][0]["text"]

        # Execute the steps (this is a placeholder; you'll need to implement this)
        execute_steps(steps)

        return {"status": "success", "message": "Task executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 
@app.get("/read")
async def read_file(path: str):
    try:
        with open(path, "r") as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def execute_steps(steps):
    # Implement logic to execute the steps here
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
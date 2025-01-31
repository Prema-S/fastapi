from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import uvicorn

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure CSV file exists
csv_file = "/mnt/data/q-fastapi.csv"
def load_csv():
    try:
        if os.path.exists(csv_file):
            return pd.read_csv(csv_file)
        else:
            return pd.DataFrame(columns=["studentId", "class"])
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=["studentId", "class"])

df = load_csv()

@app.get("/api")
def get_students(class_: list[str] = Query(None, alias="class")):
    filtered_df = df if class_ is None else df[df["class"].isin(class_)]
    return {"students": filtered_df.to_dict(orient="records")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

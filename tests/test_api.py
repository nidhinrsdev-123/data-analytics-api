def test_health(client):
 r=client.get("/health"); assert r.status_code==200 and r.json()=={"status":"ok"}
def test_upload_preview_and_summary(client):
 r=client.post("/api/v1/datasets",files={"file":("sales.csv","region,revenue\nNorth,100\nSouth,200\n","text/csv")})
 assert r.status_code==201
 i=r.json()["id"]
 assert len(client.get(f"/api/v1/datasets/{i}/preview").json()["rows"])==2
 summary=client.get(f"/api/v1/datasets/{i}/summary").json()
 assert summary["numeric_columns"]["revenue"]["mean"]==150.0
def test_reject_non_csv(client):
 assert client.post("/api/v1/datasets",files={"file":("notes.txt","hello","text/plain")}).status_code==415
def test_missing_dataset_returns_404(client):
 assert client.get("/api/v1/datasets/999/summary").status_code==404

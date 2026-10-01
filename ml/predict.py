from ultralytics import YOLO
model=YOLO("backend/models/waste.pt")
results=model.predict(source="sample.jpg",conf=0.5,save=True)
for r in results:
    print(r.probs)
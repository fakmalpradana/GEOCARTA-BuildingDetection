from ultralytics import YOLO

model = YOLO('runs/segment/train53/weights/best.pt')
results = model.train(
    data='data.yaml', 
    epochs=10000, 
    imgsz=320, 
    name='train5', 
    # resume=True, 
    amp=False,
    batch=4, 
    patience=0, 
    mask_ratio=1,
    cls=1.0,
)
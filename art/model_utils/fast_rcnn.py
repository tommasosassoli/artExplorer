import torchvision

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights='DEFAULT')
model.eval()
preprocess = torchvision.transforms.ToTensor()

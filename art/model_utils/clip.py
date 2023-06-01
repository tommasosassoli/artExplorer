import open_clip

device = "cpu"
clip_model = "RN50"     # ViT-B-32-quickgelu
pretrained = 'openai'

model, _, preprocess = open_clip.create_model_and_transforms(clip_model, pretrained=pretrained, device=device)
tokenizer = open_clip.get_tokenizer(clip_model)
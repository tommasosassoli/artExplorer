import open_clip

device = "cpu"
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32-quickgelu', pretrained='laion400m_e32',
                                                             device=device)
tokenizer = open_clip.get_tokenizer('ViT-B-32-quickgelu')
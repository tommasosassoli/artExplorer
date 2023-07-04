import open_clip
import configparser
from definitions import CONFIG_PATH

# config
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

clip_model = config['clip']['clip_model']
clip_pretrained = config['clip']['clip_pretrained']
device = config['clip']['device']

# clip init
model, _, preprocess = open_clip.create_model_and_transforms(clip_model, pretrained=clip_pretrained,
                                                             device=device)
tokenizer = open_clip.get_tokenizer(clip_model)


def get_clip_model():
    return model, preprocess, tokenizer, device

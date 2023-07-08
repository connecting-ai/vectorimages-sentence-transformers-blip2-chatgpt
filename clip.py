from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import numpy as np
import os

#these functions are to 
# encode a directory full of images as vectors, 
# encode a text description as a vector, 
# and then use those encodings to find the images in the directory that best match that text description.

# Load CLIP model. We only want to do this once.
model = SentenceTransformer('clip-ViT-B-32')

def encode_images_from_directory(directory, model):
    #creates one vector representing the content of each image in the directory
    image_embeds = []
    image_filenames = []

    for f in glob.iglob(directory):
        img_emb = model.encode(Image.open(f))
        image_embeds.append(img_emb)
        image_filenames.append(f)
    return [image_embeds, image_filenames]

def encode_text_description(text, model):
    #creates a vector for a string decsribing the image you are looking for
    text_emb = model.encode([text])
    return text_emb

def find_top_N_matches(text_emb, image_embeds, N, image_filenames):
    # Compute cosine similarities
    cos_scores = util.cos_sim(text_emb, image_embeds)
    cos_scores = cos_scores.flatten()
    sorted_indices = np.argsort(cos_scores)
    # Get the filenames of the top 5 images
    top_image_filenames = [image_filenames[i] for i in sorted_indices[-N:]]
    return top_image_filenames

def run(path, input):
    print(path)
    [image_embeds, image_filenames] = encode_images_from_directory(path ,model)
    text_emb = encode_text_description(input, model)
    top_image_filenames = find_top_N_matches(text_emb, image_embeds, 5, image_filenames)

    result_files = []
    for filename in top_image_filenames:
        name_only = os.path.basename(filename)
        result_files.append(name_only)
    
    return result_files

if __name__ == "__main__":
    run("images/*", "african style hut")
    
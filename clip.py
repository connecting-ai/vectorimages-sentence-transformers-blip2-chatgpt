from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import numpy as np
import os
import pickledb
db = pickledb.load('/db/clip.db', False)

#these functions are to 
# encode a directory full of images as vectors, 
# encode a text description as a vector, 
# and then use those encodings to find the images in the directory that best match that text description.

# Load CLIP model. We only want to do this once.
model = SentenceTransformer(model_name_or_path='sentence-transformers/clip-ViT-B-32', device='cuda:0')

def encodeCacheImage(f):
    value = db.get(f)

    try:
        if not value:
            print("Not found from DB")
            img = Image.open(f)
            img = img.resize((224, 224), Image.NEAREST)
            value = model.encode(Image.open(f))            
            db.set(f, value)
    except:
        if value is not None:
            print("PICKED from DB")

    return value

def encode_images_from_directory(directory, model):
    #creates one vector representing the content of each image in the directory
    image_embeds = []
    image_filenames = []

    for f in glob.iglob(directory):

        img_emb = encodeCacheImage(f)
        image_embeds.append(img_emb)
        image_filenames.append(f)
    return [image_embeds, image_filenames]

def encode_text_description(text, model):
    #creates a vector for a string decsribing the image you are looking for
    text_emb = model.encode([text])
    return text_emb

def find_top_N_matches(text_emb, image_embeds, N, image_filenames):
    # Compute cosine similarities
    print(image_filenames)
    for i in range(len(image_embeds)):
              #check if it is a numy sequence
        if not isinstance(image_embeds[i], np.ndarray):
            print("not a numpy array - ", image_filenames[i])
            #remove both the image and the vector
            image_filenames.pop(i)
            image_embeds.pop(i)
            continue
        #check if the vector is the right size
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
    
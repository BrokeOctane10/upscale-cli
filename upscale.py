import cv2
import os
import re
from pathlib import Path

def get_available_models(models_dir="models"):
    """Scans the models directory and returns a sorted list of model file paths."""
    if not os.path.exists(models_dir):
        return []
    
    valid_extensions = (".pb", ".onnx")
    models = [
        os.path.join(models_dir, f) 
        for f in os.listdir(models_dir) 
        if f.endswith(valid_extensions)
    ]
    return sorted(models)

def upscale_image():
    # 1. Prompt for image path
    image_path = input("Enter the path to the image: ").strip().strip("'\"")
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' not found.")
        return

    # 2. Select model from the 'models' sub-directory
    models = get_available_models("models")
    if not models:
        print("Error: No models found in the 'models/' directory! Please add some .pb files there.")
        return

    print("\nAvailable Models:")
    for idx, model_path in enumerate(models, 1):
        print(f"  [{idx}] {os.path.basename(model_path)}")

    try:
        choice = int(input("\nSelect a model number to use: "))
        if choice < 1 or choice > len(models):
            print("Invalid model selection.")
            return
        selected_model_path = models[choice - 1]
    except ValueError:
        print("Please enter a valid number.")
        return

    # 3. Automatically extract scale factor and model name from filename (e.g., '2_espcn_x4.pb' -> scale 4, name 'espcn')
    model_filename = os.path.basename(selected_model_path).lower()
    
    # Extract scale using regex (looks for 'x' followed by digits like _x2, _x3, _x4)
    scale_match = re.search(r'[xX](\d+)', model_filename)
    scale = int(scale_match.group(1)) if scale_match else 4

    # Extract clean model name
    clean_name = model_filename.split(".")[0]
    if "_" in clean_name and clean_name.split("_")[0].isdigit():
        clean_name = "_".join(clean_name.split("_")[1:])
    model_name = clean_name.split("_")[0]

    # 4. Initialize OpenCV DNN Super Resolution
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(selected_model_path)
    sr.setModel(model_name, scale)

    # 5. Load and Process Image
    image = cv2.imread(image_path)
    print(f"\nUpscaling '{os.path.basename(image_path)}' with automatically detected {scale}x scale using {model_filename}...")
    
    result = sr.upsample(image)

    # 6. Generate custom output name: <original_name>_<scale>x_<model_name>.jpg
    orig_path = Path(image_path)
    output_filename = f"{orig_path.stem}_{scale}x_{model_name}{orig_path.suffix}"
    output_path = os.path.join(orig_path.parent, output_filename)

    cv2.imwrite(output_path, result)
    print(f"Successfully saved upscaled image to: {output_path}")

if __name__ == "__main__":
    upscale_image()

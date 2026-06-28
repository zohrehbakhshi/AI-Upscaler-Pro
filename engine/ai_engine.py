# engine/ai_engine.py

import torch
import numpy as np
import cv2
from PIL import Image

try:
    from realesrgan import RealESRGANer
    from basicsr.archs.rrdbnet_arch import RRDBNet
except ImportError:
    RealESRGANer = None
    RRDBNet = None


class AIEngine:
    def __init__(self, model_path=None, scale=4, device=None):
        """
        AI Upscaling Engine using Real-ESRGAN
        """

        self.scale = scale

        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = None
        self.upsampler = None

        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        """
        Load Real-ESRGAN model
        """

        if RealESRGANer is None:
            raise ImportError("realesrgan is not installed")

        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=self.scale
        )

        self.upsampler = RealESRGANer(
            scale=self.scale,
            model_path=model_path,
            model=model,
            tile=256,
            tile_pad=10,
            pre_pad=0,
            half=(self.device == "cuda"),
            device=self.device
        )

    def upscale_image(self, image_input):
        """
        Upscale image
        image_input: str path OR PIL Image OR numpy array
        return: PIL Image
        """

        img = self._to_numpy(image_input)

        if self.upsampler is None:
            raise RuntimeError("Model is not loaded")

        output, _ = self.upsampler.enhance(img, outscale=self.scale)

        return Image.fromarray(output)

    def upscale_batch(self, images):
        """
        Upscale multiple images
        """
        return [self.upscale_image(img) for img in images]

    def _to_numpy(self, img):
        """
        Convert input to OpenCV format (BGR numpy)
        """

        if isinstance(img, str):
            img = cv2.imread(img, cv2.IMREAD_COLOR)

        elif isinstance(img, Image.Image):
            img = np.array(img.convert("RGB"))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        elif isinstance(img, np.ndarray):
            if img.shape[-1] == 3:
                img = img
            else:
                raise ValueError("Invalid image array format")

        else:
            raise TypeError("Unsupported image type")

        return img

    def clear_gpu(self):
        """
        Free GPU memory
        """
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
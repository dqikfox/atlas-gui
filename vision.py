"""
Vision Manager for ULTRON Dashboard - Full Implementation
Provides OCR, screenshot analysis, and image processing capabilities
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
import io
import base64
import logging
from PIL import Image, ImageEnhance, ImageFilter
from typing import Dict, Any, List, Tuple, Optional
import tempfile
import os

logger = logging.getLogger(__name__)

class VisionManager:
    def __init__(self):
        """Initialize vision manager with OCR and image processing"""
        self.enabled = True
        self.ocr_config = {
            'lang': 'eng',  # Language for OCR
            'oem': 3,       # OCR Engine Mode
            'psm': 6,       # Page Segmentation Mode
        }
        
        try:
            self._initialize_tesseract()
            self._test_ocr()
            logger.info("Vision Manager initialized successfully")
        except Exception as e:
            logger.error(f"Vision Manager initialization failed: {e}")
            self.enabled = False
    
    def _initialize_tesseract(self):
        """Initialize Tesseract OCR engine"""
        try:
            # Try to find Tesseract installation
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
                'tesseract'  # If in PATH
            ]
            
            for path in possible_paths:
                try:
                    pytesseract.pytesseract.tesseract_cmd = path
                    # Test if this path works
                    pytesseract.get_tesseract_version()
                    logger.info(f"Tesseract found at: {path}")
                    break
                except:
                    continue
            else:
                logger.warning("Tesseract not found in standard locations, using system PATH")
                
        except Exception as e:
            logger.error(f"Tesseract initialization failed: {e}")
            raise
    
    def _test_ocr(self):
        """Test OCR functionality with a simple image"""
        try:
            # Create a test image with text
            test_img = Image.new('RGB', (200, 50), color='white')
            import PIL.ImageDraw as ImageDraw
            import PIL.ImageFont as ImageFont
            
            draw = ImageDraw.Draw(test_img)
            try:
                # Try to use default font
                draw.text((10, 15), "TEST", fill='black')
            except:
                # Fallback if font loading fails
                pass
                
            # Test OCR on this image
            pytesseract.image_to_string(test_img)
            logger.info("OCR test passed")
            
        except Exception as e:
            logger.warning(f"OCR test failed: {e}")
    
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Take a screenshot of the screen or specific region
        
        Args:
            region: Tuple of (left, top, width, height) for specific region
            
        Returns:
            Dict with screenshot data and metadata
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            # Convert to base64 for JSON serialization
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            return {
                "status": "success",
                "image_data": img_base64,
                "format": "PNG",
                "size": screenshot.size,
                "region": region,
                "message": f"Screenshot captured: {screenshot.size[0]}x{screenshot.size[1]}"
            }
            
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return {"status": "error", "message": f"Screenshot failed: {str(e)}"}
    
    def analyze_image(self, image_data: bytes, analysis_type: str = "ocr") -> Dict[str, Any]:
        """
        Analyze image with various methods
        
        Args:
            image_data: Image data as bytes
            analysis_type: Type of analysis ("ocr", "objects", "text_detection", "colors")
            
        Returns:
            Dict with analysis results
        """
        if not self.enabled:
            return {"status": "error", "message": "Vision analysis not available"}
        
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(image_data))
            
            if analysis_type == "ocr":
                return self._perform_ocr(image)
            elif analysis_type == "objects":
                return self._detect_objects(image)
            elif analysis_type == "text_detection":
                return self._detect_text_regions(image)
            elif analysis_type == "colors":
                return self._analyze_colors(image)
            elif analysis_type == "all":
                return self._comprehensive_analysis(image)
            else:
                return {"status": "error", "message": f"Unknown analysis type: {analysis_type}"}
                
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return {"status": "error", "message": f"Analysis failed: {str(e)}"}
    
    def _perform_ocr(self, image: Image.Image) -> Dict[str, Any]:
        """Perform OCR on image to extract text"""
        try:
            # Enhance image for better OCR
            enhanced_image = self._enhance_for_ocr(image)
            
            # Configure Tesseract
            config = f'--oem {self.ocr_config["oem"]} --psm {self.ocr_config["psm"]} -l {self.ocr_config["lang"]}'
            
            # Extract text
            text = pytesseract.image_to_string(enhanced_image, config=config)
            
            # Get detailed data with bounding boxes
            data = pytesseract.image_to_data(enhanced_image, config=config, output_type=pytesseract.Output.DICT)
            
            # Process results
            words = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30:  # Confidence threshold
                    words.append({
                        'text': data['text'][i].strip(),
                        'confidence': data['conf'][i],
                        'bbox': [data['left'][i], data['top'][i], data['width'][i], data['height'][i]]
                    })
            
            return {
                "status": "success",
                "text": text.strip(),
                "words": [w for w in words if w['text']],
                "total_words": len([w for w in words if w['text']]),
                "average_confidence": np.mean([w['confidence'] for w in words if w['text']]) if words else 0
            }
            
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return {"status": "error", "message": f"OCR failed: {str(e)}"}
    
    def _enhance_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR results"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            # Scale up for better recognition
            width, height = image.size
            image = image.resize((width * 2, height * 2), Image.LANCZOS)
            
            return image
            
        except Exception as e:
            logger.error(f"Image enhancement failed: {e}")
            return image
    
    def _detect_text_regions(self, image: Image.Image) -> Dict[str, Any]:
        """Detect text regions in image using OpenCV"""
        try:
            # Convert PIL to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Use MSER (Maximally Stable Extremal Regions) for text detection
            mser = cv2.MSER_create()
            regions, _ = mser.detectRegions(gray)
            
            # Convert regions to bounding boxes
            text_regions = []
            for region in regions:
                x, y, w, h = cv2.boundingRect(region)
                text_regions.append([x, y, w, h])
            
            return {
                "status": "success",
                "text_regions": text_regions,
                "region_count": len(text_regions),
                "message": f"Found {len(text_regions)} potential text regions"
            }
            
        except Exception as e:
            logger.error(f"Text region detection failed: {e}")
            return {"status": "error", "message": f"Text detection failed: {str(e)}"}
    
    def _detect_objects(self, image: Image.Image) -> Dict[str, Any]:
        """Basic object detection using OpenCV contours"""
        try:
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter and process contours
            objects = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small objects
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        'bbox': [x, y, w, h],
                        'area': area,
                        'aspect_ratio': w / h if h > 0 else 0
                    })
            
            return {
                "status": "success",
                "objects": objects,
                "object_count": len(objects),
                "message": f"Detected {len(objects)} potential objects"
            }
            
        except Exception as e:
            logger.error(f"Object detection failed: {e}")
            return {"status": "error", "message": f"Object detection failed: {str(e)}"}
    
    def _analyze_colors(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze dominant colors in image"""
        try:
            # Convert to RGB and get pixels
            rgb_image = image.convert('RGB')
            pixels = np.array(rgb_image)
            
            # Reshape to get all pixels
            pixels_flat = pixels.reshape(-1, 3)
            
            # Use k-means clustering to find dominant colors
            from sklearn.cluster import KMeans
            
            # Reduce sample size for performance
            sample_size = min(1000, len(pixels_flat))
            sample_pixels = pixels_flat[np.random.choice(len(pixels_flat), sample_size, replace=False)]
            
            # Find 5 dominant colors
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(sample_pixels)
            
            dominant_colors = []
            for color in kmeans.cluster_centers_:
                dominant_colors.append({
                    'rgb': [int(c) for c in color],
                    'hex': '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))
                })
            
            return {
                "status": "success",
                "dominant_colors": dominant_colors,
                "image_size": image.size,
                "color_count": len(dominant_colors)
            }
            
        except Exception as e:
            logger.error(f"Color analysis failed: {e}")
            # Fallback without ML
            try:
                colors = image.getcolors(maxcolors=256*256*256)
                if colors:
                    # Get top 5 colors by frequency
                    top_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
                    simple_colors = []
                    for count, color in top_colors:
                        if isinstance(color, tuple) and len(color) >= 3:
                            simple_colors.append({
                                'rgb': list(color[:3]),
                                'hex': '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2]),
                                'frequency': count
                            })
                    
                    return {
                        "status": "success",
                        "dominant_colors": simple_colors,
                        "method": "frequency_based"
                    }
            except:
                pass
                
            return {"status": "error", "message": f"Color analysis failed: {str(e)}"}
    
    def _comprehensive_analysis(self, image: Image.Image) -> Dict[str, Any]:
        """Perform comprehensive analysis combining multiple methods"""
        try:
            results = {
                "status": "success",
                "image_info": {
                    "size": image.size,
                    "mode": image.mode,
                    "format": getattr(image, 'format', 'Unknown')
                }
            }
            
            # OCR analysis
            ocr_result = self._perform_ocr(image)
            if ocr_result["status"] == "success":
                results["ocr"] = ocr_result
            
            # Object detection
            object_result = self._detect_objects(image)
            if object_result["status"] == "success":
                results["objects"] = object_result
            
            # Color analysis
            color_result = self._analyze_colors(image)
            if color_result["status"] == "success":
                results["colors"] = color_result
            
            # Text regions
            text_region_result = self._detect_text_regions(image)
            if text_region_result["status"] == "success":
                results["text_regions"] = text_region_result
            
            return results
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return {"status": "error", "message": f"Comprehensive analysis failed: {str(e)}"}
    
    def find_text_on_screen(self, search_text: str, confidence: float = 0.8) -> Dict[str, Any]:
        """Find specific text on screen using OCR"""
        try:
            # Take screenshot
            screenshot_result = self.take_screenshot()
            if screenshot_result["status"] != "success":
                return screenshot_result
            
            # Decode image
            image_data = base64.b64decode(screenshot_result["image_data"])
            
            # Perform OCR
            ocr_result = self.analyze_image(image_data, "ocr")
            if ocr_result["status"] != "success":
                return ocr_result
            
            # Search for text
            found_matches = []
            for word_info in ocr_result.get("words", []):
                if (search_text.lower() in word_info["text"].lower() and 
                    word_info["confidence"] >= confidence * 100):
                    found_matches.append(word_info)
            
            return {
                "status": "success",
                "search_text": search_text,
                "matches": found_matches,
                "match_count": len(found_matches),
                "full_text": ocr_result.get("text", "")
            }
            
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return {"status": "error", "message": f"Text search failed: {str(e)}"}
    
    def get_vision_info(self) -> Dict[str, Any]:
        """Get information about vision capabilities and configuration"""
        try:
            tesseract_version = "Unknown"
            try:
                tesseract_version = pytesseract.get_tesseract_version()
            except:
                pass
            
            opencv_version = "Unknown"
            try:
                opencv_version = cv2.__version__
            except:
                pass
            
            return {
                "status": "success",
                "enabled": self.enabled,
                "tesseract_version": str(tesseract_version),
                "opencv_version": opencv_version,
                "ocr_config": self.ocr_config,
                "supported_analyses": ["ocr", "objects", "text_detection", "colors", "all"],
                "capabilities": [
                    "Screenshot capture",
                    "OCR text extraction",
                    "Object detection",
                    "Color analysis",
                    "Text region detection",
                    "Screen text search"
                ]
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Vision info failed: {str(e)}"}
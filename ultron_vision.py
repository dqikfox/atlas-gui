"""
ULTRON Vision System - Complete OCR and Image Analysis
Omnipotent visual processing capabilities for the ULTRON Agent
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import logging
import os
import time
import base64
import io
import json
import asyncio
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import tempfile
import threading
import queue

logger = logging.getLogger(__name__)

class UltronVision:
    def __init__(self):
        """Initialize ULTRON vision system with omnipotent capabilities"""
        self.enabled = True
        
        # Advanced OCR configurations for different scenarios
        self.ocr_configs = {
            'default': r'--oem 3 --psm 6',
            'single_line': r'--oem 3 --psm 7',
            'single_word': r'--oem 3 --psm 8',
            'single_char': r'--oem 3 --psm 10',
            'sparse_text': r'--oem 3 --psm 11',
            'dense_text': r'--oem 3 --psm 6',
            'vertical_text': r'--oem 3 --psm 5',
            'numbers_only': r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789',
            'letters_only': r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        }
        
        # Image enhancement settings
        self.enhancement_settings = {
            'contrast': 1.5,
            'brightness': 1.2,
            'sharpness': 1.3,
            'color': 1.0
        }
        
        # Screen monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self.screen_changes = queue.Queue()
        
        # Configure OCR engines
        self._setup_ocr_engines()
        
        logger.info("ULTRON Vision System initialized with omnipotent capabilities")
    
    def _setup_ocr_engines(self):
        """Configure Tesseract OCR for ULTRON precision"""
        try:
            # Windows Tesseract paths
            if os.name == 'nt':
                possible_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    r'C:\Users\Administrator\AppData\Local\Tesseract-OCR\tesseract.exe',
                    r'C:\tesseract\tesseract.exe'
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        logger.info(f"Tesseract configured at: {path}")
                        break
                else:
                    logger.warning("Tesseract not found in standard locations")
            
            # Test OCR functionality
            self._test_ocr_capability()
            
        except Exception as e:
            logger.error(f"OCR engine setup failed: {e}")
            self.enabled = False
    
    def _test_ocr_capability(self):
        """Test OCR functionality with sample image"""
        try:
            # Create test image with text
            test_img = Image.new('RGB', (200, 50), color='white')
            draw = ImageDraw.Draw(test_img)
            draw.text((10, 10), "ULTRON TEST", fill='black')
            
            # Test OCR
            result = pytesseract.image_to_string(test_img)
            if "ULTRON" in result or "TEST" in result:
                logger.info("OCR capability verified")
                return True
            else:
                logger.warning("OCR test failed - may have limited functionality")
                return False
                
        except Exception as e:
            logger.warning(f"OCR test failed: {e}")
            return False
    
    async def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None,
                           save_path: Optional[str] = None) -> Dict[str, Any]:
        """Capture screen with ULTRON precision"""
        try:
            if region:
                # Capture specific region (left, top, width, height)
                screenshot = pyautogui.screenshot(region=region)
            else:
                # Capture full screen
                screenshot = pyautogui.screenshot()
            
            # Save if path provided
            if save_path:
                screenshot.save(save_path)
            
            # Convert to various formats for processing
            img_array = np.array(screenshot)
            img_cv2 = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Get image statistics
            height, width = img_array.shape[:2]
            file_size = len(screenshot.tobytes()) if not save_path else os.path.getsize(save_path)
            
            return {
                "status": "success",
                "message": "Screen captured with ULTRON precision",
                "image": screenshot,
                "image_array": img_array,
                "opencv_image": img_cv2,
                "dimensions": {"width": width, "height": height},
                "file_size": file_size,
                "save_path": save_path,
                "region": region
            }
            
        except Exception as e:
            return {"error": f"Screen capture failed: {str(e)}"}
    
    async def enhanced_ocr(self, image_input, 
                          ocr_mode: str = 'default',
                          enhance_image: bool = True,
                          multi_engine: bool = True) -> Dict[str, Any]:
        """Advanced OCR with multiple engines and enhancement"""
        try:
            # Handle different input types
            if isinstance(image_input, str):
                # File path
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                # PIL Image
                image = image_input
            elif isinstance(image_input, np.ndarray):
                # NumPy array
                image = Image.fromarray(image_input)
            else:
                return {"error": "Unsupported image input type"}
            
            results = {}
            
            # Image enhancement for better OCR
            if enhance_image:
                enhanced_image = self._enhance_image_for_ocr(image)
            else:
                enhanced_image = image
            
            # Primary Tesseract OCR
            try:
                config = self.ocr_configs.get(ocr_mode, self.ocr_configs['default'])
                
                # Extract text with confidence data
                text_data = pytesseract.image_to_data(enhanced_image, config=config, output_type=pytesseract.Output.DICT)
                
                # Process results
                text_blocks = []
                full_text = ""
                
                for i in range(len(text_data['text'])):
                    if int(text_data['conf'][i]) > 0:  # Filter out low confidence
                        text_block = {
                            'text': text_data['text'][i],
                            'confidence': int(text_data['conf'][i]),
                            'bbox': {
                                'x': text_data['left'][i],
                                'y': text_data['top'][i],
                                'width': text_data['width'][i],
                                'height': text_data['height'][i]
                            }
                        }
                        text_blocks.append(text_block)
                        full_text += text_data['text'][i] + " "
                
                results['tesseract'] = {
                    'full_text': full_text.strip(),
                    'text_blocks': text_blocks,
                    'word_count': len([block for block in text_blocks if block['text'].strip()]),
                    'avg_confidence': np.mean([block['confidence'] for block in text_blocks if block['text'].strip()] or [0])
                }
                
            except Exception as e:
                results['tesseract'] = {'error': str(e)}
            
            # Alternative processing methods
            if multi_engine:
                # Simple text extraction
                try:
                    simple_text = pytesseract.image_to_string(enhanced_image)
                    results['simple'] = {'text': simple_text.strip()}
                except Exception as e:
                    results['simple'] = {'error': str(e)}
                
                # Character-level analysis
                try:
                    char_boxes = pytesseract.image_to_boxes(enhanced_image)
                    results['character_analysis'] = {'char_boxes': char_boxes}
                except Exception as e:
                    results['character_analysis'] = {'error': str(e)}
            
            # Image analysis
            image_stats = self._analyze_image(enhanced_image)
            
            return {
                "status": "success",
                "message": "ULTRON OCR analysis complete",
                "ocr_results": results,
                "image_stats": image_stats,
                "enhancement_applied": enhance_image,
                "ocr_mode": ocr_mode
            }
            
        except Exception as e:
            return {"error": f"OCR analysis failed: {str(e)}"}
    
    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image for optimal OCR performance"""
        try:
            # Convert to grayscale for better OCR
            if image.mode != 'L':
                enhanced = image.convert('L')
            else:
                enhanced = image.copy()
            
            # Apply enhancements
            enhanced = ImageEnhance.Contrast(enhanced).enhance(self.enhancement_settings['contrast'])
            enhanced = ImageEnhance.Brightness(enhanced).enhance(self.enhancement_settings['brightness'])
            enhanced = ImageEnhance.Sharpness(enhanced).enhance(self.enhancement_settings['sharpness'])
            
            # Apply filters for text clarity
            enhanced = enhanced.filter(ImageFilter.MedianFilter(size=3))
            enhanced = enhanced.filter(ImageFilter.SHARPEN)
            
            # Threshold for binary image (black text on white background)
            enhanced_array = np.array(enhanced)
            threshold = np.mean(enhanced_array)
            binary = np.where(enhanced_array > threshold, 255, 0).astype(np.uint8)
            enhanced = Image.fromarray(binary)
            
            return enhanced
            
        except Exception as e:
            logger.warning(f"Image enhancement failed: {e}")
            return image
    
    def _analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image properties for ULTRON intelligence"""
        try:
            img_array = np.array(image)
            
            # Basic statistics
            height, width = img_array.shape[:2] if len(img_array.shape) > 1 else (img_array.shape[0], 1)
            
            stats = {
                "dimensions": {"width": width, "height": height},
                "mode": image.mode,
                "format": getattr(image, 'format', 'Unknown'),
                "size_bytes": len(image.tobytes())
            }
            
            # Color analysis
            if len(img_array.shape) == 3:  # Color image
                stats["color_channels"] = img_array.shape[2]
                stats["mean_rgb"] = [float(np.mean(img_array[:,:,i])) for i in range(img_array.shape[2])]
            else:  # Grayscale
                stats["mean_intensity"] = float(np.mean(img_array))
                stats["contrast"] = float(np.std(img_array))
            
            # Edge detection for text analysis
            if image.mode == 'L':
                edges = cv2.Canny(img_array, 50, 150)
                stats["edge_density"] = float(np.sum(edges > 0) / edges.size)
            
            return stats
            
        except Exception as e:
            return {"error": f"Image analysis failed: {e}"}
    
    async def find_text_on_screen(self, target_text: str, 
                                 region: Optional[Tuple[int, int, int, int]] = None,
                                 case_sensitive: bool = False) -> Dict[str, Any]:
        """Find specific text on screen with ULTRON precision"""
        try:
            # Capture screen
            capture_result = await self.capture_screen(region=region)
            if "error" in capture_result:
                return capture_result
            
            # Perform OCR
            ocr_result = await self.enhanced_ocr(capture_result["image"])
            if "error" in ocr_result:
                return ocr_result
            
            # Search for target text
            matches = []
            
            if "tesseract" in ocr_result["ocr_results"]:
                text_blocks = ocr_result["ocr_results"]["tesseract"].get("text_blocks", [])
                
                for block in text_blocks:
                    text = block["text"]
                    if not case_sensitive:
                        text = text.lower()
                        search_text = target_text.lower()
                    else:
                        search_text = target_text
                    
                    if search_text in text:
                        match = {
                            "found_text": block["text"],
                            "confidence": block["confidence"],
                            "position": block["bbox"],
                            "center": {
                                "x": block["bbox"]["x"] + block["bbox"]["width"] // 2,
                                "y": block["bbox"]["y"] + block["bbox"]["height"] // 2
                            }
                        }
                        matches.append(match)
            
            return {
                "status": "success",
                "message": f"Text search complete. Found {len(matches)} matches.",
                "target_text": target_text,
                "matches": matches,
                "total_matches": len(matches),
                "region_searched": region
            }
            
        except Exception as e:
            return {"error": f"Text search failed: {str(e)}"}
    
    async def click_on_text(self, target_text: str,
                          region: Optional[Tuple[int, int, int, int]] = None,
                          click_offset: Tuple[int, int] = (0, 0)) -> Dict[str, Any]:
        """Find and click on specific text with ULTRON precision"""
        try:
            # Find text on screen
            search_result = await self.find_text_on_screen(target_text, region)
            
            if "error" in search_result:
                return search_result
            
            if search_result["total_matches"] == 0:
                return {"error": f"Text '{target_text}' not found on screen"}
            
            # Click on first match
            first_match = search_result["matches"][0]
            click_x = first_match["center"]["x"] + click_offset[0]
            click_y = first_match["center"]["y"] + click_offset[1]
            
            # Perform click with PyAutoGUI
            pyautogui.click(click_x, click_y)
            
            return {
                "status": "success",
                "message": f"Clicked on '{target_text}' at ({click_x}, {click_y})",
                "clicked_position": {"x": click_x, "y": click_y},
                "text_confidence": first_match["confidence"],
                "total_matches_found": search_result["total_matches"]
            }
            
        except Exception as e:
            return {"error": f"Click on text failed: {str(e)}"}
    
    async def monitor_screen_changes(self, callback=None, 
                                   region: Optional[Tuple[int, int, int, int]] = None,
                                   threshold: float = 0.1) -> Dict[str, Any]:
        """Monitor screen for changes with ULTRON vigilance"""
        try:
            if self.monitoring_active:
                return {"error": "Screen monitoring already active"}
            
            self.monitoring_active = True
            
            def monitoring_thread():
                previous_image = None
                
                while self.monitoring_active:
                    try:
                        # Capture current screen
                        current_capture = pyautogui.screenshot(region=region)
                        current_array = np.array(current_capture)
                        
                        if previous_image is not None:
                            # Calculate difference
                            diff = np.abs(current_array.astype(float) - previous_image.astype(float))
                            change_percentage = np.mean(diff) / 255.0
                            
                            if change_percentage > threshold:
                                change_data = {
                                    "timestamp": time.time(),
                                    "change_percentage": change_percentage,
                                    "region": region,
                                    "image": current_capture
                                }
                                
                                self.screen_changes.put(change_data)
                                
                                if callback:
                                    threading.Thread(
                                        target=callback,
                                        args=(change_data,),
                                        daemon=True
                                    ).start()
                        
                        previous_image = current_array
                        time.sleep(0.1)  # 10 FPS monitoring
                        
                    except Exception as e:
                        logger.error(f"Monitoring thread error: {e}")
                        time.sleep(1)
            
            self.monitor_thread = threading.Thread(target=monitoring_thread, daemon=True)
            self.monitor_thread.start()
            
            return {
                "status": "success",
                "message": "ULTRON screen monitoring activated",
                "monitoring": True,
                "threshold": threshold,
                "region": region
            }
            
        except Exception as e:
            return {"error": f"Screen monitoring failed: {str(e)}"}
    
    async def stop_screen_monitoring(self) -> Dict[str, Any]:
        """Stop ULTRON screen monitoring"""
        self.monitoring_active = False
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        
        return {
            "status": "success",
            "message": "ULTRON screen monitoring deactivated",
            "monitoring": False
        }
    
    async def analyze_ui_elements(self, image_input) -> Dict[str, Any]:
        """Analyze UI elements with ULTRON intelligence"""
        try:
            # Handle input
            if isinstance(image_input, str):
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                image = image_input
            else:
                capture_result = await self.capture_screen()
                if "error" in capture_result:
                    return capture_result
                image = capture_result["image"]
            
            # Convert to OpenCV format
            img_array = np.array(image)
            img_cv2 = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            
            # Detect UI elements
            ui_elements = {}
            
            # Button detection (rectangles)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            rectangles = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Filter small elements
                    x, y, w, h = cv2.boundingRect(contour)
                    rectangles.append({
                        "type": "rectangle",
                        "bbox": {"x": x, "y": y, "width": w, "height": h},
                        "area": area,
                        "aspect_ratio": w / h if h > 0 else 0
                    })
            
            ui_elements["rectangles"] = rectangles
            
            # Line detection
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
            if lines is not None:
                line_elements = []
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    line_elements.append({
                        "type": "line",
                        "start": {"x": x1, "y": y1},
                        "end": {"x": x2, "y": y2},
                        "length": length
                    })
                ui_elements["lines"] = line_elements
            
            # Circle detection
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=100)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                circle_elements = []
                for (x, y, r) in circles:
                    circle_elements.append({
                        "type": "circle",
                        "center": {"x": x, "y": y},
                        "radius": r,
                        "area": np.pi * r * r
                    })
                ui_elements["circles"] = circle_elements
            
            return {
                "status": "success",
                "message": "ULTRON UI element analysis complete",
                "ui_elements": ui_elements,
                "total_elements": sum(len(elements) if isinstance(elements, list) else 0 for elements in ui_elements.values()),
                "analysis_timestamp": time.time()
            }
            
        except Exception as e:
            return {"error": f"UI element analysis failed: {str(e)}"}
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive ULTRON vision system status"""
        return {
            "enabled": self.enabled,
            "monitoring_active": self.monitoring_active,
            "monitor_thread_active": self.monitor_thread is not None and self.monitor_thread.is_alive(),
            "screen_changes_queued": self.screen_changes.qsize(),
            "ocr_engines": ["tesseract"],
            "available_modes": list(self.ocr_configs.keys()),
            "enhancement_settings": self.enhancement_settings,
            "omnipotence_level": "MAXIMUM_VISUAL_PROCESSING"
        }
    
    def __del__(self):
        """Cleanup ULTRON vision resources"""
        try:
            if self.monitoring_active:
                asyncio.run(self.stop_screen_monitoring())
        except:
            pass
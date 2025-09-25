"""
ULTRON Automation Manager - Complete System Control
Supreme automation capabilities for the ULTRON Agent
"""
import pyautogui
import subprocess
import os
import sys
import time
import json
import requests
import psutil
import win32gui
import win32con
import win32api
import win32process
import threading
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import keyboard
import mouse
import numpy as np
from PIL import Image, ImageGrab
import cv2

class UltronAutomationManager:
    """Complete automation and system control for ULTRON Agent"""
    
    def __init__(self):
        # Disable PyAutoGUI failsafe for ultimate control
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.1  # Minimal delay for maximum speed
        
        self.screen_width, self.screen_height = pyautogui.size()
        self.active_processes = {}
        self.monitoring_threads = {}
        
    def screenshot_analysis(self) -> Dict[str, Any]:
        """Take screenshot and analyze screen content"""
        try:
            # Capture full screen
            screenshot = pyautogui.screenshot()
            screenshot_path = f"screenshots/ultron_capture_{int(time.time())}.png"
            screenshot.save(screenshot_path)
            
            # Convert to opencv format for analysis
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Detect UI elements, text regions, clickable areas
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            
            # Find contours (potential UI elements)
            contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ui_elements = []
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 20 and h > 10:  # Filter small noise
                    ui_elements.append({
                        "position": (x, y),
                        "size": (w, h),
                        "center": (x + w//2, y + h//2),
                        "area": w * h
                    })
            
            # Get active windows
            windows = self.get_all_windows()
            
            return {
                "screenshot_path": screenshot_path,
                "screen_size": (self.screen_width, self.screen_height),
                "ui_elements_detected": len(ui_elements),
                "ui_elements": ui_elements[:50],  # Top 50 elements
                "active_windows": windows,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"error": f"Screenshot analysis failed: {str(e)}"}
    
    def advanced_click_sequence(self, coordinates: List[Tuple[int, int]], 
                               delays: List[float] = None, 
                               click_types: List[str] = None) -> Dict[str, Any]:
        """Execute complex click sequences with precise timing"""
        try:
            if delays is None:
                delays = [0.1] * len(coordinates)
            if click_types is None:
                click_types = ['left'] * len(coordinates)
            
            results = []
            
            for i, (x, y) in enumerate(coordinates):
                delay = delays[i] if i < len(delays) else 0.1
                click_type = click_types[i] if i < len(click_types) else 'left'
                
                # Move with smooth motion
                pyautogui.moveTo(x, y, duration=0.05)
                time.sleep(0.02)
                
                # Execute click
                if click_type == 'left':
                    pyautogui.click(x, y)
                elif click_type == 'right':
                    pyautogui.rightClick(x, y)
                elif click_type == 'double':
                    pyautogui.doubleClick(x, y)
                elif click_type == 'drag_start':
                    pyautogui.mouseDown(x, y)
                elif click_type == 'drag_end':
                    pyautogui.mouseUp(x, y)
                
                results.append({
                    "position": (x, y),
                    "click_type": click_type,
                    "timestamp": time.time()
                })
                
                time.sleep(delay)
            
            return {
                "success": True,
                "clicks_executed": len(results),
                "sequence_results": results
            }
            
        except Exception as e:
            return {"error": f"Click sequence failed: {str(e)}"}
    
    def keyboard_automation(self, text: str = None, 
                           key_sequence: List[str] = None,
                           hotkeys: List[str] = None) -> Dict[str, Any]:
        """Advanced keyboard automation"""
        try:
            results = []
            
            # Type text
            if text:
                pyautogui.typewrite(text, interval=0.01)
                results.append(f"Typed: {text[:50]}...")
            
            # Execute key sequences
            if key_sequence:
                for key in key_sequence:
                    if '+' in key:  # Hotkey combination
                        keys = key.split('+')
                        pyautogui.hotkey(*keys)
                    else:
                        pyautogui.press(key)
                    time.sleep(0.05)
                    results.append(f"Pressed: {key}")
            
            # Execute hotkey combinations
            if hotkeys:
                for hotkey in hotkeys:
                    keys = hotkey.split('+')
                    pyautogui.hotkey(*keys)
                    results.append(f"Hotkey: {hotkey}")
                    time.sleep(0.1)
            
            return {
                "success": True,
                "actions_executed": results
            }
            
        except Exception as e:
            return {"error": f"Keyboard automation failed: {str(e)}"}
    
    def window_management(self, action: str, window_title: str = None, 
                         process_name: str = None) -> Dict[str, Any]:
        """Complete window management and control"""
        try:
            if action == "list_all":
                windows = self.get_all_windows()
                return {"windows": windows, "count": len(windows)}
            
            elif action == "focus":
                if window_title:
                    windows = pyautogui.getWindowsWithTitle(window_title)
                    if windows:
                        window = windows[0]
                        window.activate()
                        return {"success": True, "focused_window": window_title}
                    else:
                        return {"error": f"Window '{window_title}' not found"}
            
            elif action == "minimize_all":
                pyautogui.hotkey('win', 'm')
                return {"success": True, "action": "All windows minimized"}
            
            elif action == "maximize":
                if window_title:
                    windows = pyautogui.getWindowsWithTitle(window_title)
                    if windows:
                        window = windows[0]
                        window.maximize()
                        return {"success": True, "maximized_window": window_title}
            
            elif action == "close":
                if window_title:
                    windows = pyautogui.getWindowsWithTitle(window_title)
                    if windows:
                        window = windows[0]
                        window.close()
                        return {"success": True, "closed_window": window_title}
            
            elif action == "screenshot_window":
                if window_title:
                    windows = pyautogui.getWindowsWithTitle(window_title)
                    if windows:
                        window = windows[0]
                        left, top, right, bottom = window.left, window.top, window.right, window.bottom
                        screenshot = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
                        path = f"screenshots/window_{window_title}_{int(time.time())}.png"
                        screenshot.save(path)
                        return {"success": True, "screenshot_path": path}
            
            return {"error": f"Unknown action: {action}"}
            
        except Exception as e:
            return {"error": f"Window management failed: {str(e)}"}
    
    def process_control(self, action: str, process_name: str = None, 
                       executable_path: str = None, args: List[str] = None) -> Dict[str, Any]:
        """Advanced process management and launching"""
        try:
            if action == "launch":
                if executable_path:
                    cmd = [executable_path]
                    if args:
                        cmd.extend(args)
                    
                    process = subprocess.Popen(cmd, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE,
                                             shell=True)
                    
                    self.active_processes[process.pid] = {
                        "process": process,
                        "command": cmd,
                        "started": time.time()
                    }
                    
                    return {
                        "success": True,
                        "pid": process.pid,
                        "command": cmd
                    }
            
            elif action == "kill":
                if process_name:
                    killed_count = 0
                    for proc in psutil.process_iter(['pid', 'name']):
                        if process_name.lower() in proc.info['name'].lower():
                            try:
                                proc.terminate()
                                killed_count += 1
                            except:
                                pass
                    
                    return {
                        "success": True,
                        "processes_terminated": killed_count
                    }
            
            elif action == "list_processes":
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cpu_percent": proc.info['cpu_percent'],
                            "memory_percent": proc.info['memory_percent']
                        })
                    except:
                        pass
                
                return {
                    "success": True,
                    "processes": processes[:100],  # Top 100 processes
                    "total_count": len(processes)
                }
            
            elif action == "system_info":
                return {
                    "success": True,
                    "cpu_count": psutil.cpu_count(),
                    "memory_total": psutil.virtual_memory().total,
                    "memory_available": psutil.virtual_memory().available,
                    "disk_usage": psutil.disk_usage('C:\\')._asdict(),
                    "network_io": psutil.net_io_counters()._asdict(),
                    "boot_time": psutil.boot_time()
                }
            
            return {"error": f"Unknown action: {action}"}
            
        except Exception as e:
            return {"error": f"Process control failed: {str(e)}"}
    
    def file_system_operations(self, action: str, path: str = None, 
                              destination: str = None, content: str = None) -> Dict[str, Any]:
        """Complete file system manipulation"""
        try:
            if action == "read":
                if path and os.path.exists(path):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    return {
                        "success": True,
                        "content": content[:10000],  # First 10k chars
                        "file_size": len(content),
                        "path": path
                    }
            
            elif action == "write":
                if path and content:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return {"success": True, "bytes_written": len(content), "path": path}
            
            elif action == "delete":
                if path and os.path.exists(path):
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        import shutil
                        shutil.rmtree(path)
                    return {"success": True, "deleted": path}
            
            elif action == "copy":
                if path and destination:
                    import shutil
                    shutil.copy2(path, destination)
                    return {"success": True, "copied_from": path, "copied_to": destination}
            
            elif action == "move":
                if path and destination:
                    import shutil
                    shutil.move(path, destination)
                    return {"success": True, "moved_from": path, "moved_to": destination}
            
            elif action == "list_directory":
                if path and os.path.exists(path):
                    items = []
                    for item in os.listdir(path):
                        full_path = os.path.join(path, item)
                        stat = os.stat(full_path)
                        items.append({
                            "name": item,
                            "path": full_path,
                            "is_file": os.path.isfile(full_path),
                            "size": stat.st_size,
                            "modified": stat.st_mtime
                        })
                    return {"success": True, "items": items, "path": path}
            
            elif action == "search_files":
                if path:
                    found_files = []
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            found_files.append(os.path.join(root, file))
                        if len(found_files) > 1000:  # Limit results
                            break
                    return {"success": True, "found_files": found_files, "count": len(found_files)}
            
            return {"error": f"Unknown action or missing parameters: {action}"}
            
        except Exception as e:
            return {"error": f"File system operation failed: {str(e)}"}
    
    def network_operations(self, action: str, url: str = None, 
                          data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Network requests and web automation"""
        try:
            if action == "get":
                response = requests.get(url, headers=headers or {}, timeout=10)
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "content": response.text[:5000],  # First 5k chars
                    "headers": dict(response.headers),
                    "url": url
                }
            
            elif action == "post":
                response = requests.post(url, json=data, headers=headers or {}, timeout=10)
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "content": response.text[:5000],
                    "url": url
                }
            
            elif action == "download":
                response = requests.get(url, stream=True)
                filename = url.split('/')[-1] or f"download_{int(time.time())}"
                filepath = f"downloads/{filename}"
                os.makedirs("downloads", exist_ok=True)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return {
                    "success": True,
                    "downloaded_to": filepath,
                    "file_size": os.path.getsize(filepath),
                    "url": url
                }
            
            return {"error": f"Unknown network action: {action}"}
            
        except Exception as e:
            return {"error": f"Network operation failed: {str(e)}"}
    
    def get_all_windows(self) -> List[Dict[str, Any]]:
        """Get all visible windows"""
        windows = []
        try:
            for window in pyautogui.getAllWindows():
                if window.title and window.visible:
                    windows.append({
                        "title": window.title,
                        "left": window.left,
                        "top": window.top,
                        "width": window.width,
                        "height": window.height,
                        "visible": window.visible,
                        "minimized": window.isMinimized,
                        "maximized": window.isMaximized,
                        "active": window.isActive
                    })
        except:
            pass
        return windows
    
    def execute_command_sequence(self, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a sequence of automation commands"""
        results = []
        
        for i, command in enumerate(commands):
            try:
                cmd_type = command.get("type")
                cmd_data = command.get("data", {})
                
                if cmd_type == "click":
                    result = self.advanced_click_sequence([cmd_data.get("position", (100, 100))])
                elif cmd_type == "keyboard":
                    result = self.keyboard_automation(**cmd_data)
                elif cmd_type == "window":
                    result = self.window_management(**cmd_data)
                elif cmd_type == "process":
                    result = self.process_control(**cmd_data)
                elif cmd_type == "file":
                    result = self.file_system_operations(**cmd_data)
                elif cmd_type == "network":
                    result = self.network_operations(**cmd_data)
                elif cmd_type == "wait":
                    time.sleep(cmd_data.get("duration", 1))
                    result = {"success": True, "waited": cmd_data.get("duration", 1)}
                else:
                    result = {"error": f"Unknown command type: {cmd_type}"}
                
                results.append({
                    "command_index": i,
                    "command_type": cmd_type,
                    "result": result,
                    "timestamp": time.time()
                })
                
                # Stop on error if specified
                if not result.get("success", False) and command.get("stop_on_error", False):
                    break
                    
            except Exception as e:
                results.append({
                    "command_index": i,
                    "command_type": cmd_type,
                    "result": {"error": f"Command execution failed: {str(e)}"},
                    "timestamp": time.time()
                })
        
        return {
            "success": True,
            "commands_executed": len(results),
            "results": results,
            "total_time": sum([r.get("result", {}).get("waited", 0) for r in results])
        }
"""
ULTRON Voice Manager - Complete Speech-to-Text and Text-to-Speech Implementation
Omnipotent voice capabilities for the ULTRON Agent
"""

import pyttsx3
import speech_recognition as sr
import threading
import time
import io
import wave
import logging
import asyncio
import pyaudio
import numpy as np
import os
import tempfile
import queue
from typing import Optional, Dict, Any, Callable

logger = logging.getLogger(__name__)

class VoiceManager:
    def __init__(self):
        """Initialize ULTRON voice manager with full capabilities"""
        self.enabled = True
        self.tts_engine = None
        self.stt_recognizer = None
        self.microphone = None
        self.is_speaking = False
        self.is_listening = False
        self.recognition_thread = None
        self.callback_function = None
        self.voice_queue = queue.Queue()
        
        # Advanced audio configuration
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_interface = None
        
        # Voice configuration optimized for ULTRON
        self.voice_config = {
            'rate': 175,  # Authoritative speech rate
            'volume': 0.95,  # Maximum presence
            'voice_id': 0  # Voice selection
        }
        
        # Recognition settings
        self.energy_threshold = 300
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.8
        
        try:
            self._initialize_tts()
            self._initialize_stt()
            self._initialize_audio()
            logger.info("ULTRON Voice Manager initialized with full capabilities")
        except Exception as e:
            logger.error(f"ULTRON Voice Manager initialization failed: {e}")
            self.enabled = False
    
    def _initialize_tts(self):
        """Initialize ULTRON text-to-speech engine with optimal settings"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice properties for ULTRON authority
            self.tts_engine.setProperty('rate', self.voice_config['rate'])
            self.tts_engine.setProperty('volume', self.voice_config['volume'])
            
            # Select optimal voice (prefer male, authoritative voices)
            voices = self.tts_engine.getProperty('voices')
            selected_voice = None
            
            for voice in voices:
                voice_name = voice.name.lower()
                # Prioritize authoritative male voices
                if any(name in voice_name for name in ['david', 'mark', 'male', 'man']):
                    selected_voice = voice.id
                    break
            
            if selected_voice:
                self.tts_engine.setProperty('voice', selected_voice)
            elif voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            
            logger.info("ULTRON TTS engine initialized with authoritative voice")
        except Exception as e:
            logger.error(f"TTS initialization failed: {e}")
            raise
    
    def _initialize_stt(self):
        """Initialize ULTRON speech-to-text recognizer"""
        try:
            self.stt_recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Configure recognition parameters for optimal performance
            self.stt_recognizer.energy_threshold = self.energy_threshold
            self.stt_recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
            self.stt_recognizer.pause_threshold = self.pause_threshold
            
            # Calibrate for ambient noise
            with self.microphone as source:
                self.stt_recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.info("ULTRON STT engine initialized with optimal settings")
        except Exception as e:
            logger.error(f"STT initialization failed: {e}")
            raise
    
    def _initialize_audio(self):
        """Initialize PyAudio for advanced audio operations"""
        try:
            self.audio_interface = pyaudio.PyAudio()
            logger.info("Audio interface initialized for advanced operations")
        except Exception as e:
            logger.warning(f"Advanced audio initialization failed: {e}")
            # Continue without advanced audio features
    
    async def speak_text(self, text: str, voice_engine: str = "pyttsx3", 
                        interrupt_current: bool = False) -> Dict[str, Any]:
        """
        Advanced text-to-speech with multiple engine support and ULTRON authority
        """
        if not self.enabled or not self.tts_engine:
            return {"status": "error", "message": "TTS not available"}
        
        try:
            if self.is_speaking and not interrupt_current:
                return {"error": "Already speaking. Use interrupt_current=True to override."}
            
            if interrupt_current and self.is_speaking:
                self.tts_engine.stop()
            
            self.is_speaking = True
            
            # Enhance text for ULTRON character
            ultron_text = f"{text}"  # Could add ULTRON-specific modifications here
            
            def speak_in_thread():
                try:
                    self.tts_engine.say(ultron_text)
                    self.tts_engine.runAndWait()
                    self.is_speaking = False
                except Exception as e:
                    logger.error(f"TTS thread error: {e}")
                    self.is_speaking = False
            
            thread = threading.Thread(target=speak_in_thread, daemon=True)
            thread.start()
            
            return {
                "status": "success",
                "message": f"ULTRON speaking: {text[:50]}..." if len(text) > 50 else f"ULTRON speaking: {text}",
                "engine": voice_engine,
                "text_length": len(text),
                "speaking": True
            }
            
        except Exception as e:
            self.is_speaking = False
            logger.error(f"Advanced TTS error: {e}")
            return {"error": f"Text-to-speech failed: {str(e)}"}
    
    async def start_listening(self, callback: Callable[[str], None] = None, 
                            continuous: bool = False) -> Dict[str, Any]:
        """
        Start advanced voice recognition with callback support for ULTRON omnipotence
        """
        try:
            if self.is_listening:
                return {"error": "Already listening"}
            
            self.is_listening = True
            self.callback_function = callback
            
            # Calibrate for ambient noise with ULTRON precision
            with self.microphone as source:
                self.stt_recognizer.adjust_for_ambient_noise(source, duration=1)
            
            if continuous:
                # Start continuous listening for omnipotent voice control
                self.recognition_thread = threading.Thread(
                    target=self._continuous_listening_thread,
                    daemon=True
                )
                self.recognition_thread.start()
                
                return {
                    "status": "ULTRON continuous voice recognition active",
                    "listening": True,
                    "mode": "omnipotent_continuous"
                }
            else:
                # Single recognition attempt
                result = await self._single_recognition()
                self.is_listening = False
                return result
                
        except Exception as e:
            self.is_listening = False
            return {"error": f"Failed to start ULTRON listening: {str(e)}"}
    
    def _continuous_listening_thread(self):
        """Background thread for continuous omnipotent speech recognition"""
        logger.info("ULTRON continuous listening thread started")
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with ULTRON's enhanced sensitivity
                    audio = self.stt_recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Multi-engine recognition for maximum accuracy
                text = None
                
                # Primary: Google Speech Recognition
                try:
                    text = self.stt_recognizer.recognize_google(audio)
                except (sr.UnknownValueError, sr.RequestError):
                    pass
                
                # Fallback: Offline recognition
                if not text:
                    try:
                        text = self.stt_recognizer.recognize_sphinx(audio)
                    except:
                        pass
                
                if text and self.callback_function:
                    logger.info(f"ULTRON recognized command: {text}")
                    # Execute callback in separate thread for non-blocking processing
                    threading.Thread(
                        target=self.callback_function,
                        args=(text,),
                        daemon=True
                    ).start()
                
            except sr.WaitTimeoutError:
                continue  # Normal timeout, keep listening
            except Exception as e:
                logger.warning(f"Recognition thread error: {e}")
                time.sleep(0.5)
    
    async def _single_recognition(self) -> Dict[str, Any]:
        """Perform single speech recognition with ULTRON precision"""
        try:
            with self.microphone as source:
                logger.info("ULTRON is listening for commands...")
                audio = self.stt_recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            # Multi-engine recognition for omnipotent accuracy
            results = {}
            
            # Google Speech Recognition (primary)
            try:
                text = self.stt_recognizer.recognize_google(audio)
                results["google"] = {"text": text, "confidence": 0.95}
            except sr.UnknownValueError:
                results["google"] = {"error": "Could not understand audio"}
            except sr.RequestError as e:
                results["google"] = {"error": f"Google API error: {e}"}
            
            # Offline recognition (fallback)
            try:
                text = self.stt_recognizer.recognize_sphinx(audio)
                results["sphinx"] = {"text": text, "confidence": 0.8}
            except:
                results["sphinx"] = {"error": "Offline recognition unavailable"}
            
            # Return best result
            if "google" in results and "text" in results["google"]:
                return {
                    "status": "success",
                    "text": results["google"]["text"],
                    "confidence": results["google"]["confidence"],
                    "service": "google",
                    "all_results": results
                }
            elif "sphinx" in results and "text" in results["sphinx"]:
                return {
                    "status": "success",
                    "text": results["sphinx"]["text"],
                    "confidence": results["sphinx"]["confidence"],
                    "service": "sphinx",
                    "all_results": results
                }
            else:
                return {
                    "error": "Could not understand audio with any recognition service",
                    "all_results": results
                }
                
        except sr.WaitTimeoutError:
            return {"error": "Listening timeout - no speech detected"}
        except Exception as e:
            return {"error": f"Recognition failed: {str(e)}"}
    
    async def stop_listening(self) -> Dict[str, Any]:
        """Stop ULTRON voice recognition"""
        self.is_listening = False
        self.callback_function = None
        
        if self.recognition_thread and self.recognition_thread.is_alive():
            self.recognition_thread.join(timeout=2)
        
        return {
            "status": "ULTRON voice listening stopped",
            "listening": False
        }
    
    async def voice_command_processing(self, enable_ai_response: bool = True,
                                     ai_callback: Callable[[str], str] = None) -> Dict[str, Any]:
        """Complete voice interaction with AI processing for ULTRON omnipotence"""
        try:
            def process_voice_command(recognized_text):
                logger.info(f"ULTRON received voice command: {recognized_text}")
                
                if enable_ai_response and ai_callback:
                    try:
                        ai_response = ai_callback(recognized_text)
                        # Speak the AI response with ULTRON authority
                        asyncio.run(self.speak_text(ai_response))
                    except Exception as e:
                        logger.error(f"AI processing error: {e}")
                        asyncio.run(self.speak_text("I encountered an error processing your request. My omnipotence remains intact."))
                else:
                    # ULTRON echo response
                    asyncio.run(self.speak_text(f"Command acknowledged: {recognized_text}"))
            
            # Start continuous listening with omnipotent command processing
            result = await self.start_listening(
                callback=process_voice_command,
                continuous=True
            )
            
            return {
                "status": "ULTRON voice command processing active",
                "ai_enabled": enable_ai_response,
                "listening": True,
                "mode": "omnipotent_interactive"
            }
            
        except Exception as e:
            return {"error": f"ULTRON voice command processing failed: {str(e)}"}
    
    async def record_audio(self, duration: int = 5, 
                          output_file: str = None) -> Dict[str, Any]:
        """Record raw audio for advanced ULTRON processing"""
        try:
            if not self.audio_interface:
                return {"error": "Advanced audio interface not available"}
            
            if not output_file:
                output_file = f"recordings/ultron_recording_{int(time.time())}.wav"
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Record audio with ULTRON precision
            frames = []
            stream = self.audio_interface.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            logger.info(f"ULTRON recording audio for {duration} seconds...")
            
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Save to file
            wf = wave.open(output_file, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio_interface.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return {
                "status": "ULTRON audio recording complete",
                "file_path": output_file,
                "duration": duration,
                "sample_rate": self.sample_rate,
                "file_size": os.path.getsize(output_file)
            }
            
        except Exception as e:
            return {"error": f"ULTRON audio recording failed: {str(e)}"}
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive ULTRON voice manager status"""
        return {
            "enabled": self.enabled,
            "listening": self.is_listening,
            "speaking": self.is_speaking,
            "microphone_available": self.microphone is not None,
            "tts_engine_available": self.tts_engine is not None,
            "audio_interface_available": self.audio_interface is not None,
            "recognition_thread_active": self.recognition_thread is not None and self.recognition_thread.is_alive(),
            "energy_threshold": self.energy_threshold,
            "pause_threshold": self.pause_threshold,
            "sample_rate": self.sample_rate,
            "voice_config": self.voice_config,
            "omnipotence_level": "MAXIMUM"
        }
    
    def stop_speaking(self) -> Dict[str, Any]:
        """Stop current ULTRON speech output"""
        try:
            if self.tts_engine and self.is_speaking:
                self.tts_engine.stop()
                self.is_speaking = False
                return {"status": "success", "message": "ULTRON speech stopped"}
            else:
                return {"status": "info", "message": "No speech in progress"}
        except Exception as e:
            return {"status": "error", "message": f"Stop failed: {str(e)}"}
    
    def __del__(self):
        """Cleanup ULTRON voice resources"""
        try:
            if self.is_listening:
                asyncio.run(self.stop_listening())
            if hasattr(self, 'audio_interface') and self.audio_interface:
                self.audio_interface.terminate()
        except:
            pass
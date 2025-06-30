#!/usr/bin/env python3
"""
Robust VBVA Startup Script
Handles all configuration, dependencies, and startup automatically
"""

import os
import sys
import subprocess
import time
import signal
import psutil
import requests
from pathlib import Path
import json

class RobustVBVAStartup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_port = 8000
        self.frontend_port = 8501
        self.backend_process = None
        self.frontend_process = None
        
    def print_status(self, message, status="INFO"):
        """Print formatted status messages"""
        colors = {
            "INFO": "\033[94m",    # Blue
            "SUCCESS": "\033[92m", # Green
            "WARNING": "\033[93m", # Yellow
            "ERROR": "\033[91m",   # Red
            "RESET": "\033[0m"     # Reset
        }
        print(f"{colors.get(status, colors['INFO'])}[{status}]{colors['RESET']} {message}")
    
    def check_dependencies(self):
        """Check and install required dependencies"""
        self.print_status("Checking dependencies...")
        
        # Check if required packages are installed
        required_packages = [
            "fastapi", "uvicorn", "streamlit", "python-dotenv", 
            "pydantic", "pydantic-settings", "requests"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.print_status(f"Installing missing packages: {', '.join(missing_packages)}", "WARNING")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ], check=True, capture_output=True)
                self.print_status("Dependencies installed successfully", "SUCCESS")
            except subprocess.CalledProcessError as e:
                self.print_status(f"Failed to install dependencies: {e}", "ERROR")
                return False
        else:
            self.print_status("All dependencies are installed", "SUCCESS")
        
        return True
    
    def setup_environment(self):
        """Setup environment configuration"""
        self.print_status("Setting up environment...")
        
        # Check if .env file exists
        env_file = self.project_root / ".env"
        if not env_file.exists():
            self.print_status("Creating .env file from template...", "WARNING")
            env_example = self.project_root / "env.example"
            if env_example.exists():
                subprocess.run(["cp", str(env_example), str(env_file)])
                self.print_status("Please configure your API keys in the .env file", "WARNING")
                return False
            else:
                self.print_status("No .env file or template found", "ERROR")
                return False
        
        # Validate .env file format
        try:
            with open(env_file, 'r') as f:
                content = f.read()
            
            # Remove inline comments that might cause issues
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                if '#' in line and '=' in line:
                    # Keep only the part before the comment
                    cleaned_line = line.split('#')[0].strip()
                    if cleaned_line:
                        cleaned_lines.append(cleaned_line)
                else:
                    cleaned_lines.append(line)
            
            # Write back cleaned content
            with open(env_file, 'w') as f:
                f.write('\n'.join(cleaned_lines))
            
            self.print_status("Environment file validated and cleaned", "SUCCESS")
            return True
            
        except Exception as e:
            self.print_status(f"Error setting up environment: {e}", "ERROR")
            return False
    
    def create_directories(self):
        """Create necessary directories"""
        self.print_status("Creating necessary directories...")
        
        directories = [
            "uploads", "cache", "logs", "tmp"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
        
        self.print_status("Directories created", "SUCCESS")
    
    def check_ports(self):
        """Check if required ports are available"""
        self.print_status("Checking port availability...")
        
        ports_to_check = [self.backend_port, self.frontend_port]
        occupied_ports = []
        
        for port in ports_to_check:
            try:
                response = requests.get(f"http://localhost:{port}", timeout=1)
                occupied_ports.append(port)
            except requests.exceptions.RequestException:
                pass
        
        if occupied_ports:
            self.print_status(f"Ports {occupied_ports} are already in use", "WARNING")
            self.print_status("Attempting to kill existing processes...", "WARNING")
            
            for port in occupied_ports:
                try:
                    # Find and kill processes using the port
                    for proc in psutil.process_iter(['pid', 'name', 'connections']):
                        try:
                            for conn in proc.info['connections']:
                                if conn.laddr.port == port:
                                    proc.terminate()
                                    proc.wait(timeout=5)
                                    self.print_status(f"Killed process on port {port}", "SUCCESS")
                        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                            pass
                except Exception as e:
                    self.print_status(f"Error killing process on port {port}: {e}", "ERROR")
        
        self.print_status("Ports are available", "SUCCESS")
    
    def start_backend(self):
        """Start the backend server"""
        self.print_status("Starting backend server...")
        
        try:
            # Change to backend directory and start
            backend_dir = self.project_root / "backend"
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)
            
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
            ], cwd=backend_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for backend to start
            time.sleep(3)
            
            # Check if backend is responding
            try:
                response = requests.get(f"http://localhost:{self.backend_port}/health", timeout=5)
                if response.status_code == 200:
                    self.print_status("Backend started successfully", "SUCCESS")
                    return True
                else:
                    self.print_status("Backend started but health check failed", "WARNING")
                    return True
            except requests.exceptions.RequestException:
                self.print_status("Backend may still be starting up...", "WARNING")
                return True
                
        except Exception as e:
            self.print_status(f"Failed to start backend: {e}", "ERROR")
            return False
    
    def start_frontend(self):
        """Start the frontend server"""
        self.print_status("Starting frontend server...")
        
        try:
            # Change to frontend directory and start
            frontend_dir = self.project_root / "frontend"
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)
            
            self.frontend_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "app.py",
                "--server.port", str(self.frontend_port),
                "--server.headless", "true"
            ], cwd=frontend_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for frontend to start
            time.sleep(5)
            
            # Check if frontend is responding
            try:
                response = requests.get(f"http://localhost:{self.frontend_port}", timeout=5)
                if response.status_code == 200:
                    self.print_status("Frontend started successfully", "SUCCESS")
                    return True
                else:
                    self.print_status("Frontend started but may not be fully ready", "WARNING")
                    return True
            except requests.exceptions.RequestException:
                self.print_status("Frontend may still be starting up...", "WARNING")
                return True
                
        except Exception as e:
            self.print_status(f"Failed to start frontend: {e}", "ERROR")
            return False
    
    def wait_for_services(self):
        """Wait for services to be fully ready"""
        self.print_status("Waiting for services to be ready...")
        
        max_wait = 30  # Maximum wait time in seconds
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            backend_ready = False
            frontend_ready = False
            
            # Check backend
            try:
                response = requests.get(f"http://localhost:{self.backend_port}/health", timeout=2)
                if response.status_code == 200:
                    backend_ready = True
            except:
                pass
            
            # Check frontend
            try:
                response = requests.get(f"http://localhost:{self.frontend_port}", timeout=2)
                if response.status_code == 200:
                    frontend_ready = True
            except:
                pass
            
            if backend_ready and frontend_ready:
                self.print_status("All services are ready!", "SUCCESS")
                return True
            
            time.sleep(1)
        
        self.print_status("Services may not be fully ready, but continuing...", "WARNING")
        return True
    
    def print_status_summary(self):
        """Print final status summary"""
        print("\n" + "="*60)
        self.print_status("VBVA SYSTEM STATUS", "SUCCESS")
        print("="*60)
        
        # Check backend
        try:
            response = requests.get(f"http://localhost:{self.backend_port}/health", timeout=2)
            if response.status_code == 200:
                self.print_status(f"✅ Backend: http://localhost:{self.backend_port}", "SUCCESS")
            else:
                self.print_status(f"⚠️ Backend: http://localhost:{self.backend_port} (unhealthy)", "WARNING")
        except:
            self.print_status(f"❌ Backend: http://localhost:{self.backend_port} (not responding)", "ERROR")
        
        # Check frontend
        try:
            response = requests.get(f"http://localhost:{self.frontend_port}", timeout=2)
            if response.status_code == 200:
                self.print_status(f"✅ Frontend: http://localhost:{self.frontend_port}", "SUCCESS")
            else:
                self.print_status(f"⚠️ Frontend: http://localhost:{self.frontend_port} (unhealthy)", "WARNING")
        except:
            self.print_status(f"❌ Frontend: http://localhost:{self.frontend_port} (not responding)", "ERROR")
        
        print("\n" + "="*60)
        self.print_status("System startup complete!", "SUCCESS")
        self.print_status("Press Ctrl+C to stop all services", "INFO")
        print("="*60)
    
    def cleanup(self):
        """Cleanup processes on exit"""
        self.print_status("Shutting down services...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                self.print_status("Backend stopped", "SUCCESS")
            except:
                self.backend_process.kill()
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                self.print_status("Frontend stopped", "SUCCESS")
            except:
                self.frontend_process.kill()
        
        self.print_status("Cleanup complete", "SUCCESS")
    
    def run(self):
        """Main startup sequence"""
        try:
            self.print_status("🚀 Starting VBVA - Video-Based Virtual Assistant", "SUCCESS")
            print("="*60)
            
            # Step 1: Check dependencies
            if not self.check_dependencies():
                return False
            
            # Step 2: Setup environment
            if not self.setup_environment():
                return False
            
            # Step 3: Create directories
            self.create_directories()
            
            # Step 4: Check ports
            self.check_ports()
            
            # Step 5: Start backend
            if not self.start_backend():
                return False
            
            # Step 6: Start frontend
            if not self.start_frontend():
                return False
            
            # Step 7: Wait for services
            self.wait_for_services()
            
            # Step 8: Print summary
            self.print_status_summary()
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.print_status("Received interrupt signal", "INFO")
            
        except Exception as e:
            self.print_status(f"Startup failed: {e}", "ERROR")
            return False
        finally:
            self.cleanup()
        
        return True

def main():
    """Main entry point"""
    startup = RobustVBVAStartup()
    success = startup.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 
import time
import psutil
import threading
from typing import Dict, List
import json
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass, asdict

@dataclass
class PerformanceMetrics:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    process_threads: int
    active_requests: int
    response_time_ms: float

class PerformanceMonitor:
    def __init__(self, metrics_dir: str = "metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(exist_ok=True)
        self.active_requests = 0
        self.metrics_history: List[PerformanceMetrics] = []
        self.logger = logging.getLogger("performance_monitor")
        
        # Start background monitoring
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._background_monitoring)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _background_monitoring(self):
        """Continuously monitor system metrics."""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Keep last 1000 metrics
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # Save metrics periodically
                self._save_metrics()
                
                time.sleep(60)  # Collect metrics every minute
                
            except Exception as e:
                self.logger.error(f"Error in background monitoring: {str(e)}")
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        return PerformanceMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=psutil.cpu_percent(),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage_percent=psutil.disk_usage('/').percent,
            process_threads=threading.active_count(),
            active_requests=self.active_requests,
            response_time_ms=0.0  # Will be updated per request
        )
    
    def _save_metrics(self):
        """Save metrics to file."""
        try:
            current_date = datetime.now().strftime("%Y%m%d")
            metrics_file = self.metrics_dir / f"metrics_{current_date}.json"
            
            metrics_data = [asdict(m) for m in self.metrics_history]
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving metrics: {str(e)}")
    
    def start_request(self) -> float:
        """Record the start of a request."""
        self.active_requests += 1
        return time.time()
    
    def end_request(self, start_time: float):
        """Record the end of a request and calculate response time."""
        self.active_requests -= 1
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Update latest metrics with response time
        if self.metrics_history:
            self.metrics_history[-1].response_time_ms = response_time
    
    def get_current_metrics(self) -> Dict:
        """Get the current performance metrics."""
        if not self.metrics_history:
            return {}
        return asdict(self.metrics_history[-1])
    
    def get_metrics_summary(self) -> Dict:
        """Get a summary of performance metrics."""
        if not self.metrics_history:
            return {}
        
        response_times = [m.response_time_ms for m in self.metrics_history if m.response_time_ms > 0]
        
        return {
            "avg_response_time_ms": sum(response_times) / len(response_times) if response_times else 0,
            "max_response_time_ms": max(response_times) if response_times else 0,
            "avg_cpu_percent": sum(m.cpu_percent for m in self.metrics_history) / len(self.metrics_history),
            "avg_memory_percent": sum(m.memory_percent for m in self.metrics_history) / len(self.metrics_history),
            "peak_active_requests": max(m.active_requests for m in self.metrics_history)
        }
    
    def stop(self):
        """Stop the monitoring thread."""
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()
        self._save_metrics() 
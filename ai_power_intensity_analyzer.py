#!/usr/bin/env python3
"""
AI Power Intensity Analyzer
Objective-based framework for measuring AI computational intensity
"""

import psutil
import time
from datetime import datetime
from typing import Dict, List, Tuple

class AIPowerIntensityAnalyzer:
    """Analyzes AI computational intensity using objective metrics"""
    
    def __init__(self):
        self.objectives = [
            "cpu_efficiency",
            "memory_utilization", 
            "power_consumption",
            "process_distribution",
            "computational_load",
            "resource_stability",
            "processing_throughput",
            "system_responsiveness",
            "thermal_efficiency",
            "workload_distribution"
        ]
        
    def measure_objective(self, objective: str) -> float:
        """Measure a specific objective metric (0.0-1.0 scale)"""
        if objective == "cpu_efficiency":
            return self._measure_cpu_efficiency()
        elif objective == "memory_utilization":
            return self._measure_memory_utilization()
        elif objective == "power_consumption":
            return self._measure_power_efficiency()
        elif objective == "process_distribution":
            return self._measure_process_distribution()
        elif objective == "computational_load":
            return self._measure_computational_load()
        elif objective == "resource_stability":
            return self._measure_resource_stability()
        elif objective == "processing_throughput":
            return self._measure_processing_throughput()
        elif objective == "system_responsiveness":
            return self._measure_system_responsiveness()
        elif objective == "thermal_efficiency":
            return self._measure_thermal_efficiency()
        elif objective == "workload_distribution":
            return self._measure_workload_distribution()
        else:
            return 0.0
    
    def _measure_cpu_efficiency(self) -> float:
        """Measure CPU efficiency based on load vs utilization"""
        cpu_load = psutil.cpu_percent(interval=0.5)
        # Optimal range is 20-70% for AI workloads
        if 20 <= cpu_load <= 70:
            return 1.0
        elif cpu_load < 20:
            return cpu_load / 20.0
        else:
            return max(0.0, 1.0 - (cpu_load - 70) / 30.0)
    
    def _measure_memory_utilization(self) -> float:
        """Measure memory utilization efficiency"""
        memory = psutil.virtual_memory()
        # Optimal range is 30-80% for AI workloads
        if 30 <= memory.percent <= 80:
            return 1.0
        elif memory.percent < 30:
            return memory.percent / 30.0
        else:
            return max(0.0, 1.0 - (memory.percent - 80) / 20.0)
    
    def _measure_power_efficiency(self) -> float:
        """Measure power consumption efficiency"""
        cpu_load = psutil.cpu_percent(interval=0.1)
        # Estimate power based on load and TDP
        estimated_power = 15 + (cpu_load / 100) * 50  # 15-65W range
        # Lower power for same load is more efficient
        efficiency = max(0.0, 1.0 - estimated_power / 65.0)
        return efficiency
    
    def _measure_process_distribution(self) -> float:
        """Measure how well AI processes are distributed"""
        ai_processes = self._get_ai_processes()
        if not ai_processes:
            return 0.0
        
        # Check if processes are balanced across cores
        cpu_percents = psutil.cpu_percent(interval=0.1, percpu=True)
        max_load = max(cpu_percents)
        min_load = min(cpu_percents)
        
        # Lower imbalance is better
        imbalance = max_load - min_load
        return max(0.0, 1.0 - imbalance / 100.0)
    
    def _measure_computational_load(self) -> float:
        """Measure overall computational intensity"""
        cpu_load = psutil.cpu_percent(interval=0.5)
        memory_load = psutil.virtual_memory().percent
        
        # Combined computational load
        combined_load = (cpu_load + memory_load) / 2.0
        return min(1.0, combined_load / 100.0)
    
    def _measure_resource_stability(self) -> float:
        """Measure stability of resource usage"""
        # Sample multiple times to check stability
        samples = []
        for _ in range(5):
            cpu_load = psutil.cpu_percent(interval=0.1)
            memory_load = psutil.virtual_memory().percent
            samples.append((cpu_load, memory_load))
            time.sleep(0.1)
        
        # Calculate variance
        cpu_variance = sum((s[0] - sum(s[0] for s in samples)/5)**2 for s in samples) / 5
        memory_variance = sum((s[1] - sum(s[1] for s in samples)/5)**2 for s in samples) / 5
        
        # Lower variance = more stable
        stability = max(0.0, 1.0 - (cpu_variance + memory_variance) / 200.0)
        return stability
    
    def _measure_processing_throughput(self) -> float:
        """Estimate processing throughput based on system state"""
        cpu_load = psutil.cpu_percent(interval=0.1)
        memory_available = psutil.virtual_memory().available
        
        # Higher CPU load with available memory = good throughput
        throughput = (cpu_load / 100.0) * (memory_available / (1024**3)) / 100.0
        return min(1.0, throughput)
    
    def _measure_system_responsiveness(self) -> float:
        """Measure system responsiveness"""
        # Check if system is responsive by measuring CPU latency
        start_time = time.time()
        psutil.cpu_percent(interval=0.01)
        latency = time.time() - start_time
        
        # Lower latency = more responsive
        responsiveness = max(0.0, 1.0 - latency * 100)
        return responsiveness
    
    def _measure_thermal_efficiency(self) -> float:
        """Estimate thermal efficiency (simplified)"""
        cpu_load = psutil.cpu_percent(interval=0.1)
        # Higher load at lower estimated temperature = more efficient
        # This is a simplified proxy since we can't directly measure temperature
        thermal_efficiency = cpu_load / 100.0
        return thermal_efficiency
    
    def _measure_workload_distribution(self) -> float:
        """Measure workload distribution across processes"""
        ai_processes = self._get_ai_processes()
        if not ai_processes:
            return 0.0
        
        # Check if AI workload is distributed
        total_ai_cpu = sum(p['cpu_percent'] for p in ai_processes)
        if total_ai_cpu == 0:
            return 0.0
        
        # Even distribution among AI processes
        avg_cpu_per_process = total_ai_cpu / len(ai_processes)
        variance = sum((p['cpu_percent'] - avg_cpu_per_process)**2 for p in ai_processes) / len(ai_processes)
        
        # Lower variance = better distribution
        distribution = max(0.0, 1.0 - variance / 100.0)
        return distribution
    
    def _get_ai_processes(self) -> List[Dict]:
        """Get AI-related processes"""
        ai_names = {"python", "python3", "python.exe", "node", "node.exe", "java", "java.exe"}
        processes = []
        
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                name = (p.info.get("name") or "").lower()
                if name in ai_names:
                    cpu = p.cpu_percent(interval=0.0)
                    processes.append({
                        "pid": p.info["pid"],
                        "name": p.info["name"],
                        "cpu_percent": cpu,
                        "memory_percent": p.info.get("memory_percent", 0.0)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes
    
    def calculate_intensity_score(self) -> Dict[str, float]:
        """Calculate comprehensive AI power intensity score"""
        scores = {}
        total_score = 0.0
        
        for objective in self.objectives:
            score = self.measure_objective(objective)
            scores[objective] = score
            total_score += score
        
        overall_intensity = total_score / len(self.objectives)
        
        return {
            "overall_intensity": overall_intensity,
            "objective_scores": scores,
            "intensity_level": self._classify_intensity(overall_intensity),
            "timestamp": datetime.now().isoformat()
        }
    
    def _classify_intensity(self, score: float) -> str:
        """Classify intensity level"""
        if score >= 0.8:
            return "HIGH_INTENSITY"
        elif score >= 0.6:
            return "MODERATE_INTENSITY"
        elif score >= 0.4:
            return "NORMAL_INTENSITY"
        elif score >= 0.2:
            return "LOW_INTENSITY"
        else:
            return "MINIMAL_INTENSITY"

def main():
    """Main function to demonstrate AI Power Intensity analysis"""
    print("🤖 AI Power Intensity Analyzer")
    print("=" * 50)
    print("Objective-Based Framework for AI Computational Intensity")
    print()
    
    analyzer = AIPowerIntensityAnalyzer()
    
    # Calculate intensity score
    result = analyzer.calculate_intensity_score()
    
    print(f"📊 Overall AI Power Intensity: {result['overall_intensity']:.3f}")
    print(f"🎯 Intensity Level: {result['intensity_level']}")
    print(f"⏰ Timestamp: {result['timestamp']}")
    print()
    
    print("📋 Objective Breakdown:")
    print("-" * 30)
    for objective, score in result['objective_scores'].items():
        status = "✅" if score >= 0.7 else "⚠️" if score >= 0.4 else "❌"
        print(f"{status} {objective}: {score:.3f}")
    
    print()
    print("🔍 Intensity Analysis:")
    intensity = result['overall_intensity']
    if intensity >= 0.8:
        print("🔥 HIGH INTENSITY: AI system operating at maximum computational capacity")
    elif intensity >= 0.6:
        print("⚡ MODERATE INTENSITY: AI system processing complex workloads efficiently")
    elif intensity >= 0.4:
        print("🔄 NORMAL INTENSITY: AI system operating within expected parameters")
    elif intensity >= 0.2:
        print("💤 LOW INTENSITY: AI system processing light workloads")
    else:
        print("😴 MINIMAL INTENSITY: AI system mostly idle")

if __name__ == "__main__":
    main()

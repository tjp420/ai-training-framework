#!/usr/bin/env python3
"""
Unit Tests for AI Power Intensity Analyzer
Comprehensive test suite for objective-based AI computational intensity analysis
"""

import unittest
from unittest.mock import patch, MagicMock
from ai_power_intensity_analyzer import AIPowerIntensityAnalyzer
import psutil


class TestAIPowerIntensityAnalyzer(unittest.TestCase):
    """Test suite for AIPowerIntensityAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = AIPowerIntensityAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertIsInstance(self.analyzer.objectives, list)
        self.assertEqual(len(self.analyzer.objectives), 10)
        self.assertIn("cpu_efficiency", self.analyzer.objectives)
        self.assertIn("memory_utilization", self.analyzer.objectives)
    
    def test_measure_cpu_efficiency_optimal_range(self):
        """Test CPU efficiency measurement in optimal range (20-70%)"""
        with patch('psutil.cpu_percent', return_value=45):
            result = self.analyzer.measure_objective("cpu_efficiency")
            self.assertEqual(result, 1.0)
    
    def test_measure_cpu_efficiency_low_range(self):
        """Test CPU efficiency measurement in low range (<20%)"""
        with patch('psutil.cpu_percent', return_value=10):
            result = self.analyzer.measure_objective("cpu_efficiency")
            self.assertEqual(result, 0.5)  # 10/20 = 0.5
    
    def test_measure_cpu_efficiency_high_range(self):
        """Test CPU efficiency measurement in high range (>70%)"""
        with patch('psutil.cpu_percent', return_value=85):
            result = self.analyzer.measure_objective("cpu_efficiency")
            self.assertEqual(result, 0.5)  # 1.0 - (85-70)/30 = 0.5
    
    def test_measure_memory_utilization_optimal(self):
        """Test memory utilization in optimal range (30-80%)"""
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.percent = 50
            result = self.analyzer.measure_objective("memory_utilization")
            self.assertEqual(result, 1.0)
    
    def test_measure_memory_utilization_low(self):
        """Test memory utilization in low range (<30%)"""
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.percent = 15
            result = self.analyzer.measure_objective("memory_utilization")
            self.assertEqual(result, 0.5)  # 15/30 = 0.5
    
    def test_measure_memory_utilization_high(self):
        """Test memory utilization in high range (>80%)"""
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.percent = 90
            result = self.analyzer.measure_objective("memory_utilization")
            self.assertEqual(result, 0.5)  # 1.0 - (90-80)/20 = 0.5
    
    def test_measure_power_efficiency(self):
        """Test power consumption efficiency measurement"""
        with patch('psutil.cpu_percent', return_value=40):
            result = self.analyzer.measure_objective("power_consumption")
            expected = max(0.0, 1.0 - (15 + 0.4 * 50) / 65.0)
            self.assertAlmostEqual(result, expected, places=3)
    
    def test_measure_process_distribution_perfect(self):
        """Test process distribution with perfect balance"""
        with patch('psutil.cpu_percent', return_value=[25, 25, 25, 25]):
            with patch.object(self.analyzer, '_get_ai_processes', return_value=[{'pid': 1}]):
                result = self.analyzer.measure_objective("process_distribution")
                self.assertEqual(result, 1.0)  # No imbalance
    
    def test_measure_process_distribution_imbalanced(self):
        """Test process distribution with imbalance"""
        with patch('psutil.cpu_percent', return_value=[100, 0, 0, 0]):
            with patch.object(self.analyzer, '_get_ai_processes', return_value=[{'pid': 1}]):
                result = self.analyzer.measure_objective("process_distribution")
                self.assertEqual(result, 0.0)  # Maximum imbalance
    
    def test_measure_computational_load(self):
        """Test computational load measurement"""
        with patch('psutil.cpu_percent', return_value=60):
            with patch('psutil.virtual_memory') as mock_memory:
                mock_memory.return_value.percent = 40
                result = self.analyzer.measure_objective("computational_load")
                expected = (60 + 40) / 200.0  # Combined load / 2 / 100
                self.assertEqual(result, expected)
    
    def test_measure_resource_stability_perfect(self):
        """Test resource stability with perfect stability"""
        with patch('psutil.cpu_percent', return_value=50):
            with patch('psutil.virtual_memory') as mock_memory:
                mock_memory.return_value.percent = 50
                result = self.analyzer.measure_objective("resource_stability")
                self.assertEqual(result, 1.0)  # Zero variance
    
    def test_measure_resource_stability_unstable(self):
        """Test resource stability with instability"""
        cpu_values = [0, 100, 0, 100, 0]
        memory_values = [0, 100, 0, 100, 0]
        
        with patch('psutil.cpu_percent', side_effect=cpu_values):
            with patch('psutil.virtual_memory') as mock_memory:
                mock_memory.return_value.percent = 50
                mock_memory.return_value.available = 1000
                mock_memory.return_value.total = 2000
                
                result = self.analyzer.measure_objective("resource_stability")
                self.assertLess(result, 1.0)  # Should be less than perfect
    
    def test_measure_processing_throughput_high(self):
        """Test processing throughput with high values"""
        with patch('psutil.cpu_percent', return_value=80):
            with patch('psutil.virtual_memory') as mock_memory:
                mock_memory.return_value.available = 100 * (1024**3)  # 100GB
                result = self.analyzer.measure_objective("processing_throughput")
                self.assertGreater(result, 0.0)
    
    def test_measure_processing_throughput_low(self):
        """Test processing throughput with low values"""
        with patch('psutil.cpu_percent', return_value=10):
            with patch('psutil.virtual_memory') as mock_memory:
                mock_memory.return_value.available = 1 * (1024**3)  # 1GB
                result = self.analyzer.measure_objective("processing_throughput")
                self.assertGreaterEqual(result, 0.0)
    
    def test_measure_system_responsiveness_good(self):
        """Test system responsiveness with good latency"""
        with patch('time.time', side_effect=[0, 0.001]):  # 1ms latency
            with patch('psutil.cpu_percent'):
                result = self.analyzer.measure_objective("system_responsiveness")
                self.assertGreater(result, 0.0)
    
    def test_measure_system_responsiveness_poor(self):
        """Test system responsiveness with poor latency"""
        with patch('time.time', side_effect=[0, 0.02]):  # 20ms latency
            with patch('psutil.cpu_percent'):
                result = self.analyzer.measure_objective("system_responsiveness")
                self.assertEqual(result, 0.0)  # 1.0 - 0.02 * 100 = 0.0
    
    def test_measure_thermal_efficiency_high(self):
        """Test thermal efficiency with high CPU load"""
        with patch('psutil.cpu_percent', return_value=90):
            result = self.analyzer.measure_objective("thermal_efficiency")
            self.assertEqual(result, 0.9)  # 90/100 = 0.9
    
    def test_measure_thermal_efficiency_low(self):
        """Test thermal efficiency with low CPU load"""
        with patch('psutil.cpu_percent', return_value=10):
            result = self.analyzer.measure_objective("thermal_efficiency")
            self.assertEqual(result, 0.1)  # 10/100 = 0.1
    
    def test_measure_workload_distribution_balanced(self):
        """Test workload distribution with balanced processes"""
        processes = [
            {'cpu_percent': 25, 'memory_percent': 10},
            {'cpu_percent': 25, 'memory_percent': 10},
            {'cpu_percent': 25, 'memory_percent': 10}
        ]
        with patch.object(self.analyzer, '_get_ai_processes', return_value=processes):
            result = self.analyzer.measure_objective("workload_distribution")
            self.assertEqual(result, 1.0)  # Perfect balance
    
    def test_measure_workload_distribution_unbalanced(self):
        """Test workload distribution with unbalanced processes"""
        processes = [
            {'cpu_percent': 100, 'memory_percent': 10},
            {'cpu_percent': 0, 'memory_percent': 10},
            {'cpu_percent': 0, 'memory_percent': 10}
        ]
        with patch.object(self.analyzer, '_get_ai_processes', return_value=processes):
            result = self.analyzer.measure_objective("workload_distribution")
            self.assertLess(result, 1.0)  # Some imbalance
    
    def test_get_ai_processes(self):
        """Test AI process detection"""
        mock_process = MagicMock()
        mock_process.info = {
            'pid': 1234,
            'name': 'python.exe',
            'cpu_percent': 5.0,
            'memory_percent': 2.0
        }
        mock_process.cpu_percent.return_value = 5.0
        
        with patch('psutil.process_iter', return_value=[mock_process]):
            processes = self.analyzer._get_ai_processes()
            self.assertEqual(len(processes), 1)
            self.assertEqual(processes[0]['name'], 'python.exe')
            self.assertEqual(processes[0]['pid'], 1234)
    
    def test_get_ai_processes_no_access(self):
        """Test AI process detection with access denied"""
        mock_process = MagicMock()
        mock_process.info = {'name': 'python.exe'}
        mock_process.cpu_percent.side_effect = psutil.AccessDenied(0, "test")
        
        with patch('psutil.process_iter', return_value=[mock_process]):
            processes = self.analyzer._get_ai_processes()
            self.assertEqual(len(processes), 0)  # Should handle gracefully
    
    def test_calculate_intensity_score(self):
        """Test comprehensive intensity score calculation"""
        with patch.object(self.analyzer, 'measure_objective', return_value=0.5):
            result = self.analyzer.calculate_intensity_score()
            
            self.assertIn('overall_intensity', result)
            self.assertIn('objective_scores', result)
            self.assertIn('intensity_level', result)
            self.assertIn('timestamp', result)
            
            # Check that all objectives are measured
            self.assertEqual(len(result['objective_scores']), 10)
            
            # Check overall intensity calculation
            expected_average = 0.5  # All objectives return 0.5
            self.assertAlmostEqual(result['overall_intensity'], expected_average)
    
    def test_classify_intensity_high(self):
        """Test intensity classification for high intensity"""
        result = self.analyzer._classify_intensity(0.85)
        self.assertEqual(result, "HIGH_INTENSITY")
    
    def test_classify_intensity_moderate(self):
        """Test intensity classification for moderate intensity"""
        result = self.analyzer._classify_intensity(0.7)
        self.assertEqual(result, "MODERATE_INTENSITY")
    
    def test_classify_intensity_normal(self):
        """Test intensity classification for normal intensity"""
        result = self.analyzer._classify_intensity(0.5)
        self.assertEqual(result, "NORMAL_INTENSITY")
    
    def test_classify_intensity_low(self):
        """Test intensity classification for low intensity"""
        result = self.analyzer._classify_intensity(0.3)
        self.assertEqual(result, "LOW_INTENSITY")
    
    def test_classify_intensity_minimal(self):
        """Test intensity classification for minimal intensity"""
        result = self.analyzer._classify_intensity(0.1)
        self.assertEqual(result, "MINIMAL_INTENSITY")
    
    def test_invalid_objective(self):
        """Test handling of invalid objective names"""
        result = self.analyzer.measure_objective("invalid_objective")
        self.assertEqual(result, 0.0)
    
    def test_no_ai_processes(self):
        """Test behavior when no AI processes are found"""
        with patch.object(self.analyzer, '_get_ai_processes', return_value=[]):
            result = self.analyzer.measure_objective("process_distribution")
            self.assertEqual(result, 0.0)
            
            result = self.analyzer.measure_objective("workload_distribution")
            self.assertEqual(result, 0.0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete analyzer"""
    
    def test_full_analysis_cycle(self):
        """Test complete analysis cycle with real-world scenario"""
        analyzer = AIPowerIntensityAnalyzer()
        
        # Mock all objectives to return consistent values
        with patch.object(analyzer, 'measure_objective', return_value=0.5):
            result = analyzer.calculate_intensity_score()
            
            # Verify structure
            self.assertIn('overall_intensity', result)
            self.assertIn('objective_scores', result)
            self.assertIn('intensity_level', result)
            self.assertIn('timestamp', result)
            
            # Verify reasonable values
            self.assertGreaterEqual(result['overall_intensity'], 0.0)
            self.assertLessEqual(result['overall_intensity'], 1.0)
            
            # Verify all objectives have scores
            self.assertEqual(len(result['objective_scores']), 10)
            
            # Verify classification
            self.assertEqual(result['intensity_level'], 'NORMAL_INTENSITY')


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

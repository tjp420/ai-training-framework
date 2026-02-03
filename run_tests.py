#!/usr/bin/env python3
"""
Test Runner for AI Power Intensity Analyzer
Simple script to run all tests and show results
"""

import subprocess
import sys
import os

def run_tests():
    """Run the AI Power Intensity Analyzer tests"""
    print("🧪 Running AI Power Intensity Analyzer Tests")
    print("=" * 50)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Run the tests
        result = subprocess.run([
            sys.executable, 'test_ai_power_intensity_analyzer.py'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_analyzer_demo():
    """Run a quick demo of the analyzer"""
    print("\n🚀 Running AI Power Intensity Analyzer Demo")
    print("=" * 50)
    
    try:
        from ai_power_intensity_analyzer import AIPowerIntensityAnalyzer
        
        analyzer = AIPowerIntensityAnalyzer()
        result = analyzer.calculate_intensity_score()
        
        print(f"Overall Intensity: {result['overall_intensity']:.3f}")
        print(f"Intensity Level: {result['intensity_level']}")
        print(f"Timestamp: {result['timestamp']}")
        
        print("\nObjective Scores:")
        for obj, score in result['objective_scores'].items():
            status = "✅" if score >= 0.7 else "⚠️" if score >= 0.4 else "❌"
            print(f"  {status} {obj}: {score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    tests_passed = run_tests()
    
    # Run demo if tests passed
    if tests_passed:
        run_analyzer_demo()
    
    print("\n🎯 Test runner completed!")

#!/usr/bin/env python3
"""
Workspace AI Power Intensity Analysis
Comprehensive analysis of current workspace AI computational intensity
"""

import time
import json
from ai_power_intensity_analyzer import AIPowerIntensityAnalyzer
from datetime import datetime

def analyze_workspace_intensity():
    """Analyze AI power intensity across workspace data"""
    print("🔍 Workspace AI Power Intensity Analysis")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    analyzer = AIPowerIntensityAnalyzer()
    
    # Collect multiple samples for analysis
    samples = []
    print("📊 Collecting intensity samples...")
    
    for i in range(5):
        result = analyzer.calculate_intensity_score()
        samples.append(result)
        print(f"  Sample {i+1}: {result['overall_intensity']:.3f} - {result['intensity_level']}")
        if i < 4:
            time.sleep(3)
    
    print()
    
    # Calculate aggregate metrics
    avg_intensity = sum(s['overall_intensity'] for s in samples) / len(samples)
    max_intensity = max(s['overall_intensity'] for s in samples)
    min_intensity = min(s['overall_intensity'] for s in samples)
    
    print("📈 Aggregate Analysis:")
    print(f"  Average Intensity: {avg_intensity:.3f}")
    print(f"  Max Intensity: {max_intensity:.3f}")
    print(f"  Min Intensity: {min_intensity:.3f}")
    print(f"  Intensity Range: {max_intensity - min_intensity:.3f}")
    print()
    
    # Analyze objective performance
    print("🎯 Objective Performance Analysis:")
    latest_sample = samples[-1]
    
    high_performers = []
    moderate_performers = []
    low_performers = []
    
    for obj, score in latest_sample['objective_scores'].items():
        if score >= 0.7:
            high_performers.append((obj, score))
        elif score >= 0.4:
            moderate_performers.append((obj, score))
        else:
            low_performers.append((obj, score))
    
    print("  ✅ High Performing Objectives (≥0.7):")
    for obj, score in sorted(high_performers, key=lambda x: x[1], reverse=True):
        print(f"    {obj}: {score:.3f}")
    
    print("  ⚠️ Moderate Performing Objectives (0.4-0.7):")
    for obj, score in sorted(moderate_performers, key=lambda x: x[1], reverse=True):
        print(f"    {obj}: {score:.3f}")
    
    print("  ❌ Low Performing Objectives (<0.4):")
    for obj, score in sorted(low_performers, key=lambda x: x[1], reverse=True):
        print(f"    {obj}: {score:.3f}")
    
    print()
    
    # Workspace characteristics
    print("🏢 Workspace Characteristics:")
    print(f"  Total Samples: {len(samples)}")
    print(f"  Analysis Duration: 15 seconds")
    print(f"  Stability: {'STABLE' if max_intensity - min_intensity < 0.1 else 'VARIABLE'}")
    print(f"  Performance Level: {latest_sample['intensity_level']}")
    
    # Generate recommendations
    print()
    print("💡 Recommendations:")
    
    if avg_intensity < 0.4:
        print("  🔄 Consider increasing AI workload for better resource utilization")
    elif avg_intensity > 0.8:
        print("  ⚡ System operating at high intensity - monitor for thermal constraints")
    else:
        print("  ✅ AI system operating within optimal intensity range")
    
    # Check specific objectives
    if low_performers:
        print(f"  🎯 Focus on optimizing: {', '.join([obj for obj, _ in low_performers[:3]])}")
    
    if high_performers:
        print(f"  🏆 Maintain excellence in: {', '.join([obj for obj, _ in high_performers])}")
    
    return {
        'timestamp': datetime.now().isoformat(),
        'samples': samples,
        'aggregate_metrics': {
            'average': avg_intensity,
            'maximum': max_intensity,
            'minimum': min_intensity,
            'range': max_intensity - min_intensity
        },
        'classification': latest_sample['intensity_level'],
        'recommendations': generate_recommendations(latest_sample)
    }

def generate_recommendations(sample):
    """Generate specific recommendations based on sample data"""
    recommendations = []
    
    obj_scores = sample['objective_scores']
    
    if obj_scores['cpu_efficiency'] < 0.5:
        recommendations.append("Optimize CPU workload distribution")
    
    if obj_scores['process_distribution'] < 0.3:
        recommendations.append("Improve AI process load balancing")
    
    if obj_scores['processing_throughput'] < 0.2:
        recommendations.append("Enhance processing pipeline efficiency")
    
    if obj_scores['workload_distribution'] < 0.3:
        recommendations.append("Implement better workload scheduling")
    
    if obj_scores['memory_utilization'] > 0.9:
        recommendations.append("Monitor memory usage for potential leaks")
    
    return recommendations

def main():
    """Main analysis function"""
    try:
        results = analyze_workspace_intensity()
        
        # Save results to file
        output_file = f"workspace_intensity_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        print("\n🎯 Workspace AI Power Intensity Analysis Complete!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    main()

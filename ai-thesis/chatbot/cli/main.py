#!/usr/bin/env python3
"""
Command-Line Interface for Thesis Symptom Chatbot

Enhancement: Professional CLI with multiple modes for thesis demonstration
"""

import argparse
import json
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.cli.chatbot import ThesisSymptomChatbot


def main():
    parser = argparse.ArgumentParser(
        description="Thesis: AI-Powered Symptom Assessment Chatbot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --describe "I have fever and headache"
  %(prog)s --symptoms fever cough headache
  %(prog)s --demo
  %(prog)s --research-stats
        
Thesis Focus: CLI interface for limited-resource healthcare access
        """
    )
    
    # Multiple input modes for flexibility
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-d", "--describe",
        type=str,
        help="Describe symptoms in natural language"
    )
    
    input_group.add_argument(
        "-s", "--symptoms",
        nargs="+",
        help="List specific symptoms (e.g., fever cough)"
    )
    
    input_group.add_argument(
        "--demo",
        action="store_true",
        help="Run thesis demonstration"
    )
    
    input_group.add_argument(
        "--research-stats",
        action="store_true",
        help="Show research data statistics"
    )
    
    # Additional options
    parser.add_argument(
        "-o", "--output",
        choices=["simple", "detailed", "json"],
        default="simple",
        help="Output format"
    )
    
    parser.add_argument(
        "--save-log",
        action="store_true",
        help="Save assessment to research log"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Thesis Symptom Chatbot v1.0 (A-Grade Enhancement)"
    )
    
    args = parser.parse_args()
    
    # Initialize chatbot
    chatbot = ThesisSymptomChatbot()
    
    print("\n" + "="*60)
    print("🎓 THESIS: AI Symptom Assessment Chatbot")
    print("="*60)
    
    if args.demo:
        # Run the built-in demonstration
        print("\n🧪 RUNNING THESIS DEMONSTRATION MODE")
        # Import and run the demonstration function
        import chatbot.cli.chatbot as chatbot_module
        chatbot_module.demonstrate_thesis_capabilities()
        
    elif args.research_stats:
        # Show research metrics
        print("\n📊 RESEARCH DATA STATISTICS")
        print("This feature would show analysis of collected data")
        print("Example: 50 assessments, common symptoms, etc.")
        
    elif args.describe:
        # Natural language input
        print(f"\n🔍 ANALYZING: '{args.describe}'")
        
        # NLP processing
        symptoms = chatbot.analyze_with_nlp(args.describe)
        
        if not symptoms:
            print("❌ No symptoms detected. Try being more specific.")
            sys.exit(1)
        
        print(f"   NLP Detected: {', '.join(symptoms)}")
        
        # Assessment
        assessment = chatbot.assess_symptoms(symptoms)
        
        # Output based on format
        if args.output == "json":
            print(json.dumps(assessment, indent=2))
        elif args.output == "detailed":
            _print_detailed_assessment(assessment)
        else:
            _print_simple_assessment(assessment)
        
        # Save to research log if requested
        if args.save_log:
            chatbot.log_conversation(args.describe, assessment)
            print(f"\n📁 Saved to research log: data/thesis_research_log.json")
    
    elif args.symptoms:
        # Direct symptom list input
        print(f"\n🔍 ASSESSING SYMPTOMS: {', '.join(args.symptoms)}")
        
        assessment = chatbot.assess_symptoms(args.symptoms)
        
        if args.output == "json":
            print(json.dumps(assessment, indent=2))
        elif args.output == "detailed":
            _print_detailed_assessment(assessment)
        else:
            _print_simple_assessment(assessment)
        
        if args.save_log:
            chatbot.log_conversation(" ".join(args.symptoms), assessment)
            print(f"\n📁 Saved to research log")
    
    print("\n" + "="*60)
    print("🧠 Thesis Contribution: CLI for healthcare access in resource-limited areas")
    print("="*60)


def _print_simple_assessment(assessment: dict):
    """Simple output format"""
    print(f"\n🩺 POSSIBLE CONDITIONS:")
    for condition in assessment.get("possible_conditions", []):
        print(f"   • {condition}")
    
    print(f"\n❓ KEY QUESTIONS:")
    for i, question in enumerate(assessment.get("follow_up_questions", [])[:3], 1):
        print(f"   {i}. {question}")
    
    print(f"\n💡 HEALTHCARE ADVICE:")
    print(f"   {assessment.get('healthcare_advice', 'Monitor symptoms')}")
    
    print(f"\n⚠️  {assessment.get('ethical_notice', {}).get('disclaimer', '')}")


def _print_detailed_assessment(assessment: dict):
    """Detailed output format for thesis demonstration"""
    print("\n" + "-"*40)
    print("DETAILED ASSESSMENT (Thesis Methodology)")
    print("-"*40)
    
    print(f"\n📅 Assessment Time: {assessment.get('assessment_time', 'N/A')}")
    print(f"📝 Input Symptoms: {', '.join(assessment.get('input_symptoms', []))}")
    
    print(f"\n🔬 POSSIBLE MEDICAL CONDITIONS:")
    for i, condition in enumerate(assessment.get("possible_conditions", []), 1):
        print(f"   {i:2d}. {condition}")
    
    print(f"\n🔍 FOLLOW-UP CLINICAL QUESTIONS:")
    for i, question in enumerate(assessment.get("follow_up_questions", []), 1):
        print(f"   {i:2d}. {question}")
    
    print(f"\n🏥 HEALTHCARE SYSTEM INTEGRATION:")
    print(f"   Recommendation: {assessment.get('healthcare_advice', 'N/A')}")
    
    print(f"\n⚖️  ETHICAL FRAMEWORK:")
    ethics = assessment.get('ethical_notice', {})
    print(f"   Primary Disclaimer: {ethics.get('disclaimer', 'N/A')}")
    print(f"   Key Limitations: {ethics.get('limitations', ['N/A'])[0]}")
    
    print(f"\n📚 THESIS CONTEXT:")
    print("   This tool demonstrates AI-assisted preliminary assessment")
    print("   for areas with limited healthcare professional access.")


if __name__ == "__main__":
    main()

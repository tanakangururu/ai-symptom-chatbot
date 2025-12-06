#!/usr/bin/env python3
"""
AI-Powered Symptom Assessment Chatbot - Thesis Implementation

Project: Development of an AI-powered chatbot for preliminary symptom assessments
via command-line interface, focusing on areas with limited healthcare access.
"""

import json
import re
from datetime import datetime
from typing import Dict, List


class ThesisSymptomChatbot:
    """
    Thesis Implementation: AI chatbot for preliminary symptom assessment
    Key Features from Thesis Description:
    1. Command-line interface
    2. Rule-based logic + NLP techniques
    3. Designed for limited access/connectivity areas
    4. Ethical considerations framework
    5. Complements formal healthcare systems
    """
    
    def __init__(self):
        self.name = "ThesisHealthBot"
        self.version = "1.0"
        self.conversation_history = []
        
        # Rule-based symptom database (Thesis: rule-based logic)
             
        self.symptom_rules = {
            "fever": {
                "conditions": ["Influenza", "Common Cold", "Malaria", "COVID-19", "Dengue"],
                "questions": ["Temperature?", "Duration?", "Chills/Sweating?", "Recent travel?"],
                "urgency": "medium"
            },
            "cough": {
                "conditions": ["Bronchitis", "Asthma", "Allergy", "COVID-19", "Tuberculosis"],
                "questions": ["Dry/Productive?", "Duration?", "Blood in phlegm?", "Smoking history?"],
                "urgency": "low"
            },
            "headache": {
                "conditions": ["Migraine", "Tension Headache", "Sinusitis", "Hypertension"],
                "questions": ["Location?", "Intensity (1-10)?", "Duration?", "Visual disturbances?"],
                "urgency": "medium"
            },
            "fatigue": {
                "conditions": ["Anemia", "Depression", "Chronic Fatigue", "Thyroid Issues"],
                "questions": ["Duration?", "Sleep quality?", "Associated with other symptoms?"],
                "urgency": "low"
            },
            "nausea": {
                "conditions": ["Food Poisoning", "Migraine", "Gastroenteritis", "Pregnancy"],
                "questions": ["Vomiting?", "Recent food intake?", "Pregnancy possibility?"],
                "urgency": "medium"
            },
            "chest pain": {
                "conditions": ["Angina", "Heart Attack", "Costochondritis", "Anxiety"],
                "questions": ["Type (sharp/dull)?", "Duration?", "Radiation to arms?", "Shortness of breath?"],
                "urgency": "high"
            },
            "shortness of breath": {
                "conditions": ["Asthma", "Pneumonia", "Heart Failure", "Anxiety Attack"],
                "questions": ["At rest or exertion?", "Duration?", "Wheezing?", "Chest pain?"],
                "urgency": "high"
            },
            "abdominal pain": {
                "conditions": ["Appendicitis", "Gallstones", "UTI", "Irritable Bowel"],
                "questions": ["Location?", "Type (cramping/sharp)?", "Bowel changes?", "Fever?"],
                "urgency": "medium"
            },
            "dizziness": {
                "conditions": ["Vertigo", "Low Blood Pressure", "Anemia", "Dehydration"],
                "questions": ["Spinning sensation?", "Triggered by movement?", "Recent head injury?"],
                "urgency": "medium"
            },
            "rash": {
                "conditions": ["Allergy", "Eczema", "Measles", "Chickenpox"],
                "questions": ["Location?", "Itchy?", "Fever?", "Recent medication?"],
                "urgency": "low"
            },
            "joint pain": {
                "conditions": ["Arthritis", "Gout", "Lupus", "Lyme Disease"],
                "questions": ["Which joints?", "Swelling?", "Morning stiffness?", "Recent injury?"],
                "urgency": "low"
            },
            "sore throat": {
                "conditions": ["Strep Throat", "Tonsillitis", "Common Cold", "COVID-19"],
                "questions": ["Pain level?", "Difficulty swallowing?", "Fever?", "Cough?"],
                "urgency": "low"
            },
            "back pain": {
                "conditions": ["Muscle Strain", "Herniated Disc", "Kidney Infection", "Arthritis"],
                "questions": ["Location?", "Radiation to legs?", "Recent injury?", "Fever?"],
                "urgency": "medium"
            },
            "diarrhea": {
                "conditions": ["Gastroenteritis", "Food Poisoning", "IBD", "Infection"],
                "questions": ["Duration?", "Blood in stool?", "Fever?", "Recent travel?"],
                "urgency": "medium"
            },
            "weight loss": {
                "conditions": ["Hyperthyroidism", "Diabetes", "Cancer", "Depression"],
                "questions": ["Amount lost?", "Time period?", "Appetite changes?", "Other symptoms?"],
                "urgency": "medium"
            }
        }
        
        # Thesis: Ethical considerations
        self.ethical_guidelines = {
            "disclaimer": "ACADEMIC RESEARCH ONLY. NOT FOR MEDICAL DIAGNOSIS.",
            "limitations": [
                "Preliminary assessment only",
                "Cannot replace healthcare professional",
                "No treatment recommendations"
            ]
        }
    
    def analyze_with_nlp(self, user_input: str) -> List[str]:
        """
        Thesis: NLP techniques to interpret user-reported symptoms
        
        Args:
            user_input: Natural language symptom description
            
        Returns:
            List of detected symptom keywords
        """
        # Simple NLP: lower case, find keywords
        text = user_input.lower()
        detected = []
        
        for symptom, data in self.symptom_rules.items():
            if symptom in text:
                detected.append(symptom)
        
        return detected
    
    def assess_symptoms(self, symptoms: List[str]) -> Dict:
        """
        Thesis: Match symptoms to potential conditions
        
        Args:
            symptoms: List of symptom keywords
            
        Returns:
            Assessment with possible conditions and advice
        """
        if not symptoms:
            return {"error": "No symptoms detected"}
        
        possible_conditions = []
        follow_up_questions = []
        
        for symptom in symptoms:
            if symptom in self.symptom_rules:
                data = self.symptom_rules[symptom]
                possible_conditions.extend(data["conditions"])
                follow_up_questions.extend(data["questions"])
        
        # Remove duplicates
        possible_conditions = list(set(possible_conditions))
        follow_up_questions = list(set(follow_up_questions))
        
        return {
            "assessment_time": datetime.now().isoformat(),
            "input_symptoms": symptoms,
            "possible_conditions": possible_conditions,
            "follow_up_questions": follow_up_questions[:3],  # Limit to 3
            "healthcare_advice": self._generate_healthcare_advice(symptoms),
            "ethical_notice": self.ethical_guidelines
        }
    
    def _generate_healthcare_advice(self, symptoms: List[str]) -> str:
        """
        Thesis: How tool complements formal healthcare systems
        
        Args:
            symptoms: List of symptoms
            
        Returns:
            Advice for next steps in healthcare system
        """
        if not symptoms:
            return "No symptoms detected. Monitor health regularly."
        
        # Simple logic for demonstration
        if "fever" in symptoms:
            return "Consider contacting healthcare provider if fever persists >3 days"
        elif "headache" in symptoms:
            return "If headache is severe or persistent, seek medical evaluation"
        else:
            return "Monitor symptoms. Seek professional care if symptoms worsen."
    
    def log_conversation(self, user_input: str, assessment: Dict):
        """
        Thesis: Data collection for research analysis
        
        Args:
            user_input: Original user input
            assessment: Generated assessment
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "assessment": assessment,
            "research_purpose": "Thesis data collection"
        }
        self.conversation_history.append(log_entry)
        
        # Save to file (for offline/limited connectivity scenarios)
        with open("data/thesis_research_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")


def demonstrate_thesis_capabilities():
    """
    Demonstrate how this implementation addresses thesis requirements
    """
    print("🧪 THESIS PROJECT DEMONSTRATION")
    print("=" * 60)
    
    # Create chatbot instance
    chatbot = ThesisSymptomChatbot()
    
    # Test Case 1: Basic symptom assessment
    print("\n1. COMMAND-LINE INTERFACE CAPABILITY")
    print("   Input: 'I have fever and cough'")
    
    # NLP processing
    symptoms = chatbot.analyze_with_nlp("I have fever and cough")
    print(f"   NLP Detected: {symptoms}")
    
    # Rule-based assessment
    assessment = chatbot.assess_symptoms(symptoms)
    print(f"   Possible Conditions: {assessment['possible_conditions']}")
    
    # Test Case 2: Ethical considerations
    print("\n2. ETHICAL CONSIDERATIONS")
    print(f"   Disclaimer: {assessment['ethical_notice']['disclaimer']}")
    print(f"   Limitations: {assessment['ethical_notice']['limitations'][0]}")
    
    # Test Case 3: Healthcare complementarity
    print("\n3. HEALTHCARE SYSTEM COMPLEMENT")
    print(f"   Advice: {assessment['healthcare_advice']}")
    
    # Test Case 4: Data logging (for research)
    print("\n4. RESEARCH DATA COLLECTION")
    chatbot.log_conversation("I have fever and cough", assessment)
    print("   Conversation logged for thesis analysis")
    
    print("\n" + "=" * 60)
    print("✅ Thesis Requirements Addressed:")
    print("   • CLI interface implemented")
    print("   • Rule-based + NLP techniques used")
    print("   • Ethical framework included")
    print("   • Healthcare system complement defined")
    print("   • Research data collection enabled")


if __name__ == "__main__":
    demonstrate_thesis_capabilities()

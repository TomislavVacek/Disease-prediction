import pandas as pd
import json
import os

class HealthKnowledgeBase:
    """
    Class for storing and retrieving health recommendations, prevention tips,
    and treatment advice for various diseases.
    """
    
    def __init__(self):
        # Define the path for storing recommendations data
        self.data_path = os.path.join('dataset', 'health_recommendations.json')
        
        # Load existing recommendations or create new ones
        self.recommendations = self._load_recommendations()
        
    def _load_recommendations(self):
        """Load health recommendations from JSON file or create default ones"""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # If file doesn't exist, create default recommendations
                default_recommendations = self._create_default_recommendations()
                
                # Save the default recommendations
                self._save_recommendations(default_recommendations)
                
                return default_recommendations
        except Exception as e:
            print(f"Error loading health recommendations: {str(e)}")
            return self._create_default_recommendations()
    
    def _save_recommendations(self, recommendations):
        """Save health recommendations to JSON file"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            
            with open(self.data_path, 'w', encoding='utf-8') as file:
                json.dump(recommendations, file, indent=4)
        except Exception as e:
            print(f"Error saving health recommendations: {str(e)}")
    
    def _create_default_recommendations(self):
        """Create default health recommendations for common diseases"""
        return {
            "Common Cold": {
                "overview": "The common cold is a viral infection of the upper respiratory tract. Most adults catch a cold from time to time, but children may get them more frequently.",
                "lifestyle": {
                    "rest": [
                        "Get plenty of rest to help your body fight the infection",
                        "Stay home to avoid spreading the virus to others",
                        "Sleep with your head elevated to help relieve congestion"
                    ],
                    "hydration": [
                        "Drink plenty of fluids like water, juice, or clear broth",
                        "Avoid alcohol and caffeine which can contribute to dehydration"
                    ],
                    "home_remedies": [
                        "Use a humidifier to add moisture to the air and help ease congestion",
                        "Gargle with salt water to soothe a sore throat (1/4 to 1/2 teaspoon salt dissolved in 8 ounces of warm water)",
                        "Take hot showers to relieve nasal congestion"
                    ]
                },
                "diet": {
                    "include": [
                        "Warm broths and soups (especially chicken soup) to ease congestion and provide hydration",
                        "Honey to soothe cough (not for children under 1 year)",
                        "Vitamin C-rich foods like citrus fruits, berries, and leafy greens",
                        "Ginger tea with honey to help relieve congestion and soothe sore throat",
                        "Garlic, which has antimicrobial properties"
                    ],
                    "avoid": [
                        "Dairy products, which may increase mucus production",
                        "Alcoholic beverages, which can worsen inflammation and dehydrate you",
                        "Caffeine, which can contribute to dehydration",
                        "Sugary foods and drinks that may weaken immune response"
                    ]
                },
                "medical": {
                    "otc_medications": [
                        "Decongestants like pseudoephedrine (Sudafed) to reduce nasal congestion",
                        "Pain relievers such as acetaminophen (Tylenol) or ibuprofen (Advil, Motrin) to reduce fever and relieve pain",
                        "Cough suppressants containing dextromethorphan for persistent dry cough",
                        "Nasal saline sprays to ease congestion"
                    ],
                    "when_to_see_doctor": [
                        "Fever above 101.3°F (38.5°C) lasting more than three days",
                        "Symptoms that worsen after 7-10 days or don't improve with home treatment",
                        "Severe symptoms like difficult breathing or inability to keep fluids down",
                        "If you have chronic conditions like asthma, heart disease, or a weakened immune system"
                    ]
                },
                "prevention": [
                    "Wash hands frequently with soap and water for at least 20 seconds",
                    "Avoid close contact with people who are sick",
                    "Don't touch your face, especially your eyes, nose, and mouth",
                    "Clean and disinfect frequently touched surfaces",
                    "Boost your immune system through regular exercise, adequate sleep, and a balanced diet"
                ]
            },
            "Diabetes": {
                "overview": "Diabetes is a chronic condition that affects how your body turns food into energy. It occurs when your blood glucose (blood sugar) is too high. The main types are Type 1, Type 2, and gestational diabetes.",
                "lifestyle": {
                    "physical_activity": [
                        "Aim for at least 150 minutes of moderate-intensity exercise per week",
                        "Include both aerobic activities (walking, swimming, cycling) and strength training",
                        "Break up long periods of sitting with brief activity every 30 minutes",
                        "Check blood sugar before, during, and after exercise, especially when starting a new routine"
                    ],
                    "monitoring": [
                        "Check blood sugar levels regularly as advised by your healthcare provider",
                        "Keep track of your results to see patterns",
                        "Monitor blood pressure and cholesterol regularly",
                        "Check your feet daily for cuts, blisters, or swelling"
                    ],
                    "stress_management": [
                        "Practice stress-reduction techniques like meditation, deep breathing, or yoga",
                        "Get adequate sleep (7-9 hours per night)",
                        "Seek support from friends, family, or support groups for emotional well-being"
                    ]
                },
                "diet": {
                    "include": [
                        "High-fiber foods such as whole grains, fruits, vegetables, and legumes",
                        "Lean proteins like chicken, fish, tofu, and legumes",
                        "Healthy fats from sources like nuts, seeds, avocados, and olive oil",
                        "Foods with low glycemic index that won't cause spikes in blood sugar"
                    ],
                    "avoid": [
                        "Sugary foods and beverages like sodas, candy, and desserts",
                        "Refined carbohydrates like white bread, white rice, and processed snacks",
                        "Saturated and trans fats found in fried foods and many processed foods",
                        "Excessive alcohol consumption"
                    ],
                    "meal_planning": [
                        "Follow a consistent meal schedule to help maintain steady blood sugar levels",
                        "Monitor carbohydrate intake and practice portion control",
                        "Consider working with a registered dietitian to create a personalized meal plan",
                        "Stay well-hydrated with water rather than sugary drinks"
                    ]
                },
                "medical": {
                    "medications": [
                        "Insulin therapy (required for Type 1 diabetes, sometimes needed for Type 2)",
                        "Metformin, which reduces glucose production in the liver",
                        "Sulfonylureas, which help your pancreas secrete more insulin",
                        "DPP-4 inhibitors, which help reduce blood sugar levels",
                        "GLP-1 receptor agonists, which slow digestion and help lower blood sugar levels",
                        "SGLT2 inhibitors, which help the kidneys remove glucose from the bloodstream"
                    ],
                    "monitoring_supplies": [
                        "Blood glucose meter and test strips",
                        "Continuous glucose monitoring (CGM) systems",
                        "Insulin pumps for some patients",
                        "Ketone testing supplies, especially for Type 1 diabetes"
                    ],
                    "when_to_seek_help": [
                        "Blood sugar levels consistently outside your target range",
                        "Symptoms of hypoglycemia (low blood sugar) like shakiness, sweating, confusion",
                        "Symptoms of hyperglycemia (high blood sugar) like excessive thirst, frequent urination",
                        "Signs of diabetic ketoacidosis like fruity breath, nausea, confusion, or deep, rapid breathing",
                        "Any new or worsening complications related to diabetes"
                    ]
                },
                "prevention": [
                    "Maintain a healthy weight through balanced diet and regular physical activity",
                    "Get regular health screenings, especially if you have risk factors for diabetes",
                    "Don't smoke or use tobacco products",
                    "Limit alcohol consumption",
                    "Manage stress through healthy coping mechanisms",
                    "For those with prediabetes, lifestyle changes can prevent or delay the onset of Type 2 diabetes"
                ],
                "complications": [
                    "Heart disease and stroke",
                    "Kidney disease or kidney failure",
                    "Eye problems (retinopathy) that can lead to vision loss",
                    "Nerve damage (neuropathy), especially in the feet and legs",
                    "Foot problems that can lead to serious infections and in extreme cases, amputation",
                    "Skin and mouth conditions",
                    "Pregnancy complications"
                ]
            },
            "Hypertension": {
                "overview": "Hypertension, or high blood pressure, is a common condition where the long-term force of blood against artery walls is high enough to eventually cause health problems like heart disease.",
                "lifestyle": {
                    "physical_activity": [
                        "Engage in regular aerobic activities like walking, swimming, or cycling",
                        "Aim for at least 150 minutes of moderate-intensity exercise per week",
                        "Include strength training exercises 2-3 times per week",
                        "Break up periods of sitting with short activity breaks throughout the day"
                    ],
                    "stress_management": [
                        "Practice relaxation techniques such as deep breathing, meditation, or yoga",
                        "Ensure adequate sleep (7-9 hours per night)",
                        "Consider mindfulness practices to manage stress responses",
                        "Maintain social connections and seek support when needed"
                    ],
                    "other_modifications": [
                        "Quit smoking and avoid secondhand smoke",
                        "Limit alcohol consumption (no more than 1 drink per day for women, 2 for men)",
                        "Monitor your blood pressure regularly at home",
                        "Maintain a healthy weight or lose weight if overweight"
                    ]
                },
                "diet": {
                    "include": [
                        "Fruits and vegetables (aim for 8-10 servings daily)",
                        "Whole grains like brown rice, whole wheat bread, and oats",
                        "Low-fat dairy products for calcium without excessive fat",
                        "Lean proteins such as fish, poultry, beans, and nuts",
                        "Foods rich in potassium like bananas, potatoes, avocados, and spinach",
                        "Foods containing magnesium and fiber"
                    ],
                    "avoid": [
                        "High-sodium foods (processed foods, canned soups, frozen dinners)",
                        "Saturated and trans fats found in red meat and full-fat dairy",
                        "Sugar-sweetened beverages and sweets",
                        "Excessive caffeine, which can raise blood pressure temporarily",
                        "Alcohol in excess"
                    ],
                    "dietary_approaches": [
                        "Consider following the DASH (Dietary Approaches to Stop Hypertension) diet",
                        "Limit sodium intake to less than 2,300 mg per day (ideal target: 1,500 mg)",
                        "Read food labels to identify hidden sodium and unhealthy fats",
                        "Cook at home more often to control ingredients",
                        "Stay well-hydrated with water throughout the day"
                    ]
                },
                "medical": {
                    "medications": [
                        "Diuretics (water pills) to help kidneys remove sodium and water from the body",
                        "ACE inhibitors, which relax blood vessels by blocking certain hormones",
                        "Angiotensin II receptor blockers (ARBs), which help blood vessels relax and open",
                        "Calcium channel blockers, which prevent calcium from entering heart and blood vessel cells",
                        "Beta-blockers, which reduce the workload on the heart and make it beat slower with less force"
                    ],
                    "monitoring": [
                        "Home blood pressure monitor for regular self-checks",
                        "Blood pressure log to track readings over time",
                        "Regular check-ups with healthcare provider",
                        "Periodic laboratory tests to monitor kidney function and electrolyte levels"
                    ],
                    "when_to_seek_help": [
                        "Blood pressure readings consistently above 140/90 mmHg",
                        "Symptoms like severe headache, chest pain, difficulty breathing, vision problems",
                        "Blood pressure not responding to prescribed medications",
                        "Side effects from blood pressure medications"
                    ]
                },
                "prevention": [
                    "Maintain a healthy weight",
                    "Exercise regularly",
                    "Eat a healthy diet low in sodium and rich in fruits and vegetables",
                    "Limit alcohol consumption",
                    "Don't smoke and avoid secondhand smoke",
                    "Manage stress through healthy coping strategies",
                    "Get regular health screenings, especially if you have risk factors for hypertension"
                ],
                "complications": [
                    "Heart attack and stroke",
                    "Heart failure",
                    "Aneurysms (bulges in weakened blood vessels)",
                    "Kidney damage or failure",
                    "Eye damage and vision loss",
                    "Metabolic syndrome",
                    "Cognitive changes, including dementia"
                ]
            },
            "Migraine": {
                "overview": "Migraine is a neurological condition that causes recurring attacks of moderate to severe headache, often with other symptoms such as nausea, sensitivity to light and sound, and visual disturbances.",
                "lifestyle": {
                    "trigger_management": [
                        "Identify and avoid personal migraine triggers like certain foods, stress, or environmental factors",
                        "Maintain a consistent sleep schedule, even on weekends",
                        "Eat regular meals to prevent hunger-triggered migraines",
                        "Limit exposure to bright lights, loud sounds, and strong smells during attacks"
                    ],
                    "stress_reduction": [
                        "Practice stress management techniques like meditation, yoga, or progressive muscle relaxation",
                        "Consider cognitive behavioral therapy to develop coping strategies",
                        "Take breaks during work or stressful activities",
                        "Engage in enjoyable activities and hobbies regularly"
                    ],
                    "physical_activity": [
                        "Engage in regular moderate exercise like walking, swimming, or cycling",
                        "Start exercise routines gradually to avoid triggering migraines",
                        "Consider gentle practices like yoga or tai chi",
                        "Be cautious with high-intensity workouts, which can trigger migraines in some people"
                    ]
                },
                "diet": {
                    "include": [
                        "Fresh fruits and vegetables",
                        "Lean proteins",
                        "Whole grains",
                        "Adequate water (at least 8 glasses daily) to prevent dehydration-induced migraines",
                        "Foods containing magnesium, like nuts, seeds, and leafy greens",
                        "Omega-3 fatty acids found in fatty fish and flaxseeds"
                    ],
                    "avoid": [
                        "Common trigger foods like aged cheeses, processed meats, and chocolate",
                        "Foods containing MSG, artificial sweeteners, and preservatives",
                        "Alcoholic beverages, especially red wine and beer",
                        "Caffeine (excessive consumption or withdrawal can trigger migraines)",
                        "Tyramine-rich foods (aged cheeses, cured meats, fermented foods)"
                    ],
                    "dietary_approaches": [
                        "Keep a food diary to identify personal trigger foods",
                        "Eat regular meals to maintain stable blood sugar levels",
                        "Consider an elimination diet under healthcare provider guidance",
                        "Stay well-hydrated throughout the day",
                        "Be consistent with caffeine intake to avoid withdrawal headaches"
                    ]
                },
                "medical": {
                    "acute_medications": [
                        "Pain relievers like ibuprofen, aspirin, or acetaminophen for mild migraines",
                        "Triptans such as sumatriptan (Imitrex) to block pain pathways",
                        "Ergots, which constrict blood vessels and reduce inflammation",
                        "Anti-nausea medications to manage related symptoms",
                        "Gepants and ditans (newer classes of migraine medications)"
                    ],
                    "preventive_medications": [
                        "Beta-blockers like propranolol or metoprolol",
                        "Antidepressants such as amitriptyline",
                        "Anti-seizure drugs like topiramate or valproate",
                        "CGRP monoclonal antibodies (newer medications specifically developed for migraine prevention)",
                        "Botox injections for chronic migraine"
                    ],
                    "when_to_seek_help": [
                        "Migraine that is unusually severe or feels different from your typical headaches",
                        "Headache accompanied by fever, stiff neck, confusion, seizures, double vision, weakness",
                        "New headache pain after age 50",
                        "Headaches that worsen over days or that are worsened by coughing, exertion, or movement",
                        "Current medications not providing relief"
                    ]
                },
                "complementary_approaches": [
                    "Acupuncture, which may help reduce migraine frequency",
                    "Biofeedback to control physical responses to stress",
                    "Vitamin and mineral supplements like magnesium, riboflavin (B2), and coenzyme Q10",
                    "Herbal preparations like feverfew or butterbur (consult healthcare provider first)",
                    "Massage therapy to reduce muscle tension",
                    "Cold or hot compresses applied to the head or neck"
                ],
                "prevention": [
                    "Maintain a regular sleep schedule",
                    "Stay hydrated and don't skip meals",
                    "Exercise regularly",
                    "Manage stress effectively",
                    "Keep a headache diary to identify patterns and triggers",
                    "Consider preventive medications if migraines are frequent or debilitating",
                    "Regular follow-ups with healthcare provider"
                ]
            },
            "Bronchial Asthma": {
                "overview": "Bronchial asthma is a chronic inflammatory condition of the airways characterized by episodes of wheezing, shortness of breath, chest tightness, and coughing. During an asthma attack, the airways narrow, making it difficult to breathe.",
                "lifestyle": {
                    "trigger_avoidance": [
                        "Identify and avoid personal asthma triggers (allergens, irritants, exercise, etc.)",
                        "Reduce exposure to dust mites by using allergen-proof bed covers and washing bedding weekly",
                        "Keep indoor humidity between 30-50% to reduce mold growth",
                        "Consider removing carpets, especially in bedrooms",
                        "Use air purifiers with HEPA filters"
                    ],
                    "physical_activity": [
                        "Regular exercise can improve lung function and overall health",
                        "Use prescribed inhalers before exercise if needed",
                        "Choose activities that are less likely to trigger asthma (swimming, walking, biking)",
                        "Warm up adequately before exercise and cool down afterward",
                        "Exercise indoors on days with high pollution, cold air, or high pollen counts"
                    ],
                    "home_environment": [
                        "Keep your home clean and free of dust, mold, and pet dander",
                        "Don't allow smoking in your home",
                        "Use unscented cleaning products and avoid strong chemical odors",
                        "Change HVAC filters regularly",
                        "Consider removing items that collect dust like stuffed toys, curtains, and carpets"
                    ]
                },
                "diet": {
                    "include": [
                        "Fruits and vegetables rich in antioxidants",
                        "Foods with omega-3 fatty acids like fatty fish, flaxseeds, and walnuts",
                        "Vitamin D sources (fortified milk, fatty fish, egg yolks) as deficiency may worsen asthma",
                        "Foods rich in magnesium, such as leafy greens, nuts, and whole grains",
                        "Ginger and turmeric, which have anti-inflammatory properties"
                    ],
                    "avoid": [
                        "Sulfite-containing foods (wine, dried fruits, preserved foods) if sensitive",
                        "Known food allergens that may trigger asthma symptoms",
                        "Highly processed foods with artificial additives",
                        "Saltier foods, as high salt intake may worsen asthma symptoms in some people",
                        "Gas-producing foods that may cause bloating and pressure on the diaphragm"
                    ]
                },
                "medical": {
                    "controller_medications": [
                        "Inhaled corticosteroids to reduce inflammation (fluticasone, budesonide, beclomethasone)",
                        "Long-acting beta agonists (LABAs) like salmeterol or formoterol",
                        "Combination inhalers containing both a corticosteroid and a LABA",
                        "Leukotriene modifiers like montelukast (Singulair)",
                        "Biologics for severe asthma (omalizumab, mepolizumab, others)"
                    ],
                    "rescue_medications": [
                        "Short-acting beta agonists (albuterol) for quick relief during an asthma attack",
                        "Oral corticosteroids for severe asthma attacks",
                        "Anticholinergics like ipratropium for additional bronchodilation"
                    ],
                    "devices": [
                        "Metered dose inhalers (MDIs)",
                        "Dry powder inhalers (DPIs)",
                        "Nebulizers for delivering medication as a mist",
                        "Spacers or valved holding chambers to improve inhaler effectiveness",
                        "Peak flow meters to monitor lung function at home"
                    ],
                    "asthma_action_plan": [
                        "Work with your doctor to create a written plan for managing asthma",
                        "Know when to adjust medications based on symptoms",
                        "Understand emergency signs and when to seek immediate help",
                        "Have a plan for asthma attacks when away from home"
                    ],
                    "when_to_seek_help": [
                        "Symptoms not improving with rescue inhaler",
                        "Difficulty speaking due to shortness of breath",
                        "Straining chest muscles to breathe",
                        "Blue lips or fingernails",
                        "Decreasing peak flow readings"
                    ]
                },
                "prevention": [
                    "Take controller medications as prescribed, even when feeling well",
                    "Get vaccinated against flu and pneumonia",
                    "Know and avoid your triggers",
                    "Monitor your breathing and peak flow regularly",
                    "Have regular check-ups with your healthcare provider",
                    "Keep rescue medication accessible at all times",
                    "Create an asthma-friendly home environment"
                ]
            },
            "Gastroenteritis": {
                "overview": "Gastroenteritis is inflammation of the digestive tract, particularly the stomach and intestines, usually due to viral or bacterial infections. It typically results in diarrhea, vomiting, abdominal cramps, and sometimes fever.",
                "lifestyle": {
                    "rest_recovery": [
                        "Get plenty of rest to help your body fight the infection",
                        "Stay home from work or school until symptoms resolve, especially if vomiting or having diarrhea",
                        "Avoid strenuous activities until you're fully recovered"
                    ],
                    "hygiene": [
                        "Wash hands thoroughly with soap and water, especially after using the bathroom and before preparing food",
                        "Use separate towels, utensils, and dishes from others if possible",
                        "Clean and disinfect contaminated surfaces promptly, especially in bathrooms and kitchens",
                        "Avoid preparing food for others while sick and for 2 days after symptoms resolve"
                    ]
                },
                "diet": {
                    "hydration": [
                        "Drink plenty of fluids to prevent dehydration (water, clear broths, oral rehydration solutions)",
                        "Sip small amounts frequently rather than large amounts at once",
                        "For severe dehydration, use oral rehydration solutions like Pedialyte",
                        "Avoid caffeine and alcohol, which can worsen dehydration"
                    ],
                    "reintroducing_food": [
                        "Follow the BRAT diet during early recovery: Bananas, Rice, Applesauce, Toast",
                        "Gradually add bland, low-fat foods like plain crackers, boiled potatoes, and clear soups",
                        "Return to normal diet slowly as symptoms improve",
                        "Eat small, frequent meals rather than large ones"
                    ],
                    "avoid": [
                        "Dairy products (temporarily, until recovery)",
                        "Fatty, greasy, or fried foods",
                        "Spicy foods that may irritate the digestive tract",
                        "High-sugar foods and beverages",
                        "Alcohol and caffeine"
                    ]
                },
                "medical": {
                    "otc_treatments": [
                        "Oral rehydration solutions to replace lost fluids and electrolytes",
                        "Antidiarrheal medications like loperamide (Imodium) for adults (use only as directed)",
                        "Anti-nausea medications like bismuth subsalicylate (Pepto-Bismol)",
                        "Pain relievers like acetaminophen for fever or discomfort (avoid NSAIDs which may irritate the stomach)"
                    ],
                    "when_to_seek_help": [
                        "Signs of dehydration (extreme thirst, dry mouth, little or no urination, severe weakness)",
                        "Unable to keep liquids down for 24 hours",
                        "Bloody diarrhea or vomit",
                        "Fever above 102°F (39°C)",
                        "Diarrhea lasting more than 3 days",
                        "Severe abdominal or rectal pain",
                        "Symptoms in infants, elderly, pregnant women, or immunocompromised individuals"
                    ]
                },
                "prevention": [
                    "Wash hands thoroughly with soap and water, especially before handling food",
                    "Use safe water sources for drinking and food preparation",
                    "Cook foods to proper temperatures, especially meat, poultry, and eggs",
                    "Refrigerate perishable foods promptly",
                    "Wash fruits and vegetables thoroughly",
                    "Avoid cross-contamination of foods during preparation",
                    "Clean and disinfect surfaces regularly, especially in kitchens and bathrooms",
                    "Consider vaccination against rotavirus for infants"
                ]
            },
            "Peptic ulcer disease": {
                "overview": "Peptic ulcer disease involves open sores that develop on the inner lining of the stomach, upper small intestine, or esophagus. The most common causes are Helicobacter pylori (H. pylori) infection and long-term use of NSAIDs.",
                "lifestyle": {
                    "stress_management": [
                        "Practice relaxation techniques like deep breathing, meditation, or yoga",
                        "Get adequate sleep and rest",
                        "Engage in regular physical activity to reduce stress",
                        "Consider therapy or counseling if stress is significant"
                    ],
                    "habits_to_avoid": [
                        "Quit smoking, as it increases the risk of ulcers and slows healing",
                        "Limit or avoid alcohol consumption",
                        "Avoid taking NSAIDs like aspirin, ibuprofen, and naproxen when possible",
                        "If NSAIDs are necessary, take them with food and at the lowest effective dose"
                    ]
                },
                "diet": {
                    "eating_patterns": [
                        "Eat smaller, more frequent meals rather than large meals",
                        "Chew food thoroughly and eat slowly",
                        "Don't eat within 2-3 hours of bedtime",
                        "Stay upright for at least 1 hour after eating"
                    ],
                    "include": [
                        "High-fiber foods like fruits, vegetables, and whole grains",
                        "Foods rich in flavonoids, like apples, cranberries, onions, and garlic, which may inhibit H. pylori growth",
                        "Probiotic-rich foods like yogurt, which may help fight H. pylori infection",
                        "Green tea, which has antibacterial effects against H. pylori"
                    ],
                    "avoid": [
                        "Spicy foods if they cause discomfort",
                        "Acidic foods and beverages like citrus fruits and juices",
                        "Coffee and caffeinated drinks, which can increase stomach acid",
                        "Alcohol, which can irritate and erode the stomach lining",
                        "Milk and dairy (contrary to old advice, they don't help and may increase acid production)"
                    ]
                },
                "medical": {
                    "h_pylori_treatment": [
                        "Antibiotics to kill the bacteria (typically a combination of two antibiotics)",
                        "Proton pump inhibitors (PPIs) to reduce acid production",
                        "Bismuth salts may be added to help kill the bacteria and protect the stomach lining"
                    ],
                    "acid_reducers": [
                        "Proton pump inhibitors (PPIs) like omeprazole, lansoprazole, pantoprazole",
                        "H2 blockers like famotidine or cimetidine",
                        "Antacids for temporary symptom relief"
                    ],
                    "protective_medications": [
                        "Sucralfate, which coats and protects the ulcer surface",
                        "Misoprostol, which helps protect the stomach lining (often used with NSAIDs)",
                        "Bismuth subsalicylate, which may help protect the stomach lining and kill H. pylori"
                    ],
                    "when_to_seek_help": [
                        "Persistent abdominal pain that doesn't go away with antacids",
                        "Blood in stool (black or tarry stool) or vomit (which may look like coffee grounds)",
                        "Unintended weight loss or appetite changes",
                        "Persistent nausea or vomiting",
                        "Feeling faint or having trouble breathing",
                        "Ulcer symptoms when over 55 years old (higher risk of stomach cancer)"
                    ]
                },
                "prevention": [
                    "Consider alternatives to NSAIDs when possible",
                    "Take NSAIDs with food and liquid if they're necessary",
                    "Wash hands frequently to prevent H. pylori infection",
                    "Don't share utensils, food, or drinks",
                    "Drink water from clean, safe sources",
                    "Quit smoking and limit alcohol consumption",
                    "Manage stress through healthy coping mechanisms"
                ]
            },
            "Jaundice": {
                "overview": "Jaundice is a condition characterized by yellowing of the skin, whites of the eyes, and mucous membranes due to high levels of bilirubin in the blood. It's not a disease itself but a symptom of underlying conditions affecting the liver, bile ducts, or red blood cells.",
                "lifestyle": {
                    "rest_recovery": [
                        "Get plenty of rest to support the liver's recovery",
                        "Avoid strenuous physical activities until advised by your doctor",
                        "Maintain a regular sleep schedule"
                    ],
                    "hydration": [
                        "Drink plenty of water to help flush toxins from the body",
                        "Aim for at least 8-10 glasses of water daily",
                        "Consider herbal teas like ginger or dandelion tea, which may support liver function"
                    ],
                    "avoid": [
                        "Stop alcohol consumption completely as it puts additional stress on the liver",
                        "Avoid smoking and exposure to secondhand smoke",
                        "Minimize exposure to environmental toxins, harsh cleaning products, and pesticides"
                    ]
                },
                "diet": {
                    "include": [
                        "Fresh fruits and vegetables, especially those high in antioxidants",
                        "Fiber-rich foods to help eliminate bilirubin through stool",
                        "Lean proteins like fish, chicken, and plant-based proteins",
                        "Complex carbohydrates like whole grains",
                        "Turmeric, which has anti-inflammatory properties and may support liver health"
                    ],
                    "avoid": [
                        "Fatty, fried, and processed foods that can burden the liver",
                        "High-sugar foods and beverages",
                        "Excessive salt, which can cause fluid retention",
                        "Raw or undercooked shellfish, which may carry hepatitis",
                        "Supplements containing iron unless prescribed by your doctor"
                    ],
                    "special_considerations": [
                        "In cases of obstructive jaundice, a low-fat diet may be recommended",
                        "For infants with jaundice, continued breastfeeding is usually recommended",
                        "Small, frequent meals may be easier to digest than large meals",
                        "Stay well-hydrated to help eliminate bilirubin"
                    ]
                },
                "medical": {
                    "treatments": [
                        "Treatment depends on the underlying cause of jaundice",
                        "Medications to treat viral hepatitis or infections",
                        "Procedures to remove blockages in bile ducts if present",
                        "Phototherapy (light therapy) for infants with neonatal jaundice",
                        "Blood transfusions may be necessary in certain types of hemolytic anemia",
                        "In severe cases, plasmapheresis to filter the blood"
                    ],
                    "when_to_seek_help": [
                        "Yellowing of the skin or whites of the eyes",
                        "Dark-colored urine and/or clay-colored stools",
                        "Abdominal pain or swelling",
                        "Fever with jaundice",
                        "Extreme fatigue or confusion",
                        "For infants: excessive sleepiness, difficulty waking or feeding, high-pitched crying"
                    ]
                },
                "prevention": [
                    "Maintain good personal hygiene to prevent hepatitis A and E",
                    "Get vaccinated against hepatitis A and B if recommended",
                    "Don't share needles, razors, toothbrushes, or other personal items",
                    "Practice safe sex to prevent transmission of hepatitis B and C",
                    "Limit alcohol consumption",
                    "Take medications as prescribed and inform your doctor of all medications you're taking",
                    "Avoid unnecessary exposure to chemicals and toxins",
                    "Get regular check-ups if you have risk factors for liver disease"
                ],
                "specific_types": {
                    "neonatal_jaundice": [
                        "Ensure regular feeding for newborns to encourage bowel movements",
                        "Expose infant to indirect sunlight for short periods (as advised by doctor)",
                        "Watch for signs of severe jaundice like extreme yellowing, lethargy, or difficulty feeding",
                        "Follow up with healthcare provider as recommended"
                    ]
                }
            }
        }
        
    def get_health_recommendations(self, disease):
        """Get comprehensive health recommendations for a specific disease"""
        return self.recommendations.get(disease, None)
    
    def get_lifestyle_recommendations(self, disease):
        """Get lifestyle recommendations for a specific disease"""
        disease_recommendations = self.recommendations.get(disease, None)
        if disease_recommendations:
            return disease_recommendations.get("lifestyle", None)
        return None
    
    def get_diet_recommendations(self, disease):
        """Get dietary recommendations for a specific disease"""
        disease_recommendations = self.recommendations.get(disease, None)
        if disease_recommendations:
            return disease_recommendations.get("diet", None)
        return None
    
    def get_medical_recommendations(self, disease):
        """Get medical recommendations for a specific disease"""
        disease_recommendations = self.recommendations.get(disease, None)
        if disease_recommendations:
            return disease_recommendations.get("medical", None)
        return None
    
    def get_prevention_tips(self, disease):
        """Get prevention tips for a specific disease"""
        disease_recommendations = self.recommendations.get(disease, None)
        if disease_recommendations:
            return disease_recommendations.get("prevention", [])
        return []

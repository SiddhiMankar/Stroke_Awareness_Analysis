import pandas as pd
import re
from datetime import datetime

# === Step 1: Load your cleaned dataset ===
file_path = "C:/Users/S.D.M/stroke_ml_project/cleaned_data_unique.csv"  # update filename
df = pd.read_csv(file_path, encoding='utf-8')

print("✅ Dataset loaded successfully!")
print(f"Columns before cleaning: {len(df.columns)}")

# === Step 2: Basic normalization ===
def clean_column_name(name):
    # lowercase, remove leading/trailing spaces
    name = name.strip().lower()
    # replace spaces, hyphens, slashes, and special chars with underscores
    name = re.sub(r'[\s\-/(),:\[\]\?]+', '_', name)
    # remove multiple underscores and trailing underscores
    name = re.sub(r'_+', '_', name).strip('_')
    return name

df.columns = [clean_column_name(col) for col in df.columns]

# === Step 3: Manual unification for known variations ===
rename_map = {
    'name': 'name',
    'phone_number': 'phone',
    'email_id': 'email',
    'age': 'age',
    'gender': 'gender',
    'marital_status': 'marital_status',
    'medical_history': 'medical_history',
    'how_often_do_you_check_your_blood_pressure_bp': 'bp_check_freq',
    'how_often_do_you_check_your_blood_sugar': 'sugar_check_freq',
    'how_often_do_you_check_your_cholesterol': 'cholesterol_check_freq',
    'how_often_do_you_check_your_thyroid_hormones': 'thyroid_check_freq',
    'for_females_have_you_ever_taken_oral_contraceptives_or_hormonal_therapy': 'female_hormonal_therapy',
    'what_is_your_current_weight_in_kilograms': 'weight_kg',
    'what_is_your_current_height_in_cms': 'height_cm',
    'height_in_m': 'height_m',
    'bmi': 'bmi',
    'range': 'bmi_range',
    'have_you_experienced_any_of_the_following_warning_signs': 'warning_signs',
    'if_you_experience_symptoms_of_warning_signs_which_specialist_would_you_consult': 'specialist_to_consult',
    'do_you_consume_alcohol': 'alcohol',
    'do_you_smoke_if_so_how_much_and_often': 'smoking',
    'do_you_engage_in_regular_physical_activity_or_exercise': 'physical_activity',
    'what_if_your_typical_diet': 'typical_diet',
    "do_you_have_any_preference_for_junk_food_like_mcdonald's_burger_how_often_do_you_ask_for_outside_food_like_zomato_swiggy": 'junk_food_freq',
    'do_you_currently_take_any_medications': 'current_medications',
    'have_you_ever_received_abnormal_results_in_your_blood_tests_such_as_high_cholesterol_levels': 'abnormal_blood_tests',
    'do_you_currently_have_any_complaints_or_health_issues_related_to_your_heart_or_kidneys_"=': 'heart_kidney_issues',
    'salary': 'salary',
    'how_many_family_members_are_dependent_on_you_financially_or_otherwise': 'dependents_count',
    'do_you_have_a_family_history_of_brain_or_heart_stroke_of_hypertension_or_diabetes': 'family_history',
    'education_level': 'education',
    'profession': 'profession',
    'do_you_currently_have_medical_insurance': 'medical_insurance',
    'please_indicate_how_your_medical_insurance_coverage_is_obtained': 'insurance_source',
    'does_your_insurance_plan_provide_coverage_for_your_family_members_as_well': 'insurance_family',
    'do_you_know_what_is_a_brain_stroke': 'know_stroke',
    'what_are_the_symptoms_of_brain_stroke': 'stroke_symptoms',
    'what_are_the_risk_factors_for_brain_stroke': 'stroke_risk_factors',
    'where_would_you_go_if_you_or_someone_you_know_experienced_symptoms_of_a_brain_stroke_to_a_local_doctor_or_to_the_hospital': 'place_to_go',
    'how_soon_do_you_think_medical_treatment_should_be_sought_after_noticing_symptoms_of_a_brain_stroke_immediately_or_at_the_opportune_time': 'treatment_timing',
    'whom_would_you_contact_first_if_you_or_someone_you_know_experiences_symptoms_of_a_brain_stroke_the_doctor_family_member_or_a_friend': 'contact_first',
    'what_advice_would_you_give_if_someone_you_know_experiences_symptoms_of_a_brain_stroke': 'advice_if_stroke',
    'if_you_are_aware_of_brain_stroke_how_did_you_learn_about_it': 'stroke_info_source',
    'do_you_think_sudden_confusion_trouble_speaking_or_understanding_speech_is_a_stroke_symptom': 'confusion_symptom',
    'do_you_think_sudden_nosebleed_is_a_stroke_of_symptom': 'nosebleed_symptom',
    'do_you_think_sudden_numbness_or_weakness_of_face_arm_or_leg_is_a_symptom_of_stroke': 'numbness_symptom',
    'do_you_think_trouble_seeing_in_one_or_both_the_eyes_is_a_stroke_symptom': 'vision_symptom',
    'how_soon_would_you_consult_a_specialist_after_experiencing_the_first_symptom': 'consult_timing',
    "if_'other'_please_specify.": 'other_specify_1',
    "if_'yes'_please_specify.": 'yes_specify_1',
    'if_yes_mention_the_type_of_exercise.': 'exercise_type',
    "if_'yes'_please_specify..1": 'yes_specify_2',
    "if_'yes'_please_specify..2": 'yes_specify_3',
    'if_other_please_specify': 'other_specify_2',
    "if_'other'_please_specify": 'other_specify_3',
    'how_often': 'frequency',
    'language': 'language',
    'location': 'location',
    'tia': 'tia',
    'source': 'source',
    'timestamp': 'timestamp',
    'contact_number.1': 'phone_alt',
    'email_id.1': 'email_alt',
    'gender.1': 'gender_alt',
    'salaried': 'salaried',
    'where_would_you_go_if_you_or_someone_you_know_experienced_symptoms_of_a_brain_stroke_to_a_local_doctor_or_to_the_hospital_.1': 'place_to_go_alt',
    'how_soon_do_you_think_medical_treatment_should_be_sought_after_noticing_symptoms_of_a_brain_stroke_immediately_or_at_the_opportune_time_.1': 'treatment_timing_alt',
    "if_'yes'_please_specify..3": 'yes_specify_4',
    'what_is_your_current_weight_in_kilograms_.1': 'weight_kg_alt',
    'bmi_range': 'bmi_range_alt',
    'do_you_engage_regular_physical_activity_or_exercise': 'physical_activity_alt',
    'what_is_your_typical_diet': 'typical_diet_alt',
    'high_blood_pressure': 'high_bp',
    'diabetes': 'diabetes',
    'high_cholesterol': 'high_cholesterol',
    'irregular_heartbeats': 'irregular_heartbeats',
    'other': 'other_conditions',
    'how_often_do_you_check_your_blood_pressure_bp_and_blood_sugar_in_case_you_have_one': 'bp_sugar_check_freq',
    'do_you_currently_take_medications': 'current_medications_alt',
    "if_'yes'_please_specify": 'yes_specify_5',
    'do_you_smoke': 'smoking_alt',
    'do_you_have_a_family_history_of_brain_or_heart_stroke_of_hypertension_or_diabetes_.1': 'family_history_alt',
    'do_you_currently_have_medical_insurance_*': 'medical_insurance_alt',
    'please_indicate_how_your_medical_insurance_coverages_obtained': 'insurance_source_alt',
    'do_you_thin_medical_insurance_is_mandatory': 'insurance_mandatory',
    'do_you_know_what_is_brain_stroke': 'know_stroke_alt',
    'do_you_think_brain_stroke_heart_attack_or_kidney_failures_are_interrelated': 'stroke_heart_kidney_link',
    'what_are_the_symptoms_of_brain_stroke_.1': 'stroke_symptoms_alt',
    'where_would_you_go_if_you_or_someone_you_know_experienced_symptoms_of_a_brain_stroke': 'place_to_go_final',
    'whom_would_you_contact_first_if_you_or_someone_you_know_experiences_symptoms_of_a_brain_stroke': 'contact_first_final',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_high_blood_pressure': 'risk_high_bp',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_diabetes': 'risk_diabetes',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_smoking': 'risk_smoking',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_alcohol_abuse': 'risk_alcohol',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_stress': 'risk_stress',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_obesity': 'risk_obesity',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_lifestyle': 'risk_lifestyle',
    'do_you_think_any_of_the_following_is_risk_factor_for_brain_stroke_lack_of_exercise': 'risk_no_exercise',
    'location.1': 'location_alt1',
    'medical_history_high_blood_pressure': 'history_high_bp',
    'medical_history_diabetes': 'history_diabetes',
    'medical_history_high_cholesterol': 'history_high_cholesterol',
    'medical_history_irregular_heartbeats': 'history_irregular_heartbeats',
    'location.2': 'location_alt2'
}


df.rename(columns={old: new for old, new in rename_map.items() if old in df.columns}, inplace=True)

# === Step 4: Save cleaned dataset with new column names ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"C:/Users/S.D.M/stroke_ml_project/standardized_columns_{timestamp}.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print("\n✅ Column names standardized and saved!")
print(f"Total Columns: {len(df.columns)}")
print(f"✅ Cleaned file saved to: {output_path}\n")

# === Step 5: Preview a few columns ===
print("Sample of cleaned column names:")
print(df.columns[:].tolist())
# === Step 6: Remove exact duplicate columns ===
df = df.loc[:, ~df.columns.duplicated()]

# === Step 7: Clean column suffixes (.1, .2, etc.) and unify duplicates ===
df.columns = df.columns.str.replace(r'\.\d+$', '', regex=True)

# After cleaning, re-remove any duplicates that may appear after renaming
df = df.loc[:, ~df.columns.duplicated()]

print("\n✅ Duplicate columns removed and suffixes cleaned!")
print(f"Remaining columns: {len(df.columns)}")
import pandas as pd

# Dictionary to rename columns
rename_dict = {
    'name': 'name',
    'phone_number': 'phone',
    'email_id': 'email',
    'age': 'age',
    'gender': 'gender',
    'marital_status': 'marital_status',
    'medical_history': 'medical_history',
    'how_often_do_you_check_your_blood_pressure_bp': 'bp_check_frequency',
    'how_often_do_you_check_your_blood_sugar': 'blood_sugar_check_frequency',
    'how_often_do_you_check_your_cholesterol': 'cholesterol_check_frequency',
    'how_often_do_you_check_your_thyroid_hormones': 'thyroid_check_frequency',
    'for_females_have_you_ever_taken_oral_contraceptives_or_hormonal_therapy': 'female_hormonal_therapy',
    'what_is_your_current_weight_in_kilograms': 'weight_kg',
    'what_is_your_current_height_in_cms': 'height_cm',
    'height_in_m': 'height_m',
    'bmi': 'bmi',
    'range': 'bmi_range',
    'have_you_experienced_any_of_the_following_warning_signs': 'warning_signs',
    'if_you_experience_symptoms_of_warning_signs_which_specialist_would_you_consult': 'specialist_consult',
    'do_you_consume_alcohol': 'alcohol',
    'do_you_smoke_if_so_how_much_and_often': 'smoking',
    'do_you_engage_in_regular_physical_activity_or_exercise': 'physical_activity',
    'what_if_your_typical_diet': 'typical_diet',
    "do_you_have_any_preference_for_junk_food_like_mcdonald's_burger_how_often_do_you_ask_for_outside_food_like_zomato_swiggy": 'junk_food_frequency',
    'do_you_currently_take_any_medications': 'current_medications',
    'have_you_ever_received_abnormal_results_in_your_blood_tests_such_as_high_cholesterol_levels': 'abnormal_blood_tests',
    'do_you_currently_have_any_complaints_or_health_issues_related_to_your_heart_or_kidneys_"=': 'heart_kidney_issues',
    'salary': 'salary',
    'how_many_family_members_are_dependent_on_you_financially_or_otherwise': 'dependents_count',
    'do_you_have_a_family_history_of_brain_or_heart_stroke_of_hypertension_or_diabetes': 'family_history_stroke_diabetes',
    'education_level': 'education',
    'profession': 'profession',
    'do_you_currently_have_medical_insurance': 'medical_insurance',
    'please_indicate_how_your_medical_insurance_coverage_is_obtained': 'insurance_source',
    # ... you can continue for all long columns
}

# Apply renaming
df.rename(columns=rename_dict, inplace=True)

# Save to a new CSV without overwriting
output_path = "C:/Users/S.D.M/stroke_ml_project/big_dataset_renamed.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print("✅ Columns renamed and saved to:", output_path)

# Save again
output_path = "C:/Users/S.D.M/stroke_ml_project/final_standardized_dataset.csv"
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"💾 Final standardized dataset saved to: {output_path}")

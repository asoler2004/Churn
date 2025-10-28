#!/usr/bin/env python3
"""
Test script for email marketing campaign functionality
"""

import pandas as pd
import numpy as np
from faker import Faker
import sys
import os

# Add the current directory to Python path to import from streamlit_ui
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from streamlit_ui import (
        generate_email_campaign_content,
        create_bulk_email_campaign,
        export_email_campaign_data,
        load_sample_data
    )
    print("✅ Successfully imported email marketing functions")
except ImportError as e:
    print(f"❌ Failed to import functions: {e}")
    sys.exit(1)

def test_email_campaign_generation():
    """Test email campaign content generation"""
    print("\n🧪 Testing Email Campaign Generation...")
    
    # Create sample customer data
    fake = Faker()
    sample_customer = {
        'Name': fake.first_name(),
        'Surname': fake.last_name(),
        'email': fake.email(),
        'age': 35,
        'credit_score': 720,
        'housing': 'o',
        'app_downloaded': 1,
        'cc_taken': 0,
        'purchases': 15,
        'deposits': 8,
        'rewards_earned': 250,
        'risk_level_XGB': 'High',
        'churn_probability_XGB': 0.75
    }
    
    # Test different campaign types
    campaign_types = ['retention', 'engagement', 'loyalty']
    
    for campaign_type in campaign_types:
        print(f"\n📧 Testing {campaign_type} campaign...")
        
        try:
            campaign_content = generate_email_campaign_content(
                sample_customer,
                campaign_type=campaign_type,
                personalization_level='high'
            )
            
            # Verify campaign content structure
            required_keys = ['subject_lines', 'email_content', 'campaign_metrics', 'customer_segment']
            for key in required_keys:
                if key not in campaign_content:
                    print(f"❌ Missing key: {key}")
                    return False
            
            # Verify subject lines
            if len(campaign_content['subject_lines']) < 1:
                print(f"❌ No subject lines generated for {campaign_type}")
                return False
            
            # Verify email content contains customer name
            if sample_customer['Name'] not in campaign_content['email_content']:
                print(f"❌ Customer name not found in email content for {campaign_type}")
                return False
            
            # Verify HTML structure
            if '<html>' not in campaign_content['email_content'] or '</html>' not in campaign_content['email_content']:
                print(f"❌ Invalid HTML structure for {campaign_type}")
                return False
            
            print(f"✅ {campaign_type.title()} campaign generated successfully")
            print(f"   - Subject lines: {len(campaign_content['subject_lines'])}")
            print(f"   - Customer segment: {campaign_content['customer_segment']}")
            print(f"   - Expected open rate: {campaign_content['campaign_metrics']['expected_open_rate']}")
            
        except Exception as e:
            print(f"❌ Error generating {campaign_type} campaign: {e}")
            return False
    
    return True

def test_bulk_campaign_creation():
    """Test bulk email campaign creation"""
    print("\n🧪 Testing Bulk Campaign Creation...")
    
    try:
        # Load sample data
        sample_data = load_sample_data()
        
        # Add some prediction data
        sample_data['risk_level_XGB'] = np.random.choice(['High', 'Medium', 'Low'], len(sample_data))
        sample_data['churn_probability_XGB'] = np.random.uniform(0.1, 0.9, len(sample_data))
        
        # Take first 10 customers for testing
        test_customers = sample_data.head(10)
        
        campaign_settings = {
            'campaign_type': 'retention',
            'personalization_level': 'high'
        }
        
        # Create bulk campaign
        campaign_df = create_bulk_email_campaign(test_customers, campaign_settings)
        
        # Verify campaign dataframe structure
        required_columns = [
            'customer_id', 'name', 'surname', 'email', 'risk_level',
            'churn_probability', 'subject_line', 'email_content',
            'customer_segment', 'expected_open_rate'
        ]
        
        for col in required_columns:
            if col not in campaign_df.columns:
                print(f"❌ Missing column in campaign dataframe: {col}")
                return False
        
        # Verify data integrity
        if len(campaign_df) != len(test_customers):
            print(f"❌ Campaign dataframe length mismatch: {len(campaign_df)} vs {len(test_customers)}")
            return False
        
        # Verify all emails have content
        empty_content = campaign_df['email_content'].isna().sum()
        if empty_content > 0:
            print(f"❌ {empty_content} emails have empty content")
            return False
        
        print(f"✅ Bulk campaign created successfully")
        print(f"   - Total emails: {len(campaign_df)}")
        print(f"   - Risk distribution: {campaign_df['risk_level'].value_counts().to_dict()}")
        print(f"   - Segments: {campaign_df['customer_segment'].nunique()}")
        
        return True  # Return True instead of DataFrame to match test pattern
        
    except Exception as e:
        print(f"❌ Error creating bulk campaign: {e}")
        return False

def test_campaign_export():
    """Test campaign export functionality"""
    print("\n🧪 Testing Campaign Export...")
    
    # Create a small test campaign
    test_data = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'name': ['Juan', 'María', 'Carlos'],
        'surname': ['Pérez', 'García', 'López'],
        'email': ['juan@test.com', 'maria@test.com', 'carlos@test.com'],
        'risk_level': ['High', 'Medium', 'Low'],
        'churn_probability': [0.8, 0.5, 0.2],
        'subject_line': ['Test Subject 1', 'Test Subject 2', 'Test Subject 3'],
        'email_content': ['<html><body>Test 1</body></html>'] * 3,
        'customer_segment': ['High Risk - Urgent Retention'] * 3,
        'expected_open_rate': ['25-35%'] * 3,
        'recommended_send_time': ['Martes-Jueves, 10:00-14:00'] * 3
    })
    
    try:
        # Test CSV export
        csv_export = export_email_campaign_data(test_data, "csv")
        if not csv_export or len(csv_export) < 100:  # Should have headers + data
            print("❌ CSV export failed or too short")
            return False
        print("✅ CSV export successful")
        
        # Test HTML preview export
        html_export = export_email_campaign_data(test_data, "html_preview")
        if not html_export or '<html>' not in html_export:
            print("❌ HTML preview export failed")
            return False
        print("✅ HTML preview export successful")
        
        # Test summary export
        summary_export = export_email_campaign_data(test_data, "summary")
        if not summary_export or 'RESUMEN DE CAMPAÑA' not in summary_export:
            print("❌ Summary export failed")
            return False
        print("✅ Summary export successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing campaign export: {e}")
        return False

def test_personalization_levels():
    """Test different personalization levels"""
    print("\n🧪 Testing Personalization Levels...")
    
    sample_customer = {
        'Name': 'Ana',
        'Surname': 'Martínez',
        'email': 'ana@test.com',
        'age': 28,
        'credit_score': 680,
        'housing': 'r',
        'app_downloaded': 0,
        'cc_taken': 1,
        'purchases': 20,
        'deposits': 5,
        'rewards_earned': 150,
        'risk_level_XGB': 'Medium',
        'churn_probability_XGB': 0.45
    }
    
    personalization_levels = ['high', 'medium', 'basic']
    
    for level in personalization_levels:
        try:
            campaign_content = generate_email_campaign_content(
                sample_customer,
                campaign_type='engagement',
                personalization_level=level
            )
            
            # Verify personalization
            email_content = campaign_content['email_content']
            
            # All levels should include customer name
            if sample_customer['Name'] not in email_content:
                print(f"❌ Customer name missing in {level} personalization")
                return False
            
            # High personalization should include more details
            if level == 'high':
                # Check if credit score is mentioned (could be formatted differently)
                credit_score_str = str(int(sample_customer['credit_score']))
                if credit_score_str not in email_content and 'puntaje crediticio' not in email_content.lower():
                    print(f"❌ Credit score or credit reference missing in high personalization")
                    return False
            
            print(f"✅ {level.title()} personalization working correctly")
            
        except Exception as e:
            print(f"❌ Error testing {level} personalization: {e}")
            return False
    
    return True

def test_risk_level_segmentation():
    """Test risk level based segmentation"""
    print("\n🧪 Testing Risk Level Segmentation...")
    
    base_customer = {
        'Name': 'Test',
        'Surname': 'Customer',
        'email': 'test@test.com',
        'age': 30,
        'credit_score': 650,
        'housing': 'o',
        'app_downloaded': 1,
        'cc_taken': 0,
        'purchases': 10,
        'deposits': 5,
        'rewards_earned': 100
    }
    
    risk_levels = [
        ('High', 0.8),
        ('Medium', 0.5),
        ('Low', 0.2)
    ]
    
    for risk_level, churn_prob in risk_levels:
        try:
            test_customer = base_customer.copy()
            test_customer['risk_level_XGB'] = risk_level
            test_customer['churn_probability_XGB'] = churn_prob
            
            campaign_content = generate_email_campaign_content(
                test_customer,
                campaign_type='retention',
                personalization_level='high'
            )
            
            # Verify risk-appropriate content
            subject_lines = campaign_content['subject_lines']
            email_content = campaign_content['email_content']
            
            if risk_level == 'High':
                # High risk should have urgent language
                urgent_found = any('🚨' in subject or 'IMPORTANTE' in subject for subject in subject_lines)
                if not urgent_found:
                    print(f"❌ High risk campaign missing urgent indicators")
                    return False
            
            elif risk_level == 'Low':
                # Low risk should have positive language
                positive_found = any('🎁' in subject or 'gracias' in subject.lower() for subject in subject_lines)
                if not positive_found:
                    print(f"❌ Low risk campaign missing positive indicators")
                    return False
            
            print(f"✅ {risk_level} risk segmentation working correctly")
            
        except Exception as e:
            print(f"❌ Error testing {risk_level} risk segmentation: {e}")
            return False
    
    return True

def main():
    """Run all email marketing tests"""
    print("🚀 Starting Email Marketing Campaign Tests")
    print("=" * 50)
    
    tests = [
        ("Email Campaign Generation", test_email_campaign_generation),
        ("Bulk Campaign Creation", test_bulk_campaign_creation),
        ("Campaign Export", test_campaign_export),
        ("Personalization Levels", test_personalization_levels),
        ("Risk Level Segmentation", test_risk_level_segmentation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "="*50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All email marketing tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
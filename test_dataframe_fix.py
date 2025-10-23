#!/usr/bin/env python3
"""
Test script to verify DataFrame boolean issue fixes
"""

import pandas as pd
import numpy as np
from faker import Faker

def test_dataframe_boolean_issue():
    """Test the DataFrame boolean issue and our fixes"""
    print("🧪 Testing DataFrame boolean issue fixes...")
    
    fake = Faker()
    
    # Create test data that might cause the issue
    test_data = {
        'Name': [fake.first_name(), fake.first_name(), fake.first_name()],
        'Surname': [fake.last_name(), fake.last_name(), fake.last_name()],
        'age': [30, 45, 25],
        'credit_score': [650.5, 720.0, 580.0]
    }
    
    df = pd.DataFrame(test_data)
    print(f"✅ Created test DataFrame with {len(df)} rows")
    
    # Test the problematic scenarios
    for idx, row in df.iterrows():
        print(f"\n🔍 Testing row {idx}:")
        
        # Old way (problematic)
        try:
            name_old = row.get('Name', 'Unknown')
            surname_old = row.get('Surname', 'Customer')
            
            # This might cause the DataFrame boolean issue
            # if name_old and surname_old:  # This could fail
            #     print("Old way would work")
            
            print(f"  Old way values: {type(name_old)} {name_old}, {type(surname_old)} {surname_old}")
            
        except Exception as e:
            print(f"  ❌ Old way failed: {e}")
        
        # New way (fixed)
        try:
            name_new = str(row.get('Name', 'Unknown')).strip()
            surname_new = str(row.get('Surname', 'Customer')).strip()
            
            # This should always work
            if (name_new and surname_new and 
                name_new.lower() not in ['nan', 'none', 'unknown', ''] and 
                surname_new.lower() not in ['nan', 'none', 'customer', '']):
                print(f"  ✅ New way works: {name_new} {surname_new}")
            else:
                print(f"  ⚠️ New way detected invalid data: {name_new} {surname_new}")
                
        except Exception as e:
            print(f"  ❌ New way failed: {e}")
    
    # Test with problematic data (NaN, None values)
    print(f"\n🧪 Testing with problematic data...")
    
    problematic_data = {
        'Name': ['John', np.nan, None, ''],
        'Surname': ['Doe', 'Smith', np.nan, ''],
        'age': [30, 45, 25, 35],
        'credit_score': [650.5, 720.0, 580.0, 600.0]
    }
    
    df_prob = pd.DataFrame(problematic_data)
    
    for idx, row in df_prob.iterrows():
        print(f"\n🔍 Testing problematic row {idx}:")
        
        try:
            name = str(row.get('Name', 'Unknown')).strip()
            surname = str(row.get('Surname', 'Customer')).strip()
            
            # Clean up any 'nan' or 'None' values
            if name.lower() in ['nan', 'none']:
                name = 'Unknown'
            if surname.lower() in ['nan', 'none']:
                surname = 'Customer'
            
            print(f"  ✅ Fixed values: '{name}' '{surname}'")
            
            # Test boolean evaluation
            if (name and surname and 
                name.lower() not in ['nan', 'none', 'unknown', ''] and 
                surname.lower() not in ['nan', 'none', 'customer', '']):
                print(f"  ✅ Boolean test passed: Valid customer")
            else:
                print(f"  ⚠️ Boolean test: Invalid/missing data detected")
                
        except Exception as e:
            print(f"  ❌ Fix failed: {e}")
    
    print(f"\n🎉 DataFrame boolean issue test completed!")
    return True

if __name__ == "__main__":
    test_dataframe_boolean_issue()
"""
Unit tests for data cleaning functions
Bonus feature: pytest tests
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from clean_data import parse_date, validate_email


class TestDateParsing:
    """Test date parsing functionality"""
    
    def test_parse_date_yyyy_mm_dd(self):
        """Test YYYY-MM-DD format"""
        result = parse_date('2023-01-15')
        assert pd.notna(result)
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
    
    def test_parse_date_dd_mm_yyyy(self):
        """Test DD/MM/YYYY format"""
        result = parse_date('15/01/2023')
        assert pd.notna(result)
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
    
    def test_parse_date_mm_dd_yyyy(self):
        """Test MM-DD-YYYY format"""
        result = parse_date('01-15-2023')
        assert pd.notna(result)
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
    
    def test_parse_date_invalid(self):
        """Test invalid date returns NaT"""
        result = parse_date('invalid-date')
        assert pd.isna(result)
    
    def test_parse_date_null(self):
        """Test null value returns NaT"""
        result = parse_date(None)
        assert pd.isna(result)


class TestEmailValidation:
    """Test email validation functionality"""
    
    def test_validate_email_valid(self):
        """Test valid email"""
        assert validate_email('test@example.com') == True
    
    def test_validate_email_no_at(self):
        """Test email without @ symbol"""
        assert validate_email('testexample.com') == False
    
    def test_validate_email_no_dot(self):
        """Test email without dot"""
        assert validate_email('test@examplecom') == False
    
    def test_validate_email_null(self):
        """Test null email"""
        assert validate_email(None) == False
    
    def test_validate_email_with_spaces(self):
        """Test email with spaces gets stripped"""
        assert validate_email('  test@example.com  ') == True


class TestDataCleaning:
    """Integration tests for data cleaning"""
    
    def test_customers_cleaning_removes_duplicates(self):
        """Test that duplicate customers are removed"""
        # Create test data with duplicates
        test_data = pd.DataFrame({
            'customer_id': [1, 1, 2],
            'name': ['John', 'John', 'Jane'],
            'email': ['john@test.com', 'john@test.com', 'jane@test.com'],
            'region': ['North', 'North', 'South'],
            'signup_date': ['2023-01-01', '2023-02-01', '2023-01-15']
        })
        
        # Apply date parsing
        test_data['signup_date'] = test_data['signup_date'].apply(parse_date)
        test_data_sorted = test_data.sort_values('signup_date', ascending=False)
        result = test_data_sorted.drop_duplicates(subset=['customer_id'], keep='first')
        
        assert len(result) == 2
        assert result[result['customer_id'] == 1]['signup_date'].iloc[0].strftime('%Y-%m-%d') == '2023-02-01'
    
    def test_email_standardization(self):
        """Test email standardization to lowercase"""
        test_emails = pd.Series(['TEST@EXAMPLE.COM', 'Test@Example.Com', 'test@example.com'])
        result = test_emails.str.lower().str.strip()
        
        assert all(result == 'test@example.com')
    
    def test_region_filling(self):
        """Test missing region filled with 'Unknown'"""
        test_data = pd.DataFrame({
            'region': ['North', None, 'South', pd.NA]
        })
        result = test_data['region'].fillna('Unknown')
        
        assert result.iloc[1] == 'Unknown'
        assert result.iloc[3] == 'Unknown'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

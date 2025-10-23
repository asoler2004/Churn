# 📧 Email Marketing Campaign Feature

## Overview

The Email Marketing Campaign feature leverages customer analysis data from the churn prediction system to create personalized, targeted email campaigns. This feature integrates seamlessly with the existing customer filtering and batch analysis functionality.

## 🎯 Key Features

### 1. **Intelligent Segmentation**
- Automatic customer segmentation based on churn risk levels
- Personalized campaign strategies for each risk category
- Integration with existing customer filters and analysis

### 2. **Personalized Content Generation**
- Dynamic email content based on customer profile
- Multiple personalization levels (High, Medium, Basic)
- Spanish-language templates with professional design

### 3. **Campaign Types**
- **🚨 Retention Campaigns**: For high-risk customers requiring immediate intervention
- **💡 Engagement Campaigns**: For medium-risk customers needing proactive engagement
- **🏆 Loyalty Campaigns**: For low-risk customers to maintain satisfaction

### 4. **Export & Integration**
- CSV export for email marketing platforms
- HTML preview for campaign review
- Mailchimp-compatible format
- Campaign summary reports

## 🚀 How to Use

### Step 1: Filter Your Customers
1. Go to the **"📊 Datos de Clientes"** tab
2. Apply filters to target specific customer segments
3. Review the filtered customer list

### Step 2: Run Batch Analysis (Optional but Recommended)
1. Navigate to **"📊 Análisis Masivo"** tab
2. Enable **"🤖 Incluir Predicciones de Abandono"**
3. Click **"🚀 Iniciar Análisis Masivo"**
4. Wait for predictions to complete

### Step 3: Create Email Campaign
1. Go to **"📧 Email Marketing"** tab
2. Configure campaign settings:
   - **Campaign Type**: Choose based on your objective
   - **Personalization Level**: Select detail level
   - **Use Predictions**: Enable if batch analysis was completed
3. Click **"🚀 Generar Campaña de Email"**

### Step 4: Review and Export
1. Review campaign statistics and segmentation
2. Preview individual emails
3. Export in your preferred format:
   - **📊 CSV**: Complete campaign data
   - **🌐 HTML**: Email previews
   - **📋 Summary**: Campaign overview
   - **📮 Mailchimp**: Ready-to-import format

## 📊 Campaign Types Explained

### 🚨 Retention Campaigns (High Risk)
**Target**: Customers with high churn probability (>60%)
**Strategy**: Urgent intervention with immediate value offers
**Features**:
- Urgent subject lines with alert emojis
- Exclusive offers and bonuses
- Premium support access
- 24-48 hour response timeframe

**Example Subject**: "🚨 IMPORTANTE: Ana, te extrañamos - Oferta exclusiva dentro"

### 💡 Engagement Campaigns (Medium Risk)
**Target**: Customers with medium churn probability (30-60%)
**Strategy**: Proactive engagement with personalized recommendations
**Features**:
- Opportunity-focused subject lines
- Product recommendations based on profile
- Educational content
- Feature highlights

**Example Subject**: "💡 Oportunidad especial: Ana, nuevas funciones que te encantarán"

### 🏆 Loyalty Campaigns (Low Risk)
**Target**: Customers with low churn probability (<30%)
**Strategy**: Maintain satisfaction and build long-term loyalty
**Features**:
- Appreciation-focused messaging
- Exclusive benefits and early access
- VIP treatment offers
- Community building

**Example Subject**: "🎁 Para ti: Ana, gracias por ser parte de nuestra familia"

## 🎨 Personalization Levels

### High Personalization
- Customer name and surname
- Specific credit score mentions
- Detailed activity metrics
- Tailored product recommendations
- Risk-specific messaging

### Medium Personalization
- Customer name
- General activity patterns
- Basic product suggestions
- Standard risk messaging

### Basic Personalization
- Customer name only
- Generic content
- Standard offers

## 📈 Expected Performance Metrics

| Risk Level | Expected Open Rate | Expected Click Rate | Recommended Send Time |
|------------|-------------------|--------------------|--------------------|
| High       | 25-35%           | 8-12%              | Immediate          |
| Medium     | 20-30%           | 5-8%               | 2-3 days           |
| Low        | 15-25%           | 3-6%               | Within a week      |

## 🔧 Technical Implementation

### Core Functions

#### `generate_email_campaign_content(customer_data, campaign_type, personalization_level)`
Generates personalized email content for individual customers.

**Parameters**:
- `customer_data`: Dictionary with customer information
- `campaign_type`: "retention", "engagement", or "loyalty"
- `personalization_level`: "high", "medium", or "basic"

**Returns**: Dictionary with subject lines, email content, and campaign metrics

#### `create_bulk_email_campaign(filtered_customers, campaign_settings)`
Creates bulk email campaigns for multiple customers.

**Parameters**:
- `filtered_customers`: DataFrame with customer data
- `campaign_settings`: Dictionary with campaign configuration

**Returns**: DataFrame with complete campaign data

#### `export_email_campaign_data(campaign_df, format_type)`
Exports campaign data in various formats.

**Supported Formats**:
- `"csv"`: Complete campaign data
- `"html_preview"`: HTML email previews
- `"summary"`: Campaign summary report

## 📋 Data Requirements

### Required Customer Fields
- `Name`: Customer first name
- `Surname`: Customer last name
- `email`: Customer email address
- `age`: Customer age
- `credit_score`: Credit score
- `housing`: Housing status
- `app_downloaded`: Mobile app usage
- `cc_taken`: Credit card status
- `purchases`: Purchase activity
- `deposits`: Deposit activity
- `rewards_earned`: Rewards points

### Optional Prediction Fields
- `risk_level_XGB`: Churn risk level (High/Medium/Low)
- `churn_probability_XGB`: Churn probability (0-1)

## 🎯 Best Practices

### Campaign Timing
1. **High Risk**: Send immediately (within 24 hours)
2. **Medium Risk**: Send within 2-3 days
3. **Low Risk**: Send within a week

### Follow-up Strategy
- High risk: Follow up in 3 days if no response
- Medium risk: Follow up in 7 days
- Low risk: Follow up in 14 days

### A/B Testing
- Test different subject lines
- Compare personalization levels
- Measure campaign effectiveness
- Adjust strategies based on results

### Monitoring
- Track open rates by segment
- Monitor click-through rates
- Analyze conversion rates
- Review unsubscribe rates

## 🔍 Troubleshooting

### Common Issues

**Issue**: No customers in filtered data
**Solution**: Adjust filters in the "Datos de Clientes" tab

**Issue**: Missing prediction data
**Solution**: Run batch analysis first or disable prediction usage

**Issue**: Email content appears generic
**Solution**: Increase personalization level or ensure customer data is complete

**Issue**: Export files are empty
**Solution**: Verify campaign was generated successfully before exporting

## 🚀 Future Enhancements

### Planned Features
- A/B testing framework
- Campaign performance tracking
- Integration with email service providers
- Advanced segmentation rules
- Dynamic content blocks
- Multi-language support
- Automated follow-up sequences

### Integration Opportunities
- CRM system integration
- Marketing automation platforms
- Analytics and reporting tools
- Customer feedback collection
- Real-time personalization

## 📞 Support

For technical support or feature requests related to the Email Marketing Campaign feature, please refer to the main application documentation or contact the development team.

---

**Note**: This feature is designed to work with the existing churn prediction and customer analysis system. Ensure all dependencies are properly configured before using the email marketing functionality.
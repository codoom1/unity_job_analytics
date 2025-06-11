# Email Outreach

The SLURM Job Analytics package includes powerful email outreach tools to help administrators communicate with HPC users about their job efficiency and resource usage.

## Overview

The email outreach system allows you to:

- Send personalized efficiency reports to users
- Notify users about suboptimal resource usage
- Provide recommendations for job optimization
- Track outreach campaigns and responses

## Quick Start

### 1. Configure Email Settings

First, set up your email configuration in the environment or configuration file:

```python
from src.outreach.email_manager import EmailManager

# Initialize with your email settings
email_manager = EmailManager(
    smtp_server="your-smtp-server.com",
    smtp_port=587,
    sender_email="hpc-admin@your-org.edu",
    sender_password="your-app-password"
)
```

### 2. Generate User Reports

Create efficiency reports for specific users:

```python
from src.outreach.report_generator import ReportGenerator

# Generate a report for a specific user
report_gen = ReportGenerator()
user_report = report_gen.generate_user_efficiency_report(
    username="jdoe",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### 3. Send Outreach Emails

Send personalized emails to users:

```python
# Send efficiency report to user
email_manager.send_efficiency_report(
    recipient="jdoe@your-org.edu",
    report_data=user_report,
    template="efficiency_report"
)
```

## Email Templates

The system includes several pre-built email templates:

### Efficiency Report Template
- **Purpose**: Monthly efficiency summaries
- **Content**: GPU/CPU utilization, job statistics, recommendations
- **Tone**: Informative and helpful

### Low Efficiency Alert
- **Purpose**: Alert users about consistently low efficiency
- **Content**: Specific metrics, optimization tips, resources
- **Tone**: Constructive and educational

### Best Practices Reminder
- **Purpose**: General reminders about HPC best practices
- **Content**: Resource allocation tips, job submission guidelines
- **Tone**: Educational and supportive

## Customizing Email Content

### Template Customization

You can customize email templates by modifying the template files:

```python
# Customize the efficiency report template
template_path = "templates/efficiency_report.html"
custom_template = report_gen.customize_template(
    template_path,
    custom_branding=True,
    organization_name="Your University HPC",
    contact_email="hpc-support@your-org.edu"
)
```

### Dynamic Content

Include dynamic content based on user data:

```python
# Add personalized recommendations
recommendations = report_gen.generate_recommendations(
    user_efficiency=user_report['efficiency'],
    job_patterns=user_report['patterns'],
    resource_usage=user_report['resources']
)

email_content = {
    'user_name': user_report['username'],
    'efficiency_score': user_report['efficiency'],
    'recommendations': recommendations,
    'support_contact': 'hpc-help@your-org.edu'
}
```

## Batch Operations

### Mass Email Campaigns

Send emails to multiple users at once:

```python
from src.outreach.campaign_manager import CampaignManager

campaign = CampaignManager()

# Define target users (low efficiency users)
target_users = campaign.get_low_efficiency_users(
    threshold=0.6,  # Users with <60% efficiency
    time_period="last_30_days"
)

# Send batch emails
results = campaign.send_batch_emails(
    users=target_users,
    template="low_efficiency_alert",
    delay_between_emails=5  # seconds
)
```

### Scheduling Campaigns

Set up recurring outreach campaigns:

```python
# Schedule monthly efficiency reports
campaign.schedule_recurring_campaign(
    name="monthly_efficiency_reports",
    template="efficiency_report",
    frequency="monthly",
    day_of_month=1,
    target_criteria={
        'min_jobs': 10,  # Users with at least 10 jobs
        'active_period': 30  # Active in last 30 days
    }
)
```

## Analytics and Tracking

### Email Metrics

Track the success of your outreach campaigns:

```python
from src.outreach.analytics import OutreachAnalytics

analytics = OutreachAnalytics()

# Get campaign statistics
stats = analytics.get_campaign_stats(
    campaign_id="monthly_efficiency_reports",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"Emails sent: {stats['sent_count']}")
print(f"Delivery rate: {stats['delivery_rate']:.1%}")
print(f"Open rate: {stats['open_rate']:.1%}")
```

### User Response Tracking

Monitor how users respond to outreach:

```python
# Track efficiency improvements after outreach
response_data = analytics.track_efficiency_improvements(
    campaign_id="low_efficiency_alert",
    follow_up_period=30  # days
)

print(f"Users improved efficiency: {response_data['improved_count']}")
print(f"Average improvement: {response_data['avg_improvement']:.1%}")
```

## Configuration Options

### SMTP Settings

Configure your email server settings:

```yaml
# config/email.yaml
smtp:
  server: "smtp.your-org.edu"
  port: 587
  use_tls: true
  timeout: 30

sender:
  email: "hpc-admin@your-org.edu"
  name: "HPC Administration"
  reply_to: "hpc-support@your-org.edu"
```

### Rate Limiting

Configure email sending limits to avoid overwhelming your SMTP server:

```python
# Set rate limits
email_manager.configure_rate_limits(
    emails_per_minute=10,
    emails_per_hour=200,
    emails_per_day=1000
)
```

### Content Filtering

Set up content filters and approval workflows:

```python
# Require approval for certain email types
campaign.set_approval_required(
    templates=["low_efficiency_alert", "resource_violation"],
    approvers=["admin@your-org.edu"]
)
```

## Best Practices

### Timing
- Send reports during business hours
- Avoid sending too frequently (max once per week per user)
- Schedule bulk campaigns during off-peak hours

### Content
- Keep messages concise and actionable
- Include specific metrics and recommendations
- Provide clear next steps and contact information

### Privacy
- Only include aggregated data in emails
- Avoid sharing sensitive job details
- Respect user preferences for communication frequency

### Monitoring
- Track delivery rates and bounce-backs
- Monitor user feedback and responses
- Adjust messaging based on effectiveness metrics

## Troubleshooting

### Common Issues

**Email delivery failures**:
```python
# Check SMTP connection
connection_status = email_manager.test_connection()
if not connection_status['success']:
    print(f"Connection error: {connection_status['error']}")
```

**Template rendering errors**:
```python
# Validate template before sending
template_valid = report_gen.validate_template("efficiency_report")
if not template_valid['valid']:
    print(f"Template error: {template_valid['errors']}")
```

**Rate limit exceeded**:
```python
# Check current rate limit status
rate_status = email_manager.get_rate_limit_status()
print(f"Emails remaining this hour: {rate_status['remaining_hour']}")
```

## Integration with Dashboard

The email outreach system integrates with the web dashboard for easy management:

1. **Campaign Management**: Create and monitor campaigns through the web interface
2. **Template Editor**: Edit email templates with live preview
3. **Analytics Dashboard**: View outreach metrics and user responses
4. **User Management**: Manage email preferences and opt-outs

Access the outreach features through the dashboard's "Outreach" section.

## API Reference

For detailed API documentation, see the [Email Outreach API Reference](../api-reference/outreach.md).

"""
email_templates.py
-----------------
This module provides email templates for outreach and communication.
Templates may be used for user notifications, reports, or automated messages.

Update this docstring as you add or modify templates or functions in this file.
"""

def generate_email(user, jobs):
    """Generate a personalized outreach email for a user with underutilized GPU jobs."""
    job_list = '\n'.join([f"- JobID {j['JobID']}: {j['GPUMemUsage']/(2**30):.1f} GB used" for j in jobs])
    
    num_jobs = len(jobs)
    total_wasted_gb = sum(j['GPUMemUsage']/(2**30) for j in jobs)
    
    return f"""Dear {user},

Over the past few months, we've noticed that {num_jobs} of your jobs on Unity which requested GPU resources did not fully utilize the allocated GPU memory.

These jobs resulted in approximately {total_wasted_gb:.1f} GB of unused GPU memory. Here are some recent examples:

{job_list}

To help maximize Unity's GPU resources for all users, we recommend:
• Monitoring your GPU memory usage during job execution
• Requesting only the GPU memory you actually need
• Using tools like nvidia-smi to check memory utilization
• Reviewing our GPU best practices documentation

If you need assistance optimizing your GPU usage or have questions about resource allocation, please don't hesitate to reach out to our support team.

Best regards,
Unity Support Team

Note: This is an automated message based on recent job analysis. If you believe this assessment is incorrect, please contact us for clarification.
"""

INTRO = """Dear {name},

Over the past few months, we've noticed that all of your {jobs} jobs on Unity which requested GPU resources did not utilize the requested GPUs."""

HOURS = "{hours} unused GPU hours. The most recent jobs are the following:"

def get_job_type_breakdown(interactive, jobs):
    """Generate job type breakdown text for email."""
    if interactive == jobs:
        return f" These consisted of {interactive} interactive sessions, totaling "
    elif not interactive:
        return " These amounted to "
    else:
        return f" These included {interactive} interactive session{'s' if interactive > 1 else ''}, as well as {jobs-interactive} batch job{'s' if jobs-interactive>1 else ''}, totaling "

def generate_comprehensive_email(user_name, user_data, job_samples):
    """Generate a comprehensive email using the same format as zero_gpu_usage_list.py"""
    jobs = int(user_data.get('WastedJobs', 0))
    hours = int(user_data.get('TotalWastedGB', 0))  # Using GB as proxy for hours
    interactive = int(user_data.get('Interactive', 0))
    
    template = INTRO + get_job_type_breakdown(interactive, jobs) + HOURS
    email_content = template.format(name=user_name, jobs=jobs, hours=hours)
    
    # Add job samples
    job_details = "\n".join([
        f"JobID {job['JobID']}: {job['GPUMemUsage']/(2**30):.1f} GB used" 
        for job in job_samples
    ])
    
    email_content += f"\n\n{job_details}"
    
    email_content += """

To help maximize Unity's GPU resources for all users, we recommend:
• Monitoring your GPU memory usage during job execution
• Requesting only the GPU memory you actually need
• Using tools like nvidia-smi to check memory utilization
• Reviewing our GPU best practices documentation

If you need assistance optimizing your GPU usage, please contact our support team.

Best regards,
Unity Support Team
"""

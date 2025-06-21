import os
import csv
from typing import Dict, List, Any
from logger import get_logger

logger = get_logger(__name__)


def save_to_results_csv(project: str, assessment: Dict[str, Any], category_stats: Dict[str, Dict] = None):
    """
    Save assessment results to a single CSV file in real-time.
    
    Args:
        project: Name of the project being assessed
        assessment: Dictionary containing assessment results with criteria IDs as keys
        category_stats: Optional dictionary containing category statistics
    """
    csv_file = "data/outputs/results.csv"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(csv_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Calculate overall statistics
    total_criteria = len(assessment)
    met_criteria = sum(1 for score in assessment.values() if score.get("score", 0) == 1)
    percentage = round(met_criteria/total_criteria*100, 1) if total_criteria > 0 else 0
    
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.exists(csv_file)
    
    # Append results to CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header if file doesn't exist
        if not file_exists:
            headers = ['project', 'total_criteria', 'met_criteria', 'percentage', 'timestamp']
            if category_stats:
                headers.extend(['essential_met', 'essential_total', 'essential_percentage',
                               'professional_met', 'professional_total', 'professional_percentage',
                               'elite_met', 'elite_total', 'elite_percentage'])
            writer.writerow(headers)
        
        # Write project results
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [project, total_criteria, met_criteria, percentage, timestamp]
        
        if category_stats:
            for category in ['Essential', 'Professional', 'Elite']:
                stats = category_stats.get(category, {'met': 0, 'total': 0, 'percentage': 0})
                row.extend([stats['met'], stats['total'], stats['percentage']])
        
        writer.writerow(row)
    
    logger.info(f"Results saved to {csv_file}")


def generate_markdown_report(
        project: str,
    assessment: Dict[str, Any],
    output_file: str,
    criteria_types: Dict[str, List[str]],
    criteria_names: Dict[str, str],
    category_criteria: Dict[str, List[str]],
):
    """
    Generate a Markdown report summarizing criteria satisfaction.

    Args:
        project: Name of the project being assessed
        assessment: Dictionary containing assessment results with criteria IDs as keys
        output_file: Path where to save the Markdown report
        criteria_types: Dictionary mapping category names to lists of criteria IDs
        criteria_names: Dictionary mapping criteria IDs to their display names
        category_criteria: Dictionary mapping category names to lists of criteria IDs
    """
    
    total_criteria = len(assessment)
    met_criteria = sum(1 for score in assessment.values() if score.get("score", 0) == 1)
    percentage = round(met_criteria/total_criteria*100, 1) if total_criteria > 0 else 0

    # Calculate statistics by category
    category_stats = {}

    # First get essential criteria
    essential_criteria = [
        crit for crit in criteria_types.get("Essential", []) if crit in assessment
    ]

    # Professional excludes essential
    professional_criteria = [
        crit
        for crit in criteria_types.get("Professional", [])
        if crit in assessment and crit not in essential_criteria
    ]

    # Elite excludes both essential and professional
    elite_criteria = [
        crit
        for crit in criteria_types.get("Elite", [])
        if crit in assessment
        and crit not in essential_criteria
        and crit not in professional_criteria
    ]

    # Calculate stats for each filtered category
    filtered_categories = {
        "Essential": essential_criteria,
        "Professional": professional_criteria,
        "Elite": elite_criteria,
    }

    for category, criteria_list in filtered_categories.items():
        total_in_category = len(criteria_list)
        met_in_category = sum(
            1 for crit in criteria_list if assessment[crit].get("score", 0) == 1
        )
        category_stats[category] = {
            "total": total_in_category,
            "met": met_in_category,
            "percentage": (
                round(met_in_category / total_in_category * 100, 1)
                if total_in_category > 0
                else 0
            ),
        }

    # Save to results CSV with category stats
    save_to_results_csv(project, assessment, category_stats)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate Markdown report
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Quality Assessment Report\n\n")

        # Overall summary
        f.write("## Overall Summary\n\n")
        f.write(f"- **Total Criteria**: {total_criteria}\n")
        f.write(
            f"- **Criteria Met**: {met_criteria} ({percentage}%)\n\n"
        )

        # Category breakdown
        f.write("## Category Breakdown\n\n")
        f.write("| Category | Criteria Met | Total Criteria | Percentage |\n")
        f.write("|----------|-------------|----------------|------------|\n")
        for category, stats in category_stats.items():
            f.write(
                f"| {category} | {stats['met']} | {stats['total']} | {stats['percentage']}% |\n"
            )
        f.write("\n")

        # Detailed criteria breakdown
        f.write("## Detailed Criteria Breakdown\n\n")

        # Use the already filtered lists for each category
        category_filtered_criteria = {
            "Essential": essential_criteria,
            "Professional": professional_criteria,
            "Elite": elite_criteria,
        }

        for category, criteria_list in category_filtered_criteria.items():
            if not criteria_list:
                continue

            f.write(f"### {category} Criteria\n\n")
            f.write("| Category | Criterion | Status | Explanation |\n")
            f.write("|------------|------------|----------|------------------------|\n")

            for criterion in criteria_list:
                # Find which category this criterion belongs to
                criterion_category = None
                for cat, criteria in category_criteria.items():
                    if criterion in criteria:
                        criterion_category = cat
                        break

                status = "✅" if assessment[criterion].get("score", 0) == 1 else "❌"
                explanation = assessment[criterion].get(
                    "explanation", "No explanation provided"
                )
                f.write(
                    f"| {criterion_category} | {criteria_names[criterion]} | {status} | {explanation} |\n"
                )

            f.write("\n")

    logger.info(f"Report generated successfully at {output_file}")
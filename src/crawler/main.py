import click
import sys
import os
import logging
from crawler.domain.models import InputItem
from crawler.services.profiles import load_aws_profiles
from crawler.adapters.storage import load_input

# Configuração básica de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("LambdaCrawler")

@click.command()
@click.option('--input', 'input_file', required=True, type=click.Path(exists=True), help='Path to JSON input file.')
@click.option('--days', default=180, help='Days to look back for execution metrics (Default: 180).')
@click.option('--limit', default=0, help='Limit number of items to process (0 = No limit).')
def main(input_file, days, limit):
    """
    AWS Lambda FinOps Crawler.
    Audits execution and triggers for a list of functions across accounts.
    """
    click.echo(f"Starting Lambda Crawler...")
    click.echo(f"Input: {input_file}")
    click.echo(f"Window: {days} days")
    
    try:
        # Determine output filenames
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        report_file = f"{base_name}_report.xlsx"
        errors_file = f"{base_name}_errors.json"

        # 1. Load Input
        items = load_input(input_file)
        logger.info(f"Loaded {len(items)} items from input.")
        
        # 2. Apply Limit
        if limit > 0:
            logger.info(f"Limit set to {limit}. truncating list.")
            items = items[:limit]
            
        # 3. Load Profiles
        # (Orchestrator loads internally, but acceptable to keep log)
        
        # 4. Run Crawler
        from crawler.orchestrator import run_crawler
        results = run_crawler(items, days)
        
        # 5. Generate Report
        from crawler.adapters.excel import generate_report
        generate_report(results, report_file)
        
        # 6. Save Errors JSON (Retry State)
        from crawler.adapters.storage import save_errors
        errors = []
        for r in results:
            if r.status == "ERROR":
                errors.append({
                    "name": r.function_name,
                    "account": r.account_id,
                    "region": r.region,
                    "_error": r.error_message
                })
        
        if errors:
            save_errors(errors_file, errors)
            logger.warning(f"Saved {len(errors)} failed items to {errors_file}")
            
        logger.info("Done.")

    except Exception as e:
        logger.error(f"Fatal Error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()

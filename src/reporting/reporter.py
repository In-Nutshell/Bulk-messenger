import json
from datetime import datetime
from typing import Dict, List
import logging


class Reporter:
    """Handles report generation and statistics"""
    
    def __init__(self, file_path: str = 'messaging_report.json'):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        
    def generate_report(self, successful_sends: List[Dict], failed_contacts: List[Dict]) -> Dict:
        """Generate detailed report"""
        report = {
            'summary': {
                'total_successful': len(successful_sends),
                'total_failed': len(failed_contacts),
                'report_generated': datetime.now().isoformat()
            },
            'successful_sends': successful_sends,
            'failed_contacts': failed_contacts
        }
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Report saved to {self.file_path}")
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
            
        return report
        
    def print_summary(self, summary: Dict, successful_sends: List[Dict], 
                     failed_contacts: List[Dict]) -> None:
        """Print detailed summary to console"""
        print(f"\n{'='*50}")
        print(f"MESSAGING SUMMARY")
        print(f"{'='*50}")
        print(f"Total contacts processed: {summary['total_contacts']}")
        print(f"Successful sends: {summary['successful_sends']}")
        print(f"Failed sends: {summary['failed_sends']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print(f"{'='*50}")
        
        # Show successful sends
        if successful_sends:
            print(f"\nSUCCESSFUL SENDS (showing first 5):")
            for i, send in enumerate(successful_sends[:5]):
                print(f"  {i+1}. {send['contact_key']} -> {send['identifier_type']} -> User ID: {send['user_id']}")
        
        # Show failed sends
        if failed_contacts:
            print(f"\nFAILED SENDS (showing first 5):")
            for i, fail in enumerate(failed_contacts[:5]):
                tried = fail.get('tried_identifiers', ['unknown'])
                print(f"  {i+1}. {fail['contact_key']} -> {fail['error']}")
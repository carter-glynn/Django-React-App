from abc import ABC, abstractmethod

class Report(ABC):
    def __init__(self, items):
        self.items = items  # Inventory data to include in the report

    @abstractmethod
    def generate(self):
        """Generate the report content."""
        pass

class InsuranceReport(Report):
    def generate(self):
        # Generate a detailed insurance report
        report_data = "Insurance Report\n\n"
        for item in self.items:
            report_data += f"Name: {item['name']}\nValue: ${item['price']}\nPhoto: {item['image_url']}\n\n"
        return report_data

class MovingReport(Report):
    def generate(self):
        # Generate a moving inventory report
        report_data = "Moving Inventory Report\n\n"
        for item in self.items:
            report_data += f"Name: {item['name']}\nCategory: {item['category']}\nPurchase Date: {item['purchase_date']}\n\n"
        return report_data

class MaintenanceReport(Report):
    def generate(self):
        # Generate a maintenance schedule report
        report_data = "Maintenance Schedule Report\n\n"
        for item in self.items:
            if item['warranty_expiration']:
                report_data += f"Name: {item['name']}\nWarranty Expiration: {item['warranty_expiration']}\n\n"
            else:
                report_data += f"Name: {item['name']}\nNo warranty information available.\n\n"
        return report_data

class ReportFactory:
    @staticmethod
    def create_report(report_type, items):
        if report_type == "insurance":
            return InsuranceReport(items)
        elif report_type == "moving":
            return MovingReport(items)
        elif report_type == "maintenance":
            return MaintenanceReport(items)
        else:
            raise ValueError(f"Unknown report type: {report_type}")
